#!/usr/bin/env python3
"""Sync review progress from tracking table back to note frontmatter.

Source of truth: 复习追踪表.md (the table).
Direction: table → note frontmatter (one-way).

Usage:
    python3 sync_review_progress.py /path/to/复习追踪表.md
"""

import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


# --- Config ---
INTERVALS = {1: 1, 2: 3, 3: 7, 4: 15}  # review_count → days until next review
DEFAULT_INTERVAL = 30  # for review_count >= 5

# --- Helpers ---


def parse_date(s: str) -> date | None:
    """Parse YYYY-MM-DD string, return None on failure or placeholder."""
    s = s.strip()
    if not s or s == "—" or s == "-":
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def fmt_date(d: date | None) -> str:
    return d.strftime("%Y-%m-%d") if d else "—"


def add_days(d: date | None, n: int) -> date | None:
    return d + timedelta(days=n) if d else None


def next_review_date(review_count: int, last_review: date | None) -> str:
    """Calculate next review date based on review count and last review date."""
    if last_review is None:
        return "—"
    interval = INTERVALS.get(review_count, DEFAULT_INTERVAL)
    return fmt_date(add_days(last_review, interval))


def parse_wikilink(cell: str) -> tuple[str, str] | None:
    """Extract (path, display_name) from [[path|display]] or [[path]] wikilink."""
    m = re.search(r"\[\[([^\]]+)\]\]", cell)
    if not m:
        return None
    content = m.group(1)
    if "|" in content:
        path, display = content.split("|", 1)
        return path.strip(), display.strip()
    return content.strip(), content.strip()


def resolve_note_path(table_dir: Path, wikilink_path: str) -> Path:
    """Resolve a wikilink path relative to the table's directory."""
    return (table_dir / wikilink_path).resolve()


def parse_frontmatter(filepath: Path) -> dict:
    """Parse YAML frontmatter from a markdown file. Returns empty dict on failure."""
    if not filepath.exists():
        return {}
    text = filepath.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    # Simple YAML parser for the 3 fields we care about
    fm = {}
    for line in m.group(1).split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            fm[key] = val
    return fm


