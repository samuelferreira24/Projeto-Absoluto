#!/usr/bin/env bash
# Controlled finalizer for the six local ABS models. Fixed allowlist; no user shell input.
set -uo pipefail
export HOME=/home/absadmin
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
cd "$HOME/Projeto-Absoluto" || exit 2
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup="$HOME/abs-local-ai-operation-backups/finalize-$stamp"
mkdir -p "$backup"
log="$backup/finalize.log"
exec > >(tee -a "$log") 2>&1
echo "ABS_LOCAL_AI_FINALIZE_BEGIN $stamp"
free -h
df -h /
curl -fsS --max-time 10 http://127.0.0.1:8787/health || true
curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags > "$backup/tags-before.json" || { echo "BLOCKED ollama_api_unavailable"; exit 2; }
ollama list | tee "$backup/ollama-list-before.txt"
sudo systemctl cat abs.service > "$backup/abs-service.before.txt" 2>&1 || true
if [ ! -f /etc/abs-local-models.env ]; then echo "BLOCKED config_backup_missing"; exit 3; fi
sudo cp -a /etc/abs-local-models.env "$backup/abs-local-models.env.before"
sudo systemctl show abs.service -p Environment -p EnvironmentFiles > "$backup/abs-env.before.txt" 2>&1 || true

restart_ollama() {
  active="$(curl -fsS --max-time 5 http://127.0.0.1:11434/api/ps 2>&1)" || { echo "OLLAMA_RECOVERY_FAIL api_ps_unavailable"; return 1; }
  printf '%s' "$active" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert not d.get("models"), d' >/dev/null 2>&1 || { echo "OLLAMA_RECOVERY_BLOCKED active_model_present"; return 1; }
  sudo systemctl restart ollama.service || { echo "OLLAMA_RECOVERY_FAIL service_restart"; return 1; }
  sleep 4
  curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags >/dev/null || { echo "OLLAMA_RECOVERY_FAIL api_not_ready"; return 1; }
  printf 'OLLAMA_RECOVERY_PASS available_mb='
  awk '/MemAvailable:/ {print int($2/1024)}' /proc/meminfo
  return 0
}
assert_unloaded() {
  active="$(curl -fsS --max-time 5 http://127.0.0.1:11434/api/ps 2>&1)" || { echo "UNLOAD_FAIL api_ps_unavailable"; return 1; }
  printf '%s' "$active" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert not d.get("models"), d; print("UNLOAD_PASS models=[]")'
}
min_memory() { awk '/MemAvailable:/ {print int($2/1024)}' /proc/meminfo; }

# Test multimodal input first, while the VPS is near its baseline memory state.
vision_pass=0
echo "=== GEMMA VISION FIRST ==="
if ! ollama list | awk 'NR>1 {print $1}' | grep -Fxq 'hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S'; then
  echo "VISION_RESULT FAIL model=gemma-e2b-q3 reason=tag_not_installed"
else
  avail="$(min_memory)"
  if [ "$avail" -lt 3000 ]; then
    restart_ollama || true
    avail="$(min_memory)"
  fi
  if [ "$avail" -lt 3000 ]; then
    echo "VISION_RESULT BLOCKED_MEMORY available_mb=$avail required_mb=3000"
  else
    image_b64="$(python3 - <<'PY'
import base64,struct,zlib
def chunk(kind,data): return struct.pack(">I",len(data))+kind+data+struct.pack(">I",zlib.crc32(kind+data)&0xffffffff)
w=h=16
raw=b"".join(b"\x00"+(b"\xff\x00\x00\xff"*w) for _ in range(h))
png=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))+chunk(b"IDAT",zlib.compress(raw))+chunk(b"IEND",b"")
print(base64.b64encode(png).decode())
PY
)"
    payload="$(python3 - "$image_b64" <<'PY'
import json,sys
print(json.dumps({"model":"hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S","messages":[{"role":"user","content":"Inspect the attached image. If its dominant color is red, reply exactly ABS_GEMMA_VISION_OK; otherwise reply NO.","images":[sys.argv[1]]}],"stream":False,"think":False,"keep_alive":0,"options":{"num_ctx":2048,"num_predict":32,"temperature":0}}))
PY
)"
    response="$(curl -sS --max-time 240 http://127.0.0.1:11434/api/chat -H 'Content-Type: application/json' -d "$payload" 2>&1)"
    rc=$?
    if [ "$rc" -eq 0 ] && printf '%s' "$response" | python3 -c 'import json,sys; d=json.load(sys.stdin); s=((d.get("message") or {}).get("content") or "").upper(); assert "ABS_GEMMA_VISION_OK" in s, s; print("vision_response="+s[:100])' && assert_unloaded; then
      vision_pass=1; echo "VISION_RESULT PASS model=gemma-e2b-q3"
    else
      echo "VISION_RESULT FAIL model=gemma-e2b-q3 curl_rc=$rc detail=$(printf '%s' "$response" | head -c 500)"
    fi
  fi
