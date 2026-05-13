#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT"
echo "Running full GitBook gate: links, reachability, HonKit build, browser smoke test."
exec "$ROOT/scripts/test_docs.sh" --with-browser
