#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WITH_BROWSER=0
PORT="${DOCS_TEST_PORT:-4173}"
ARTIFACT_DIR="${ROOT}/.artifacts/docs-smoke"

for arg in "$@"; do
  case "$arg" in
    --with-browser)
      WITH_BROWSER=1
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      exit 2
      ;;
  esac
done

cd "$ROOT"

python3 scripts/check_docs.py

rm -rf en/_book en/en/_book
npx --yes honkit build en _book

test -f en/_book/index.html
test -f en/_book/search_index.json

if [[ "$WITH_BROWSER" -eq 1 ]]; then
  rm -rf "$ARTIFACT_DIR"
  npx --yes playwright install chromium
  python3 -m http.server "$PORT" --directory "$ROOT/en/_book" >"$ROOT/.tmp-doc-server.log" 2>&1 &
  SERVER_PID=$!
  trap 'kill "$SERVER_PID" >/dev/null 2>&1 || true' EXIT
  sleep 2
  mkdir -p "$ARTIFACT_DIR"

  test -f en/_book/index.html
  test -f en/_book/interfaces/core-interfaces.html
  test -f en/_book/standards/testing-and-regression.html

  rg -q "Styio 维护者手册" en/_book/index.html
  rg -q "核心接口总览" en/_book/interfaces/core-interfaces.html
  rg -q "测试与回归策略" en/_book/standards/testing-and-regression.html

  npx --yes playwright screenshot --browser=chromium "http://127.0.0.1:${PORT}" "$ARTIFACT_DIR/home.png"

  test -f "$ARTIFACT_DIR/home.png"

  kill "$SERVER_PID" >/dev/null 2>&1 || true
  wait "$SERVER_PID" 2>/dev/null || true
  trap - EXIT
fi

echo "OK: docs checks passed."
