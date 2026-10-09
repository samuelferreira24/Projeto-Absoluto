#!/usr/bin/env bash
# Read-only VPS inventory for a safe, evidence-based cleanup.
set -uo pipefail
export HOME=/home/absadmin
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup="$HOME/abs-vps-inventory/$stamp"
mkdir -p "$backup"
log="$backup/inventory.log"
exec > >(tee -a "$log") 2>&1
echo "ABS_VPS_INVENTORY_BEGIN $stamp"
echo "=== HOST ==="
hostname
date -Is
uptime
free -h
df -h /
echo "=== TOP-LEVEL DISK USAGE ==="
sudo du -x -h --max-depth=1 / 2>/dev/null | sort -h | tail -n 18 | sed 's/^/DISK_DIR /' || true
echo "=== RELEVANT SERVICES ==="
systemctl --no-pager --type=service --state=running | grep -Ei 'abs|ollama|docker|coolify|code-server|postgres|uptime|tailscale|redis|n8n' | sed 's/^/SERVICE /' || true
echo "=== DOCKER CONTAINERS ==="
if command -v docker >/dev/null 2>&1; then
  docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' | sed 's/^/DOCKER_CONTAINER /' || true
  echo "=== DOCKER STORAGE SUMMARY ==="
  docker system df -v 2>&1 | head -n 180 | sed 's/^/DOCKER_STORAGE /' || true
else
  echo "DOCKER_NOT_INSTALLED"
fi
echo "=== OLLAMA MODELS WITH DIGESTS ==="
curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags > "$backup/ollama-tags.json" || {
  echo "OLLAMA_API_UNAVAILABLE"
  exit 3
}
python3 - "$backup/ollama-tags.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
for m in d.get("models",[]):
    print("MODEL name=%s digest=%s size=%s modified=%s" % (
        m.get("name",""),m.get("digest",""),m.get("size",""),m.get("modified_at","")))
PY
echo "=== ACTIVE OLLAMA MODELS ==="
curl -fsS --max-time 5 http://127.0.0.1:11434/api/ps || true
echo
echo "=== ABS LOCAL MODEL CONFIG REFERENCES (NAMES ONLY) ==="
if sudo test -r /etc/abs-local-models.env; then
  sudo cat /etc/abs-local-models.env | python3 -c '
import sys
for line in sys.stdin:
    if line.startswith("ABS_LOCAL_AI_MODELS="):
        for spec in line.strip().split("=",1)[1].split(","):
            p=spec.split("|")
            if len(p)==3:
                print("CONFIG_MODEL id=%s tag=%s" % (p[0],p[2]))
    elif line.startswith("ABS_LOCAL_AI_MODEL="):
        print("CONFIG_DEFAULT_TAG="+line.strip().split("=",1)[1])
    elif line.startswith("ABS_LOCAL_AI_URL="):
        print("CONFIG_ENDPOINT="+line.strip().split("=",1)[1])
'
else
  echo "CONFIG_MISSING_OR_UNREADABLE"
fi
echo "=== ABS HEALTH AND V3 STATUS ==="
curl -fsS --max-time 10 http://127.0.0.1:8787/health || true
echo
curl -fsS --max-time 10 http://127.0.0.1:8787/v3/status || true
echo
echo "=== REPOSITORY STATUS ==="
cd "$HOME/Projeto-Absoluto" && git status --short --branch 2>&1 || true
echo "BACKUP_DIR=$backup"
echo "LOG=$log"
echo "ABS_VPS_INVENTORY_END"
