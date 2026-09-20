#!/data/data/com.termux/files/usr/bin/bash
set -eu

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"

# Start the Termux service supervisor when Android boots.
if [ -f "$PREFIX/etc/profile.d/start-services.sh" ]; then
  . "$PREFIX/etc/profile.d/start-services.sh"
fi
