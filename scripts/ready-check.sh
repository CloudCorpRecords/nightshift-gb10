#!/usr/bin/env bash
# NightShift readiness gate — run on the GB10 before any demo or live run.
# Prints GO / NO-GO. Checks: endpoint answers, model id is qwen36, and a
# real 1-token completion succeeds WITH the API key (catches the 401 trap
# Bino flagged: a keyed vLLM makes an unkeyed client silently fall back).
set -u
URL="${NIGHTSHIFT_MODEL_URL:-http://localhost:8000/v1}"
KEY_FILE="${NIGHTSHIFT_MODEL_KEY_FILE:-$HOME/Downloads/vllm-api-key.txt}"
AUTH=()
if [ -f "$KEY_FILE" ]; then
  AUTH=(-H "Authorization: Bearer $(cat "$KEY_FILE")")
fi

echo "== models =="
MODELS=$(curl -s --max-time 10 "${AUTH[@]}" "$URL/models") || { echo "NO-GO: endpoint unreachable"; exit 1; }
echo "$MODELS" | head -c 300; echo
echo "$MODELS" | grep -q "qwen36" || { echo "NO-GO: qwen36 not served"; exit 1; }

echo "== completion probe =="
RESP=$(curl -s --max-time 60 "${AUTH[@]}" "$URL/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen36","messages":[{"role":"user","content":"Reply with one word: ready"}],"max_tokens":8,"temperature":0}')
echo "$RESP" | head -c 300; echo
echo "$RESP" | grep -q '"content"' || { echo "NO-GO: completion failed (auth? warm-up?) — check vLLM log"; exit 1; }
echo "GO: model endpoint is live, keyed, and answering."
