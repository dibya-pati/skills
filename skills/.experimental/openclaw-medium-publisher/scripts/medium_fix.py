#!/usr/bin/env python3
"""Apply safe Markdown fixes for Medium publishing."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def fix_markdown(text: str) -> str:
    # Remove numeric heading prefixes: ## 1) Title -> ## Title
    text = re.sub(r"(?m)^(#{2,6}\s+)\d+\)\s+", r"\1", text)

    # Convert Example:
    # - "quote"
    # to plain quote line
    text = re.sub(r"(?m)^Example:\n\s*[-*]\s+(\".*\")", r"Example:\n\1", text)

    # Convert local absolute image links to explicit upload placeholders.
    def repl_image(match: re.Match[str]) -> str:
        alt = match.group(1)
        target = match.group(2).strip()
        if target.startswith("/") or target.startswith("file://") or re.match(r"^[A-Za-z]:\\", target):
            name = Path(target).name
            if name.lower().endswith(".svg"):
                name = name[:-4] + ".png"
            return f"![{alt}](UPLOAD_THIS_IMAGE:{name})"
        if target.lower().endswith(".svg"):
            return f"![{alt}]({target[:-4]}.png)"
        return match.group(0)

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl_image, text)

    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply safe Markdown fixes for Medium")
    parser.add_argument("file", type=Path, help="Markdown file path")
    parser.add_argument("--in-place", action="store_true", help="Overwrite file in place")
    args = parser.parse_args()

    original = args.file.read_text(encoding="utf-8")
    fixed = fix_markdown(original)

    if args.in_place:
        args.file.write_text(fixed, encoding="utf-8")
        print(f"Updated {args.file}")
    else:
        print(fixed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
