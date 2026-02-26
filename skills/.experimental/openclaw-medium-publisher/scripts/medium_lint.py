#!/usr/bin/env python3
"""Lint Markdown for Medium-hostile formatting and media patterns."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
NUMBERED_HEADING_RE = re.compile(r"^#{2,6}\s+\d+\)\s+", re.MULTILINE)
BULLET_RE = re.compile(r"^(\s*)[-*]\s+", re.MULTILINE)
EXAMPLE_BULLET_RE = re.compile(r"(?m)^Example:\n\s*[-*]\s+")


def lint_text(text: str) -> list[str]:
    findings: list[str] = []

    for match in IMAGE_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith("/") or target.startswith("file://") or re.match(r"^[A-Za-z]:\\", target):
            findings.append(f"Local image path is not Medium-safe: {target}")
        if target.lower().endswith(".svg"):
            findings.append(f"SVG image link may not render reliably on Medium: {target}")

    if NUMBERED_HEADING_RE.search(text):
        findings.append("Numbered heading prefix detected (e.g., '## 1) ...').")

    for i, line in enumerate(text.splitlines(), start=1):
        if re.match(r"^\s{2,}[-*]\s+", line):
            findings.append(f"Nested/indented bullet detected at line {i}: {line.strip()}")

    if EXAMPLE_BULLET_RE.search(text):
        findings.append("Example block uses bullet immediately after 'Example:'; consider plain text quote.")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint Markdown for Medium compatibility")
    parser.add_argument("file", type=Path, help="Markdown file path")
    parser.add_argument("--strict", action="store_true", help="Return non-zero exit code if issues are found")
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8")
    findings = lint_text(text)

    if not findings:
        print("No Medium formatting issues found.")
        return 0

    print(f"Found {len(findings)} issue(s):")
    for issue in findings:
        print(f"- {issue}")

    return 1 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
