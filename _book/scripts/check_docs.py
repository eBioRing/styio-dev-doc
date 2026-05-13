#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ENTRYPOINTS = [ROOT / "README.md", ROOT / "SUMMARY.md"]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def internal_links(path: Path) -> list[Path]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
        
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
    # Collect all markdown files in zh and en
    markdown_files = {
        p.resolve() for p in ROOT.rglob("*.md") 
        if "_book" not in p.parts and (".git" not in p.parts)
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

    seen = {p.resolve() for p in ENTRYPOINTS if p.exists()}
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
    
    # Filter out GEMINI.md and LICENSE etc if they are not meant to be in the book
    unreachable = [p for p in unreachable if p not in ["GEMINI.md", "LICENSE.md", "README.md", "SUMMARY.md"]]
    
    if unreachable:
        print("Unreachable markdown pages (not linked from root README.md or SUMMARY.md):")
        for item in unreachable:
            print(item)
        return 1

    print(f"OK: {len(markdown_files)} markdown pages are internally linked and reachable from root.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
