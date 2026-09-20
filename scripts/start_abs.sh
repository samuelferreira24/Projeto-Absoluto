#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")/.."
export ABS_HOST="${ABS_HOST:-127.0.0.1}"
export ABS_PORT="${ABS_PORT:-8787}"
export ABS_AUTO_UPDATE="${ABS_AUTO_UPDATE:-1}"
export ABS_UPDATE_INTERVAL="${ABS_UPDATE_INTERVAL:-60}"
exec python -m abs_core.local
