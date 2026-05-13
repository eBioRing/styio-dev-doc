#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BOOK_ROOTS = [ROOT / "zh", ROOT / "en"]
PROHIBITED_ROOT_FILES = [ROOT / "SUMMARY.md", ROOT / "LANGS.md"]
MIRRORED_BOOK_ROOTS = (ROOT / "zh", ROOT / "en")
GITBOOK_CONFIG_NAME = ".gitbook.yaml"
GITBOOK_CONFIG_FILENAMES = {GITBOOK_CONFIG_NAME, ".gitbook.yml", "gitbook.yaml", "gitbook.yml"}
EXPECTED_GITBOOK_CONFIGS = {book_root / GITBOOK_CONFIG_NAME for book_root in BOOK_ROOTS}
IGNORED_SCAN_PARTS = {".git", "_book", ".artifacts"}

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


def strip_optional_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def normalize_config_path(value: str) -> str:
    value = strip_optional_quotes(value).strip()
    while value.startswith("./"):
        value = value[2:]
    if value in {"", "."}:
        return "."
    return value.rstrip("/")


def parse_simple_gitbook_yaml(path: Path) -> tuple[dict[str, object], list[str]]:
    config: dict[str, object] = {}
    errors: list[str] = []
    current_section: str | None = None

    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        indent_text = raw[: len(raw) - len(raw.lstrip(" "))]
        if "\t" in indent_text:
            errors.append(f"{relative_to(path, ROOT)}:{line_no} uses tabs for indentation")
            continue

        line = raw.split("#", 1)[0].rstrip()
        indent = len(line) - len(line.lstrip(" "))
        content = line.strip()

        if ":" not in content:
            errors.append(f"{relative_to(path, ROOT)}:{line_no} is not a key/value entry")
            continue

        key, raw_value = content.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        if indent == 0:
            if value:
                config[key] = strip_optional_quotes(value)
                current_section = None
            else:
                config[key] = {}
                current_section = key
            continue

        if indent == 2 and current_section:
            section = config.get(current_section)
            if not isinstance(section, dict):
                errors.append(f"{relative_to(path, ROOT)}:{line_no} cannot add nested value under {current_section}")
                continue
            section[key] = strip_optional_quotes(value)
            continue

        errors.append(f"{relative_to(path, ROOT)}:{line_no} has unsupported indentation")

    return config, errors


def gitbook_config_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name not in GITBOOK_CONFIG_FILENAMES:
            continue
        if any(part in IGNORED_SCAN_PARTS for part in path.parts):
            continue
        files.append(path)
    return files


def check_gitbook_configs() -> list[str]:
    errors: list[str] = []
    found = {path.resolve() for path in gitbook_config_files()}
    expected = {path.resolve() for path in EXPECTED_GITBOOK_CONFIGS}

    for path in sorted(expected - found):
        errors.append(f"{relative_to(path, ROOT)} is required for the GitBook Project directory")

    for path in sorted(found - expected):
        if path.name == GITBOOK_CONFIG_NAME:
            errors.append(
                f"{relative_to(path, ROOT)} is not allowed; .gitbook.yaml must live directly under zh/ and en/"
            )
        else:
            errors.append(
                f"{relative_to(path, ROOT)} is not allowed; GitBook configuration must be named .gitbook.yaml"
            )

    for path in sorted(expected & found):
        config, parse_errors = parse_simple_gitbook_yaml(path)
        errors.extend(parse_errors)

        if "root" not in config:
            errors.append(f"{relative_to(path, ROOT)} must set root: ./")
        root = normalize_config_path(str(config.get("root", "")))
        if "root" in config and root != ".":
            errors.append(f"{relative_to(path, ROOT)} must set root: ./")

        structure = config.get("structure")
        if not isinstance(structure, dict):
            errors.append(f"{relative_to(path, ROOT)} must define structure.readme and structure.summary")
            continue

        readme = normalize_config_path(str(structure.get("readme", "")))
        summary = normalize_config_path(str(structure.get("summary", "")))
        if readme != "README.md":
            errors.append(f"{relative_to(path, ROOT)} must set structure.readme: README.md")
        if summary != "SUMMARY.md":
            errors.append(f"{relative_to(path, ROOT)} must set structure.summary: SUMMARY.md")

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

    errors.extend(check_gitbook_configs())

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