def write_frontmatter(filepath: Path, updates: dict):
    """Update specific frontmatter fields in a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    # Find frontmatter block
    m = re.match(r"^(---\s*\n)(.*?)(\n---)", text, re.DOTALL)
    if not m:
        return
    before = m.group(1)
    body = m.group(2)
    after = m.group(3)
    rest = text[m.end():]

    lines = body.split("\n")
    new_lines = []
    updated_keys = set()

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue
        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            if key in updates:
                new_val = updates[key]
                if new_val is not None and new_val != "—":
                    new_lines.append(f"{key}: {new_val}")
                elif key == "next_review":
                    # Keep next_review but with empty value if cleared
                    new_lines.append(f"{key}: ")
                else:
                    new_lines.append(f"{key}: {val}")
                updated_keys.add(key)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Append any new keys that weren't in the original frontmatter
    for k, v in updates.items():
        if k not in updated_keys and v is not None and v != "—":
            new_lines.append(f"{k}: {v}")

    new_text = before + "\n".join(new_lines) + after + rest
    filepath.write_text(new_text, encoding="utf-8")


# --- Table Parsing ---


def parse_tracking_table(filepath: str) -> tuple[list[dict], list[str], list[str]]:
    """Parse the tracking table. Returns (rows, stats_block_lines, pre_stats_lines).

    Each row dict:
        {section, sub_section, num, name, wikilink_path, wikilink_display,
         frequency, status, first_study, last_review, review_count, next_review,
         line_index_in_file}
    """
    table_dir = Path(filepath).resolve().parent
    text = Path(filepath).read_text(encoding="utf-8")
    lines = text.split("\n")

    rows = []
    current_section = None
    current_subsection = None
    in_table = False
    header_cols = None
    stats_start = None
    pre_stats_lines = []

    for i, line in enumerate(lines):
        # Track section headers
        if line.startswith("## ") and "统计面板" not in line:
            current_section = line.strip("# ").strip()
            current_subsection = None
            continue
        if line.startswith("### "):
            current_subsection = line.strip("# ").strip()
            continue

        # Detect stats panel
        if line.startswith("## 统计面板"):
            stats_start = i
            # Collect all pre-stats content
            pre_stats_lines = lines[:i]
            continue

        # Detect table start/end
        if line.startswith("|") and not in_table:
            # Check if next line is a separator
            if i + 1 < len(lines) and re.match(r"\|[\s\-:|]+\|", lines[i + 1]):
                in_table = True
                header_cols = [c.strip() for c in line.split("|")[1:-1]]
                continue

        if in_table:
            if line.startswith("|") and not re.match(r"\|[\s\-:|]+\|", line):
                cols = [c.strip() for c in line.split("|")[1:-1]]
                if len(cols) >= 8:
                    try:
                        num = int(cols[0])
                    except ValueError:
                        continue

                    wl = parse_wikilink(cols[1])
                    if not wl:
                        continue

                    frequency = int(cols[2]) if cols[2].isdigit() else 1
                    status = cols[3].strip()
                    first_study = cols[4].strip() if len(cols) > 4 else "—"
                    last_review = cols[5].strip() if len(cols) > 5 else "—"
                    review_count = int(cols[6]) if len(cols) > 6 and cols[6].isdigit() else 0
                    next_review_val = cols[7].strip() if len(cols) > 7 else "—"

                    rows.append({
                        "section": current_section,
                        "subsection": current_subsection,
                        "num": num,
                        "name": wl[1],
                        "wikilink_path": wl[0],
                        "wikilink_display": wl[1],
                        "frequency": frequency,
                        "status": status,
                        "first_study": first_study,
                        "last_review": last_review,
                        "review_count": review_count,
                        "next_review": next_review_val,
                        "line_index": i,
                    })
            elif not line.startswith("|"):
                in_table = False
                header_cols = None

    if stats_start is None:
        stats_start = len(lines)

    return rows, lines[stats_start:], pre_stats_lines


# --- Main Sync Logic ---


def sync(table_path: str) -> dict:
    table_dir = Path(table_path).resolve().parent
    rows, stats_lines, pre_lines = parse_tracking_table(table_path)

    synced = []
    degraded = []
    broken = []
    review_warnings = []

    for row in rows:
        wl_path = row["wikilink_path"]
        note_path = resolve_note_path(table_dir, wl_path)

        if not note_path.exists():
            broken.append(f"{row['name']} ({wl_path})")
            continue

        fm = parse_frontmatter(note_path)

        # Compare table vs frontmatter
        table_status = row["status"]
        fm_status = fm.get("status", "new")

        table_last_review = row["last_review"]
        fm_last_review = fm.get("last_reviewed", "")

        # Determine if user manually changed the table
        status_changed = table_status != fm_status
        date_changed = (table_last_review != "—" and table_last_review != fm_last_review)

        if not status_changed and not date_changed:
            # Also check if next_review needs recalculation (review_count may have changed
            # without status/last_review changing — edge case, skip)
            continue

        # Detect degradation: frontmatter says mastered, table says reviewing/new
        if fm_status == "mastered" and table_status in ("new", "reviewing"):
            degraded.append(f"{row['name']} (fm: {fm_status} → table: {table_status})")

        # Check review_count decreasing
        # We can't easily track previous count without reading the old frontmatter review_count
        # But we can check if it went to 0 from something
        old_fm_review_count = fm.get("review_count", "")
        if old_fm_review_count and old_fm_review_count.isdigit():
            old_rc = int(old_fm_review_count)
            if row["review_count"] < old_rc:
                review_warnings.append(
                    f"{row['name']}: 复习次数 {old_rc} → {row['review_count']}，请确认是否手误"
                )

        # Calculate new values
        new_status = table_status
        rc = row["review_count"]

        # Determine last_review date
        lr_date = parse_date(table_last_review)
        if lr_date is None and table_status == "reviewing":
            # Fallback: use first_study date or today
            lr_date = parse_date(row["first_study"]) or date.today()
            table_last_review = fmt_date(lr_date)

        # Calculate next_review
        nr = "—"
        if lr_date and table_status != "new":
            nr = next_review_date(rc, lr_date)
        elif table_status == "new":
            nr = "—"

        # Update row's next_review in memory
        row["next_review"] = nr
        row["last_review"] = table_last_review

        # Write to note frontmatter
        frontmatter_updates = {
            "status": new_status,
            "last_reviewed": table_last_review if table_last_review != "—" else "",
            "next_review": nr if nr != "—" else "",
        }
        write_frontmatter(note_path, frontmatter_updates)
        synced.append(row["name"])

    # --- Rebuild stats ---
    stats = {}
    for row in rows:
        sec = row["section"]
        if sec not in stats:
            stats[sec] = {"total": 0, "new": 0, "reviewing": 0, "mastered": 0}
        stats[sec]["total"] += 1
        s = row["status"]
        if s in stats[sec]:
            stats[sec][s] += 1
        else:
            stats[sec]["new"] += 1  # fallback

    # Section display order
    section_order = [
        "00-Cpp语言基础（17 篇）",
        "01-Csharp语言基础（19 篇）",
        "02-Unity引擎原理（20 篇）",
        "03-图形学与渲染（19 篇）",
        "04-计算机基础（15 篇）",
        "05-数据结构与算法（12 篇）",
        "06-设计模式（9 篇）",
        "07-性能优化与内存管理（11 篇）",
        "08-系统设计与项目经验（9 篇）",
        "09-网易互娱专项（3 篇）",
        "10-算法手撕高频题（19 篇）",
    ]

    total_new = sum(s["new"] for s in stats.values())
    total_reviewing = sum(s["reviewing"] for s in stats.values())
    total_mastered = sum(s["mastered"] for s in stats.values())
    total_all = sum(s["total"] for s in stats.values())

    # Build new stats panel
    new_stats_lines = [
        "## 统计面板",
        "",
        "> 本面板由 `sync_review_progress.py` 自动生成，请勿手动编辑，运行 skill 后会自动覆盖。",
        "",
        "| 大专题 | 总数 | new | reviewing | mastered | 完成率 |",
        "|--------|------|-----|-----------|----------|--------|",
    ]

    for sec_name in section_order:
        s = stats.get(sec_name, {"total": 0, "new": 0, "reviewing": 0, "mastered": 0})
        total = s["total"]
        rate = f"{s['mastered'] / total * 100:.0f}%" if total > 0 else "0%"
        short_name = sec_name.split("（")[0] if "（" in sec_name else sec_name
        new_stats_lines.append(
            f"| {short_name} | {total} | {s['new']} | {s['reviewing']} | {s['mastered']} | {rate} |"
        )

    new_stats_lines.append(
        f"| **合计** | **{total_all}** | **{total_new}** | **{total_reviewing}** | **{total_mastered}** | **{total_mastered / total_all * 100:.0f}%** |"
        if total_all > 0 else
        f"| **合计** | **0** | **0** | **0** | **0** | **0%** |"
    )
    new_stats_lines.append("")

    # --- Rebuild the file ---
    # Write: pre_stats content (before stats panel) + new stats + footer
    # The pre_stats_lines already includes everything before ## 统计面板
    # We need to also update the next_review values in the table rows

    # Re-read the full text for rebuilding
    full_text = Path(table_path).read_text(encoding="utf-8")
    all_lines = full_text.split("\n")

    # Update each row's next_review in the text
    row_map = {r["line_index"]: r for r in rows}
    new_all_lines = []
    for i, line in enumerate(all_lines):
        if i in row_map:
            r = row_map[i]
            # Rebuild the table row with updated values
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 8:
                cols[3] = r["status"]
                cols[4] = r["first_study"]
                cols[5] = r["last_review"]
                cols[6] = str(r["review_count"])
                cols[7] = r["next_review"]
                # Reconstruct line preserving original formatting approach
                new_line = "| " + " | ".join(cols) + " |"
                new_all_lines.append(new_line)
            else:
                new_all_lines.append(line)
        else:
            new_all_lines.append(line)

    # Find stats panel boundaries in the updated text
    stats_start_idx = None
    stats_end_idx = None
    for i, line in enumerate(new_all_lines):
        if line.startswith("## 统计面板"):
            stats_start_idx = i
        if stats_start_idx is not None and i > stats_start_idx:
            if line.startswith("## ") or line.startswith("# "):
                stats_end_idx = i
                break
    if stats_end_idx is None:
        stats_end_idx = len(new_all_lines)

    # Also find and remove the trailing old footer (建议工作流 section starts after stats)
    # Keep going until we find the next ## section after stats
    footer_start = stats_end_idx
    for i in range(stats_end_idx, len(new_all_lines)):
        if new_all_lines[i].startswith("## "):
            footer_start = i
            break
    else:
        footer_start = len(new_all_lines)

    # Build final file: content before stats + new stats + footer content
    final_lines = new_all_lines[:stats_start_idx] + new_stats_lines + new_all_lines[footer_start:]

    Path(table_path).write_text("\n".join(final_lines), encoding="utf-8")

    # --- Build today's review list ---
    today = date.today()
    today_review = []
    for row in rows:
        nr_date = parse_date(row["next_review"])
        if nr_date and nr_date <= today and row["status"] != "mastered":
            today_review.append({
                "name": row["name"],
                "frequency": row["frequency"],
                "status": row["status"],
                "next_review": row["next_review"],
                "section": row["section"],
            })

    # Also include mastered items due for review as optional
    mastered_due = []
    for row in rows:
        nr_date = parse_date(row["next_review"])
        if nr_date and nr_date <= today and row["status"] == "mastered":
            mastered_due.append({
                "name": row["name"],
                "frequency": row["frequency"],
                "status": row["status"],
                "next_review": row["next_review"],
                "section": row["section"],
            })

    # Sort by frequency desc
    today_review.sort(key=lambda x: (-x["frequency"], x["name"]))
    mastered_due.sort(key=lambda x: (-x["frequency"], x["name"]))

    return {
        "synced_count": len(synced),
        "synced_notes": synced,
        "degraded_notes": degraded,
        "broken_links": broken,
        "review_count_warnings": review_warnings,
        "today_review_list": today_review,
        "mastered_due": mastered_due,
        "stats": {
            "by_section": stats,
            "total": {
                "total": total_all,
                "new": total_new,
                "reviewing": total_reviewing,
                "mastered": total_mastered,
            },
        },
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 sync_review_progress.py <path-to-复习追踪表.md>", file=sys.stderr)
        sys.exit(1)

    table_path = sys.argv[1]
    result = sync(table_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
