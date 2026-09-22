#!/data/data/com.termux/files/usr/bin/bash
set -eu

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
REPO_DIR="${ABS_REPO_DIR:-$HOME/Projeto-Absoluto}"
SERVICE_DIR="$PREFIX/var/service/abs-updater"

mkdir -p "$SERVICE_DIR/log"

cat > "$SERVICE_DIR/run" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -eu
REPO_DIR="${ABS_REPO_DIR:-$HOME/Projeto-Absoluto}"
cd "$REPO_DIR"
export ABS_REPO_DIR="$REPO_DIR"
export ABS_UPDATE_INTERVAL="${ABS_UPDATE_INTERVAL:-60}"
exec python -m abs_core.update_daemon
EOF

cat > "$SERVICE_DIR/log/run" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -eu
mkdir -p "$HOME/.abs/log"
exec svlogd "$HOME/.abs/log"
EOF

chmod +x "$SERVICE_DIR/run" "$SERVICE_DIR/log/run"

if command -v sv-enable >/dev/null 2>&1; then
  sv-enable abs-updater || true
fi
if command -v sv >/dev/null 2>&1; then
  sv up abs-updater || true
fi

echo "ABS updater service installed at: $SERVICE_DIR"
echo "Repository: $REPO_DIR"
echo "Interval: ${ABS_UPDATE_INTERVAL:-60}s"
