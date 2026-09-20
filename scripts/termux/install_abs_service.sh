#!/data/data/com.termux/files/usr/bin/bash
set -eu

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
SERVICE_DIR="$PREFIX/var/service/abs"
REPO_DIR="${ABS_REPO_DIR:-$HOME/Projeto-Absoluto}"

mkdir -p "$SERVICE_DIR/log"

cat > "$SERVICE_DIR/run" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -eu
REPO_DIR="${ABS_REPO_DIR:-$HOME/Projeto-Absoluto}"
cd "$REPO_DIR"
exec python -m abs_core.local
EOF

cat > "$SERVICE_DIR/log/run" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
set -eu
mkdir -p "$HOME/.abs/log"
exec svlogd "$HOME/.abs/log"
EOF

chmod +x "$SERVICE_DIR/run" "$SERVICE_DIR/log/run"

echo "ABS service installed at: $SERVICE_DIR"
echo "Repository: $REPO_DIR"
echo
echo "Next:"
echo "  sv-enable abs"
echo "  sv up abs"
echo "  sv status abs"
