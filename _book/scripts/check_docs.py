#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LANGS = ["zh", "en"]
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


def check_lang(lang: str) -> int:
    book_root = ROOT / lang
    entrypoints = [book_root / "README.md", book_root / "SUMMARY.md"]
    markdown_files = {
        p.resolve() for p in book_root.rglob("*.md") if "_book" not in p.parts
    }
    broken: list[str] = []

    for path in sorted(markdown_files):
        for target in internal_links(path):
            if target not in markdown_files:
                broken.append(f"{path.relative_to(ROOT)} -> {target}")

    if broken:
        print(f"[{lang}] Broken internal links:")
        for item in broken:
            print(item)
        return 1

    seen = {p.resolve() for p in entrypoints if p.exists()}
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
        print(f"[{lang}] Unreachable markdown pages (not in README.md or SUMMARY.md):")
        for item in unreachable:
            print(item)
        return 1

    # Ensure all content files are linked in README.md
    readme_path = book_root / "README.md"
    if not readme_path.exists():
        print(f"[{lang}] Missing README.md")
        return 1
        
    readme_links = set(internal_links(readme_path))
    summary_path = book_root / "SUMMARY.md"
    content_files = markdown_files - {readme_path.resolve(), summary_path.resolve()}
    
    missing_from_readme = sorted(
        p.relative_to(ROOT).as_posix() for p in content_files if p not in readme_links
    )
    
    if missing_from_readme:
        print(f"[{lang}] Markdown pages missing from README.md index:")
        for item in missing_from_readme:
            print(item)
        return 1

    print(f"OK [{lang}]: {len(markdown_files)} markdown pages are internally linked, reachable, and indexed.")
    return 0


def main() -> int:
    exit_code = 0
    for lang in LANGS:
        if check_lang(lang) != 0:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
