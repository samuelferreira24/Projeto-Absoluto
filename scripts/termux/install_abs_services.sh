#!/data/data/com.termux/files/usr/bin/bash
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

"$SCRIPT_DIR/install_abs_service.sh"
"$SCRIPT_DIR/install_abs_updater_service.sh"

if command -v sv-enable >/dev/null 2>&1; then
  sv-enable abs || true
fi
if command -v sv >/dev/null 2>&1; then
  sv up abs || true
  sv up abs-updater || true
fi

echo "ABS services installed and started."
echo "  abs         = ABS runtime"
echo "  abs-updater = autonomous update supervisor"
