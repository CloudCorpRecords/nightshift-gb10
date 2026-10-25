#!/usr/bin/env bash
# NightShift model watchdog — keeps the demo honest, not heroic.
# Polls the local vLLM endpoint; writes a one-line status file the demo
# operator (or the brief) can glance at; optionally restarts the server
# if you set SERVE_CMD to the box's serve command. It never invents a
# restart command on its own — Russ's auto-serve owns starting vLLM.
#
# Usage on the GB10:
#   tmux new -s watchdog 'bash scripts/model-keepalive.sh'
# Status: ~/nightshift-ops/status.txt  Log: ~/nightshift-ops/watchdog.log
set -u
URL="${NIGHTSHIFT_MODEL_URL:-http://localhost:8000/v1}"
OPS="$HOME/nightshift-ops"; mkdir -p "$OPS"
SERVE_CMD="${SERVE_CMD:-}"   # e.g. SERVE_CMD='bash ~/bin/start-vllm.sh'
FAILS=0
echo "$(date +%T) watchdog up (url=$URL serve_cmd=${SERVE_CMD:-none})" >> "$OPS/watchdog.log"
while true; do
  if curl -s --max-time 8 "$URL/models" | grep -q "qwen36"; then
    [ "$FAILS" -ge 3 ] && echo "$(date +%T) recovered" >> "$OPS/watchdog.log"
    FAILS=0
    echo "UP $(date +%T)" > "$OPS/status.txt"
  else
    FAILS=$((FAILS+1))
    echo "DOWN? fails=$FAILS $(date +%T)" > "$OPS/status.txt"
    echo "$(date +%T) probe failed ($FAILS in a row)" >> "$OPS/watchdog.log"
    if [ "$FAILS" -ge 3 ] && [ -n "$SERVE_CMD" ]; then
      echo "$(date +%T) restarting via SERVE_CMD" >> "$OPS/watchdog.log"
      eval "$SERVE_CMD" >> "$OPS/watchdog.log" 2>&1 &
      FAILS=0
      sleep 60   # give warm-up a head start before probing again
    fi
  fi
  sleep 20
done
