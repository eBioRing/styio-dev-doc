#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT"
echo "Running full GitBook gate for separate zh/en spaces."
exec "$ROOT/scripts/test_docs.sh" --with-browser
