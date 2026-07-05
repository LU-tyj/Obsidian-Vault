---
name: update-review
description: 同步复习进度 — 以复习追踪表为唯一真源，回写笔记 frontmatter、计算下次复习日期、更新统计面板、生成今日待复习清单。触发词：同步复习进度、更新复习记录、跑一下复习追踪、今天该复习哪些笔记、生成待复习清单
---

# 复习进度同步

以 `复习追踪表.md` 为唯一真源（source of truth），单向同步到每篇笔记的 frontmatter。用户只手动维护追踪表，其余全部自动化。

## 核心原则

- **表格是唯一真源**：如果表格和笔记 frontmatter 不一致，以表格为准，覆盖笔记
- **脚本做确定性计算**：日期数学、统计面板、待复习清单均由 Python 脚本完成，不依赖 LLM 推理
- **只写三个字段**：脚本只修改笔记 frontmatter 的 `status` / `last_reviewed` / `next_review`，不动其他字段和正文

## 工作流程

```
用户手动改追踪表 → 用户说触发词 → Claude 调用脚本 → 脚本输出 JSON 摘要 → Claude 解读并汇报
```

### 第一步：调用脚本

```bash
python3 .claude/skills/update-review/scripts/sync_review_progress.py \
  "/Users/touyijun/Obsidian/NGNL/No Game No Life/面试/00-总览/复习追踪表.md"
```

### 第二步：解读脚本输出

脚本输出一个 JSON 对象到 stdout，包含：

```json
{
  "synced_count": 3,
  "synced_notes": ["Cpp 虚函数与多态", "Cpp 智能指针", "Unity 生命周期"],
  "degraded_notes": [],
  "broken_links": [],
  "review_count_warnings": [],
  "today_review_list": [
    {"name": "Cpp 虚函数与多态", "frequency": 3, "status": "reviewing", "next_review": "2026-07-05"}
  ],
  "stats": {
    "00-Cpp语言基础": {"total": 17, "new": 14, "reviewing": 3, "mastered": 0},
    ...
    "total": {"total": 153, "new": 150, "reviewing": 3, "mastered": 0}
  }
}
```

### 第三步：向用户汇报

用自然语言汇报：
1. 本次同步了几篇笔记的 frontmatter → 列出笔记名
2. 如果有 `degraded_notes`：提醒用户笔记 frontmatter 已是 mastered 但表格还是 reviewing，问是否需要把表格也改成 mastered
3. 如果有 `broken_links`：列出路径失效的笔记
4. 如果有 `review_count_warnings`：提醒复习次数异常
5. 展示各专题最新完成率
6. 列出今日待复习清单（按频率降序、最多 20 条）

## 关键规则

- **绝不**反过来用笔记 frontmatter 覆盖表格
- 如果某行解析失败（缺 wikilink、格式异常），跳过该行并在 broken_links 中记录
- 脚本运行后追踪表会被原地更新（统计面板 + 下次复习列），用户无需手动改那些列

## 文件位置

- 追踪表：`No Game No Life/面试/00-总览/复习追踪表.md`
- 脚本：`.claude/skills/update-review/scripts/sync_review_progress.py`
- 笔记库根目录：`/Users/touyijun/Obsidian/NGNL/`
