#!/usr/bin/env bash
# deploy.sh — rsync demos/ to VPS or a Netlify/Cloudflare manual deploy.
# Called by run.py after demos are built. Set VPS_DEPLOY_TARGET in .env.
set -euo pipefail

DEMOS_DIR="$(cd "$(dirname "$0")/demos" && pwd)"
TARGET="${VPS_DEPLOY_TARGET:-}"

if [[ -z "$TARGET" ]]; then
  echo "[deploy] VPS_DEPLOY_TARGET not set — skipping remote deploy."
  echo "[deploy] Demos available locally at $DEMOS_DIR"
  exit 0
fi

echo "[deploy] Syncing $DEMOS_DIR → $TARGET"
rsync -avz --delete "$DEMOS_DIR/" "$TARGET/"
echo "[deploy] Done."
