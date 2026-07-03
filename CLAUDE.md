# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an **Obsidian vault** (named "NGNL" / No Game No Life) containing personal notes on game development. Notes are written primarily in Chinese, with technical terms and some sections in English.

## Vault Structure

- `No Game No Life/GAMES104/` — Course notes from the GAMES104 game engine course (16 lectures)
- `No Game No Life/Game Programming Patterns/` — Notes from the "Game Programming Patterns" book, organized by chapter
- `No Game No Life/Gameplay/` — Game project designs and framework analysis (e.g., Unity GAS, Slay the Spire 2 source study, turn-based combat frameworks)
- `No Game No Life/Multiplayer/` — Multiplayer/networking game development notes
- `No Game No Life/面试/` — Interview preparation notes (NetEase Unity game client, LeetCode)
- `Clippings/` — Web-clipped content
- `吾日三省吾身/` — Personal reflections

## Obsidian Conventions

- New notes go in the same folder as the current file (`newFileLocation: "current"`)
- Attachments are stored in `./assets` relative to each note
- Theme: Blue Topaz

## Image Handling

Images are stored in `assets/` subdirectories relative to the notes that reference them. When adding images to notes, place them in the appropriate `assets/` folder and use relative wiki-links or markdown links.

## Git

The `.gitignore` excludes Obsidian plugin/theme files, workspace state, and binary attachments. PDFs under GAMES104 are also excluded.