fi
if [ "$vision_pass" -ne 1 ]; then
  echo "STOP_NO_CONFIG_CHANGE reason=vision_not_proven"
  echo "FINAL_STATE"; free -h; df -h /; echo "BACKUP_DIR=$backup"; echo "ABS_LOCAL_AI_FINALIZE_END"; exit 4
fi
restart_ollama || { echo "STOP_NO_CONFIG_CHANGE reason=ollama_recovery_failed"; exit 5; }

direct_pass=0
direct_fail=0
test_model() {
  model="$1"; marker="$2"; min_mb="$3"; timeout_s="$4"
  echo "--- DIRECT $model ---"
  if ! ollama list | awk 'NR>1 {print $1}' | grep -Fxq "$model"; then echo "DIRECT_RESULT FAIL model=$model reason=not_installed"; direct_fail=$((direct_fail+1)); return; fi
  avail="$(min_memory)"
  if [ "$avail" -lt "$min_mb" ]; then echo "DIRECT_RESULT FAIL model=$model reason=memory available_mb=$avail required_mb=$min_mb"; direct_fail=$((direct_fail+1)); return; fi
  payload="$(python3 - "$model" "$marker" <<'PY'
import json,sys
print(json.dumps({"model":sys.argv[1],"prompt":"Reply with exactly "+sys.argv[2]+" and nothing else.","stream":False,"think":False,"keep_alive":0,"options":{"num_ctx":2048,"num_predict":40,"temperature":0}}))
PY
)"
  response="$(curl -sS --max-time "$timeout_s" http://127.0.0.1:11434/api/generate -H 'Content-Type: application/json' -d "$payload" 2>&1)"
  rc=$?
  if [ "$rc" -eq 0 ] && printf '%s' "$response" | python3 -c 'import json,sys; d=json.load(sys.stdin); marker=sys.argv[1].upper(); s=(d.get("response") or "").upper(); assert marker in s, s; print("response="+s[:100])' "$marker" && assert_unloaded; then
    direct_pass=$((direct_pass+1)); echo "DIRECT_RESULT PASS model=$model"
  else
    direct_fail=$((direct_fail+1)); echo "DIRECT_RESULT FAIL model=$model curl_rc=$rc detail=$(printf '%s' "$response" | head -c 400)"
  fi
  restart_ollama || direct_fail=$((direct_fail+1))
}
test_model 'qwen3.5:0.8b' 'ABS_QWEN08_OK' 1200 90
test_model 'qwen3.5:2b' 'ABS_QWEN2B_OK' 2600 150
test_model 'qwen3.5:4b' 'ABS_QWEN4B_OK' 3400 240
test_model 'ministral-3:3b' 'ABS_MINISTRAL3B_OK' 3000 240
test_model 'hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S' 'ABS_GEMMA_E2B_Q3_OK' 3200 240
test_model 'phi4-mini:3.8b' 'ABS_PHI4MINI_OK' 3200 240
echo "DIRECT_SUMMARY pass=$direct_pass fail=$direct_fail"

tool_pass=0
echo "=== MINISTRAL STRUCTURED TOOL CALL ==="
avail="$(min_memory)"
if [ "$avail" -ge 3000 ]; then
  payload="$(python3 - <<'PY'
import json
print(json.dumps({"model":"ministral-3:3b","messages":[{"role":"user","content":"You must call record_test, not answer directly. Use marker ABS_MINISTRAL_TOOL_OK."}],"tools":[{"type":"function","function":{"name":"record_test","description":"Record a local capability validation marker.","parameters":{"type":"object","properties":{"marker":{"type":"string"}},"required":["marker"]}}}],"stream":False,"think":False,"keep_alive":0,"options":{"num_ctx":2048,"num_predict":96,"temperature":0}}))
PY
)"
  response="$(curl -sS --max-time 240 http://127.0.0.1:11434/api/chat -H 'Content-Type: application/json' -d "$payload" 2>&1)"
  if printf '%s' "$response" | python3 -c 'import json,sys; d=json.load(sys.stdin); calls=(d.get("message") or {}).get("tool_calls") or []; assert any((x.get("function") or {}).get("name")=="record_test" and ((x.get("function") or {}).get("arguments") or {}).get("marker")=="ABS_MINISTRAL_TOOL_OK" for x in calls), d; print("tool_call=record_test marker=ABS_MINISTRAL_TOOL_OK")' && assert_unloaded; then tool_pass=1; echo "TOOL_RESULT PASS model=ministral-3:3b"; else echo "TOOL_RESULT FAIL model=ministral-3:3b detail=$(printf '%s' "$response" | head -c 400)"; fi
else
  echo "TOOL_RESULT BLOCKED_MEMORY available_mb=$avail required_mb=3000"
fi
restart_ollama || true

if [ "$direct_pass" -ne 6 ] || [ "$direct_fail" -ne 0 ] || [ "$tool_pass" -ne 1 ] || [ "$vision_pass" -ne 1 ]; then
  echo "STOP_NO_CONFIG_CHANGE direct=$direct_pass/6 tool=$tool_pass vision=$vision_pass"
  free -h; df -h /; echo "BACKUP_DIR=$backup"; echo "ABS_LOCAL_AI_FINALIZE_END"; exit 6
