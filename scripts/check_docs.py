#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BOOK_ROOTS = [ROOT / "zh", ROOT / "en"]
PROHIBITED_ROOT_FILES = [ROOT / "SUMMARY.md", ROOT / "LANGS.md"]
MIRRORED_BOOK_ROOTS = (ROOT / "zh", ROOT / "en")

LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)]+)\)")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
EXTERNAL_PREFIXES = ("http://", "https://", "#", "mailto:", "tel:")


def clean_target(raw: str) -> str:
    target = raw.strip()
    for marker in ("#", "?"):
        if marker in target:
            target = target.split(marker, 1)[0]
    return target.strip()


def internal_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    text = FENCED_CODE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)

    links: list[str] = []
    for match in LINK_RE.finditer(text):
        target = clean_target(match.group(1))
        if not target or target.startswith(EXTERNAL_PREFIXES):
            continue
        links.append(target)
    return links


def markdown_files(book_root: Path) -> set[Path]:
    return {
        path.resolve()
        for path in book_root.rglob("*.md")
        if "_book" not in path.parts and ".git" not in path.parts
    }


def relative_to(path: Path, base: Path) -> str:
    return path.relative_to(base).as_posix()


def is_inside(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
    except ValueError:
        return False
    return True


def check_book(book_root: Path) -> list[str]:
    errors: list[str] = []
    entrypoints = [book_root / "README.md", book_root / "SUMMARY.md"]

    for entrypoint in entrypoints:
        if not entrypoint.is_file():
            errors.append(f"{relative_to(entrypoint, ROOT)} is required")

    files = markdown_files(book_root)
    for path in sorted(files):
        for link in internal_links(path):
            target = (path.parent / link).resolve()
            source = relative_to(path, ROOT)

            if not is_inside(target, book_root.resolve()):
                errors.append(f"{source} links outside its GitBook root: {link}")
                continue

            if target.suffix == ".md":
                if target not in files:
                    errors.append(f"{source} links to missing markdown: {link}")
            elif not target.exists():
                errors.append(f"{source} links to missing asset: {link}")

    seen = {entrypoint.resolve() for entrypoint in entrypoints if entrypoint.exists()}
    stack = list(seen)

    while stack:
        path = stack.pop()
        for link in internal_links(path):
            target = (path.parent / link).resolve()
            if target in files and target not in seen:
                seen.add(target)
                stack.append(target)

    unreachable = sorted(relative_to(path, ROOT) for path in files if path not in seen)
    if unreachable:
        errors.append(
            f"{relative_to(book_root, ROOT)} has unreachable markdown pages: "
            + ", ".join(unreachable)
        )

    return errors


def check_mirrored_markdown_paths(left: Path, right: Path) -> list[str]:
    errors: list[str] = []
    left_files = {relative_to(path, left) for path in markdown_files(left)}
    right_files = {relative_to(path, right) for path in markdown_files(right)}

    missing_in_right = sorted(left_files - right_files)
    if missing_in_right:
        errors.append(
            f"{relative_to(right, ROOT)} is missing markdown pages mirrored from {relative_to(left, ROOT)}: "
            + ", ".join(missing_in_right)
        )

    missing_in_left = sorted(right_files - left_files)
    if missing_in_left:
        errors.append(
            f"{relative_to(left, ROOT)} is missing markdown pages mirrored from {relative_to(right, ROOT)}: "
            + ", ".join(missing_in_left)
        )

    return errors


def main() -> int:
    errors: list[str] = []

    for path in PROHIBITED_ROOT_FILES:
        if path.exists():
            errors.append(
                f"{relative_to(path, ROOT)} is not allowed; GitBook spaces must sync zh/ and en/ separately"
            )

    for book_root in BOOK_ROOTS:
        if not book_root.is_dir():
            errors.append(f"{relative_to(book_root, ROOT)} directory is required")
            continue
        errors.extend(check_book(book_root))

    if all(book_root.is_dir() for book_root in MIRRORED_BOOK_ROOTS):
        errors.extend(check_mirrored_markdown_paths(*MIRRORED_BOOK_ROOTS))

    if errors:
        print("Docs gate failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    total = sum(len(markdown_files(book_root)) for book_root in BOOK_ROOTS)
    print(f"OK: zh and en GitBook roots are separate, linked, and reachable ({total} markdown pages).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
