#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BOOK_ROOT = ROOT / "en"
ENTRYPOINTS = [BOOK_ROOT / "README.md", BOOK_ROOT / "SUMMARY.md"]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def internal_links(path: Path) -> list[Path]:
    text = path.read_text(encoding="utf-8")
    text = FENCED_CODE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    out: list[Path] = []
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip()
        if not target or target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        out.append((path.parent / target).resolve())
    return out


def main() -> int:
    markdown_files = {
        p.resolve() for p in BOOK_ROOT.rglob("*.md") if "_book" not in p.parts
    }
    broken: list[str] = []

    for path in sorted(markdown_files):
        for target in internal_links(path):
            if target not in markdown_files:
                broken.append(f"{path.relative_to(ROOT)} -> {target}")

    if broken:
        print("Broken internal links:")
        for item in broken:
            print(item)
        return 1

    seen = {p.resolve() for p in ENTRYPOINTS}
    stack = list(seen)

    while stack:
        path = stack.pop()
        if not path.exists():
            continue
        for target in internal_links(path):
            if target in markdown_files and target not in seen:
                seen.add(target)
                stack.append(target)

    unreachable = sorted(
        p.relative_to(ROOT).as_posix() for p in markdown_files if p not in seen
    )
    if unreachable:
        print("Unreachable markdown pages (not in README.md or SUMMARY.md):")
        for item in unreachable:
            print(item)
        return 1

    # New check: Ensure all content files are linked in README.md
    readme_path = BOOK_ROOT / "README.md"
    readme_links = set(internal_links(readme_path))
    content_files = markdown_files - {readme_path.resolve(), (BOOK_ROOT / "SUMMARY.md").resolve()}
    
    missing_from_readme = sorted(
        p.relative_to(ROOT).as_posix() for p in content_files if p not in readme_links
    )
    
    if missing_from_readme:
        print("Markdown pages missing from en/README.md:")
        for item in missing_from_readme:
            print(item)
        return 1

    print(f"OK: {len(markdown_files)} markdown pages are internally linked, reachable, and indexed in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