fi

echo "=== APPLY SIX-MODEL CONFIG WITH ROLLBACK ==="
sudo tee /etc/abs-local-models.env >/dev/null <<'ENV'
ABS_LOCAL_AI_MODELS=qwen3.5-0.8b|http://127.0.0.1:11434|qwen3.5:0.8b,qwen3.5-2b|http://127.0.0.1:11434|qwen3.5:2b,qwen3.5-4b|http://127.0.0.1:11434|qwen3.5:4b,ministral-3b|http://127.0.0.1:11434|ministral-3:3b,gemma4-e2b-q3|http://127.0.0.1:11434|hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S,phi4-mini-3.8b|http://127.0.0.1:11434|phi4-mini:3.8b
ABS_LOCAL_AI_URL=http://127.0.0.1:11434
ABS_LOCAL_AI_MODEL=qwen3.5:0.8b
ABS_LOCAL_AI_MAX_TOKENS=64
ABS_LOCAL_AI_TEMPERATURE=0
ABS_LOCAL_AI_THINK=false
ENV
sudo systemctl restart abs.service || { sudo cp -a "$backup/abs-local-models.env.before" /etc/abs-local-models.env; sudo systemctl restart abs.service; echo "ROLLBACK service_restart_failed"; exit 7; }
sleep 4
integration_pass=0
integration_fail=0
test_abs_model() {
  cap="$1"; marker="$2"; min_mb="$3"
  restart_ollama || { echo "ABS_INTEGRATION_FAIL capability=$cap reason=ollama_recovery_failed"; integration_fail=$((integration_fail+1)); return; }
  avail="$(min_memory)"
  if [ "$avail" -lt "$min_mb" ]; then echo "ABS_INTEGRATION_FAIL capability=$cap reason=memory available_mb=$avail required_mb=$min_mb"; integration_fail=$((integration_fail+1)); return; fi
  payload="$(python3 - "$cap" "$marker" <<'PY'
import json,sys
print(json.dumps({"message":"Reply with exactly "+sys.argv[2]+" and nothing else.","approved":True,"context":{"capability_id":"local-ai:"+sys.argv[1],"max_tokens":24,"temperature":0,"think":False,"keep_alive":0,"timeout":170}}))
PY
)"
  response="$(curl -sS --max-time 180 -X POST http://127.0.0.1:8787/chat -H 'Content-Type: application/json' -d "$payload" 2>&1)"
  if printf '%s' "$response" | python3 -c 'import json,sys; d=json.load(sys.stdin); cap=sys.argv[1]; marker=sys.argv[2].upper(); p=d.get("provenance") or []; p=p if isinstance(p,list) else [p]; resource=d.get("resource") or {}; assert d.get("work_state")=="completed", d; assert marker in str(d.get("response","")).upper(), d; assert resource.get("capability_id")=="local-ai:"+cap or any(isinstance(x,dict) and x.get("capability_id")=="local-ai:"+cap for x in p), d; print("ABS_INTEGRATION_PASS "+cap)' "$cap" "$marker" && assert_unloaded; then
    integration_pass=$((integration_pass+1)); echo "ABS_INTEGRATION_PASS capability=$cap"
  else
    integration_fail=$((integration_fail+1)); echo "ABS_INTEGRATION_FAIL capability=$cap detail=$(printf '%s' "$response" | head -c 700)"
  fi
}
test_abs_model 'qwen3.5-0.8b' 'ABS_QWEN08_OK' 2568
test_abs_model 'qwen3.5-2b' 'ABS_QWEN2B_OK' 3768
test_abs_model 'qwen3.5-4b' 'ABS_QWEN4B_OK' 4018
test_abs_model 'ministral-3b' 'ABS_MINISTRAL3B_OK' 4018
test_abs_model 'gemma4-e2b-q3' 'ABS_GEMMA_E2B_Q3_OK' 3968
test_abs_model 'phi4-mini-3.8b' 'ABS_PHI4MINI_OK' 3668
echo "ABS_INTEGRATION_SUMMARY pass=$integration_pass fail=$integration_fail"
if [ "$integration_pass" -ne 6 ] || [ "$integration_fail" -ne 0 ]; then
  sudo cp -a "$backup/abs-local-models.env.before" /etc/abs-local-models.env
  sudo systemctl restart abs.service
  sleep 3
  echo "ROLLBACK_CONFIG_RESTORED"
  exit 8
fi
echo "CLEANUP_DEFERRED: only the exact-digest Ministral alias was removed; other variants kept because the VPS has <4 GB free and full weight rollback copies cannot be guaranteed"
echo "FINAL_HEALTH"; curl -fsS --max-time 10 http://127.0.0.1:8787/health || true
curl -fsS --max-time 10 http://127.0.0.1:8787/v3/status || true
free -h; df -h /
echo "BACKUP_DIR=$backup"
echo "ABS_LOCAL_AI_FINALIZE_END"
