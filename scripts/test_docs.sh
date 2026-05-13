#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WITH_BROWSER=0
PORT="${DOCS_TEST_PORT:-4173}"
BUILD_DIR="${ROOT}/.artifacts/docs-build"
SMOKE_DIR="${ROOT}/.artifacts/docs-smoke"

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

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

npx --yes honkit build zh "$BUILD_DIR/zh"
npx --yes honkit build en "$BUILD_DIR/en"

test -f "$BUILD_DIR/zh/index.html"
test -f "$BUILD_DIR/zh/interfaces/core-interfaces.html"
grep -q "Styio 维护者手册" "$BUILD_DIR/zh/index.html"

test -f "$BUILD_DIR/en/index.html"
test -f "$BUILD_DIR/en/ecosystem/repository-matrix.html"
grep -q "Styio Maintainer Manual" "$BUILD_DIR/en/index.html"

if [[ "$WITH_BROWSER" -eq 1 ]]; then
  rm -rf "$SMOKE_DIR"
  npx --yes playwright install chromium
  python3 -m http.server "$PORT" --directory "$BUILD_DIR" >"$ROOT/.tmp-doc-server.log" 2>&1 &
  SERVER_PID=$!
  trap 'kill "$SERVER_PID" >/dev/null 2>&1 || true' EXIT
  sleep 2
  mkdir -p "$SMOKE_DIR"

  npx --yes playwright screenshot --browser=chromium "http://127.0.0.1:${PORT}/zh/" "$SMOKE_DIR/zh-home.png"
  npx --yes playwright screenshot --browser=chromium "http://127.0.0.1:${PORT}/en/" "$SMOKE_DIR/en-home.png"

  test -f "$SMOKE_DIR/zh-home.png"
  test -f "$SMOKE_DIR/en-home.png"

  kill "$SERVER_PID" >/dev/null 2>&1 || true
  wait "$SERVER_PID" 2>/dev/null || true
  trap - EXIT
fi

echo "OK: separate zh/en GitBook checks passed."
