#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
UV_BIN="${UV_BIN:-$HOME/.local/bin/uv}"

cd "$APP_DIR"

if [[ ! -x "$UV_BIN" ]]; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

"$UV_BIN" sync --extra dev
mkdir -p data

for example in config/*.example.yaml; do
  target="${example%.example.yaml}.yaml"
  if [[ ! -f "$target" ]]; then
    cp "$example" "$target"
  fi
done

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

chmod 600 .env

echo "VPS bootstrap complete in $APP_DIR"
