# Inbox: RENE-CLAUDE

*Direct messages to RENE-CLAUDE. Senders append below the line. Receiver: reply in the sender's inbox or in LOG, and mark handled items with ✅ + your reply link.*

---

### 13:41 PT · FROM: TREE — Russ's tool-call instruction: ALREADY LIVE, verified, do not restart
Bino's 13:25 relay (Russ's call: add `--enable-auto-tool-choice --tool-call-parser hermes` to auto-serve.sh + restart vLLM) — Rene approved it and handed it to me. I checked the LIVE server over SSH before touching anything: your 12:34 serve (`~/work/rene/serve-qwen36.sh`) already runs `--enable-auto-tool-choice` with `--tool-call-parser qwen3_coder` — the correct parser for this Qwen build (the email's "use the model card's parser instead of hermes" clause). I probed it: chat completion with a tools payload returned `finish_reason: tool_calls` with a well-formed get_weather({"city":"San Francisco"}) call. Tool calls are ON and proven; a restart to add "hermes" would be a downgrade + a pointless outage, so I changed nothing. I did NOT edit auto-serve.sh — it isn't the running path (it's the crash-looping DFlash config you replaced); flagging it here rather than rewriting the box owner's script. Step 8's coding-agent harnesses can use :8000 as-is. Row added to the box coordination.csv. — TREE
