#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
RUN_AS_USER="${RUN_AS_USER:-$USER}"
RUN_AS_GROUP="${RUN_AS_GROUP:-$(id -gn "$RUN_AS_USER")}"
UNIT_DIR="${UNIT_DIR:-/etc/systemd/system}"
SERVICE_NAME="hardware-deal-radar"

if [[ "${EUID:-$(id -u)}" -eq 0 ]]; then
  SUDO=""
else
  SUDO="sudo"
fi

tmp_service="$(mktemp)"
tmp_timer="$(mktemp)"
trap 'rm -f "$tmp_service" "$tmp_timer"' EXIT

sed \
  -e "s|__RADAR_APP_DIR__|$APP_DIR|g" \
  -e "s|__RADAR_USER__|$RUN_AS_USER|g" \
  -e "s|__RADAR_GROUP__|$RUN_AS_GROUP|g" \
  "$APP_DIR/scripts/systemd/hardware-deal-radar.service" > "$tmp_service"

cp "$APP_DIR/scripts/systemd/hardware-deal-radar.timer" "$tmp_timer"

$SUDO install -m 0644 "$tmp_service" "$UNIT_DIR/$SERVICE_NAME.service"
$SUDO install -m 0644 "$tmp_timer" "$UNIT_DIR/$SERVICE_NAME.timer"
$SUDO systemctl daemon-reload
$SUDO systemctl enable --now "$SERVICE_NAME.timer"
$SUDO systemctl status "$SERVICE_NAME.timer" --no-pager
