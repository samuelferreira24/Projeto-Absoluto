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
echo "=== HOME DIRECTORY USAGE ==="
sudo du -x -h --max-depth=1 "$HOME" 2>/dev/null | sort -h | tail -n 30 | sed 's/^/HOME_DIR /' || true
echo "=== VAR DIRECTORY USAGE ==="
sudo du -x -h --max-depth=1 /var /var/lib /var/log 2>/dev/null | sort -h | tail -n 35 | sed 's/^/VAR_DIR /' || true
echo "=== OTHER LARGE DIRECTORIES ==="
for path in /usr/local /usr/share /opt /data /root; do
  [ -d "$path" ] && sudo du -x -h --max-depth=1 "$path" 2>/dev/null | sort -h | tail -n 12 | sed 's/^/OTHER_DIR /' || true
done
echo "=== RELEVANT SERVICES ==="
systemctl --no-pager --type=service --state=running | grep -Ei 'abs|ollama|docker|coolify|code-server|postgres|uptime|tailscale|redis|n8n|openclaw|actions.runner' | sed 's/^/SERVICE /' || true
echo "=== SERVICE UNIT DETAILS (NO ENVIRONMENT SECRETS) ==="
for unit in abs.service ollama.service docker.service openclaw-gateway.service actions.runner.samuelferreira24-Projeto-Absoluto.abs-vps-01.service actions.runner.samuelferreira24-Projeto-Absoluto.abs-vps-01-reserve.service; do
  if systemctl cat "$unit" >/dev/null 2>&1; then
    systemctl show "$unit" -p LoadState -p ActiveState -p SubState -p FragmentPath -p WorkingDirectory -p User -p ExecStart --no-pager 2>/dev/null | sed "s/^/UNIT $unit /"
  fi
done
echo "=== DOCKER CONTAINERS ==="
if command -v docker >/dev/null 2>&1; then
  sudo docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' | sed 's/^/DOCKER_CONTAINER /' || true
  echo "=== DOCKER STORAGE SUMMARY ==="
  sudo docker system df -v 2>&1 | head -n 180 | sed 's/^/DOCKER_STORAGE /' || true
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
echo "=== OLLAMA MANIFEST AUDIT (MINISTRAL ONLY) ==="
model_root="$(sudo systemctl show ollama.service -p Environment --value 2>/dev/null | tr ' ' '\n' | sed -n 's/^OLLAMA_MODELS=//p' | head -n 1)"
if [ -z "$model_root" ]; then
  for candidate in /usr/share/ollama/.ollama/models /home/ollama/.ollama/models /var/lib/ollama/.ollama/models /root/.ollama/models; do
    if sudo test -d "$candidate/manifests"; then model_root="$candidate"; break; fi
  done
fi
if [ -n "$model_root" ] && sudo test -d "$model_root/manifests"; then
  echo "OLLAMA_STORE_ROOT=$model_root"
  sudo python3 - "$model_root/manifests" <<'PYMANIFEST'
import hashlib,json,os,sys
root=sys.argv[1]
found=0
for base,dirs,files in os.walk(root):
    for name in files:
        path=os.path.join(base,name)
        rel=os.path.relpath(path,root)
        if not any(term in rel.lower() for term in ("ministral-3","llamacpp")):
            continue
        try:
            with open(path,encoding="utf-8") as f: data=json.load(f)
            layers=data.get("layers",[])
            digest=",".join(str(x.get("digest","")) for x in layers if x.get("mediaType","").endswith("model"))
            sizes=",".join(str(x.get("size","")) for x in layers if x.get("mediaType","").endswith("model"))
            manifest_sha256=hashlib.sha256(open(path,"rb").read()).hexdigest()
            print("OLLAMA_MANIFEST path=%s manifest_sha256=%s model_digest=%s model_bytes=%s" % (rel,manifest_sha256,digest,sizes))
            found+=1
        except Exception as exc:
            print("OLLAMA_MANIFEST_READ_FAIL path=%s error=%s" % (rel,type(exc).__name__))
print("OLLAMA_MANIFEST_MATCHES=%d" % found)
PYMANIFEST
else
  echo "OLLAMA_MANIFEST_AUDIT_BLOCKED: model manifest directory not identified"
fi
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
