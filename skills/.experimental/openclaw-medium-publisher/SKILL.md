---
name: openclaw-medium-publisher
description: Prepare and polish drafts for Medium publication with Medium-safe formatting and media rules. Use when cleaning Markdown or DOCX-derived content, fixing heading/list structure, replacing unsupported image usage (local file paths or SVG embeds), generating reader topics, and producing a final paste-ready article.
---

# OpenClaw Medium Publisher

## Overview

Use this skill to turn a rough draft into a Medium-ready post with clean structure, predictable rendering, and publish-safe media handling.

## Workflow

1. Collect source and target format.
- Accept Markdown or extracted DOCX text.
- Keep wording intact unless the user asks for rewriting.

2. Normalize article structure.
- Use heading levels consistently.
- Remove numeric heading prefixes like `1)` unless explicitly requested.
- Keep bullet lists flat (single level) unless hierarchy is essential.
- Avoid turning example quotes into list items unless the user asks.

3. Enforce Medium media rules.
- Do not use local file paths in image links.
- Do not rely on SVG embeds in Medium posts.
- Prefer PNG/JPG/WebP assets uploaded through the Medium editor.
- Replace invalid image links with upload placeholders or instructions.

4. Run a formatting check.
- Run `scripts/medium_lint.py <file>` to detect Medium-hostile patterns.
- If issues exist, run `scripts/medium_fix.py <file> --in-place` or patch manually.

5. Prepare final delivery.
- Provide one clean, paste-ready Markdown body.
- Provide short topic suggestions (up to five).
- Provide image placement notes with caption text.

## Media Rules (Strict)

- Never publish Markdown that references local absolute filesystem paths.
- Never assume Medium will render `image/svg+xml` reliably in article content.
- Keep captions as normal text immediately under each image.

## Topic Guidance

- Return up to five topics.
- Prefer discoverable, broad-first topics plus one specific topic.
- See `references/topic-presets.md` for reusable sets.

## Resources

### scripts/
- `scripts/medium_lint.py`: Detect formatting/media issues before publishing.
- `scripts/medium_fix.py`: Apply safe structural fixes for common Medium issues.

### references/
- `references/medium-publish-checklist.md`: Final pre-publish checks.
- `references/topic-presets.md`: Reusable topic bundles.
