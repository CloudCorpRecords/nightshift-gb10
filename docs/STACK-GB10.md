# Stack — Running NightShift on the Dell Pro Max with GB10

*Owner: Lane C. Keep this file truthful: record what actually ran, with versions and exact commands, as you go. Judges and teammates will follow this file.*

## Target stack (from the event brief)

| Layer | Choice | Status |
|---|---|---|
| Hardware | Dell Pro Max with GB10 (venue unit for the day) | ☐ claimed at venue |
| Agent runtime | **OpenClaw** — always-on loop, channels, scheduling | ☐ |
| Agent framework | **NVIDIA NemoClaw** — agent team implementation | ☐ |
| Sandbox / guardrails | **OpenShell** — policy-bound execution, egress deny | ☐ |
| Model | **Local open-weight, uncensored/abliterated variant preferred** (see below) via local OpenAI-compatible server | ☐ |
| Product core | This repo, Python 3 stdlib skeleton | ✅ runs |

## Model choice — uncensored, local (team direction, Rene, Oct 25 ~10:21 PT)

We run an **uncensored (abliterated / refusal-removed) open-weight model, locally**, as the primary drafting/research brain. This is an engineering decision, not a stunt:

- **The night shift reads real business data.** Furious customers swear. Security logs describe attacks. Spam contains adult content. A heavily-aligned chat model can refuse, sanitize, or silently mangle exactly the items the Triager most needs summarized faithfully — at 3am, with nobody awake to notice the pipeline quietly dropped the most urgent item of the night.
- **Local means no third-party "safety review" of private data.** The inbox never transits a cloud filter because it never leaves the box at all.
- **Our guardrails are architectural, not model mood.** Safety in NightShift comes from the system: OpenShell sandbox (egress denied), the human approval gate (the model cannot send anything), and receipts for every action. We don't ask the model to be the police; we build a building it can't leave. That's the story for judges: *uncensored model, censored blast radius.*

**Evaluation shortlist (Lane C, decide by results on the box, record the pick here):**
1. An abliterated Qwen or Llama build (refusal-removed variants) sized for the GB10's unified memory with room for the doc index.
2. A Dolphin-family uncensored fine-tune as the alternate.
3. Stock Nemotron-family model as the control — if an uncensored build underperforms on draft quality, we ship the control and say so honestly.

Whichever wins must pass: simulated night end-to-end, no dropped/refused items, fallback test green. Bring candidate weights on a drive — venue Wi-Fi is not a model-delivery plan.

## Bring-up order (do it in this order — each step de-risks the next)

1. **Core first (15 min):** clone repo on the GB10, `python3 -m src.nightshift.main run --simulate`, confirm `outputs/morning-brief.md` renders. *Now the demo exists on the box, whatever happens next.*
2. **Model second:** start the local model server (venue-preferred path first), note the endpoint, `export NIGHTSHIFT_MODEL_URL=http://localhost:<port>/v1`, re-run, confirm drafts change + `python3 -m unittest discover tests` still green (includes the fallback test — kill the server, re-run, core must still work).
3. **OpenShell:** wrap the run command in the sandbox with egress denied; run the demo with venue Wi-Fi **off**. Record the policy file under `config/openshell/`.
4. **OpenClaw + NemoClaw:** wire the night loop as an OpenClaw-scheduled job / NemoClaw agents calling the same `src/nightshift` entry points. If this layer fights back, timebox to 90 minutes — the core demo + OpenShell offline proof already satisfies "runs locally on the box"; document what was wired and what wasn't, honestly, in this file.
5. **Bring a model on a drive:** venue Wi-Fi won't survive 40 teams downloading weights. Anything we might load goes on a USB/external drive *before* relying on it (per event guidance).

## Offline proof protocol (the demo's money moment)

1. Show `NIGHTSHIFT_MODEL_URL` pointing at `localhost`.
2. Disable Wi-Fi / pull the cable, on camera, before the run.
3. Run the full simulated night → brief → approval → receipts.
4. Re-enable network only after the pitch segment ends.

## Fallback ladder (if a layer breaks on stage)

- Model server down → deterministic drafter (automatic).
- GB10 unit trouble → same demo on a team laptop, and we say so honestly; keep fighting for the box in parallel (Lane C).
- OpenClaw/NemoClaw wiring incomplete → core loop runs standalone; stack slide describes core as "agent team with OpenClaw/NemoClaw integration in progress" — never claim what isn't running.

## Record your run here

**Known box facts (from Russ's setup + Bino's SSH guide, 2026-10-25 ~11:06 PT — full guide: `docs/GB10-SSH.md`):**
- Host: `promaxgb10-8525.local` · IP `192.168.107.157` (can change; `hostname -I` on the box) · user `dell` · Wi-Fi `Frontier:Makerspace` only
- GPU: NVIDIA GB10, 128 GB unified memory · CUDA 13.0 at `/usr/local/cuda` (on PATH)
- llama.cpp **already built with CUDA**: `~/src/llama.cpp/build/bin/` — the local model path is `llama-server` + a GGUF in `~/models/`
- PyTorch venv: `source ~/.venvs/torch/bin/activate`
- House rules: check `nvidia-smi` before big jobs (shared GPU); **vLLM `--gpu-memory-utilization` ≤ 0.7** (box stalls above 0.8); don't change the password/SSH settings
- Long jobs: run inside `tmux` so they survive disconnects

### C1 — core on the box (RENE-CLAUDE, 2026-10-25 11:40 PT) ✅

```
Machine: promaxgb10-8525 (aarch64, DGX OS 7.5.0 / Ubuntu 24.04)   Python: 3.12.3
Checkout: ~/work/rene/nightshift-gb10 (branch agent/rene-claude/c1-gb10-bringup)
$ python3 -m src.nightshift.main run --simulate
Night complete: 23 items → 8 clusters → 7 drafts queued. Nothing sent.
$ python3 -m unittest discover tests
Ran 6 tests ... OK
```

### C2 — local model (RENE-CLAUDE, 12:43 PT) ✅

```
vLLM: ghcr.io/aeon-7/aeon-vllm-ultimate:latest (v0.29.0+aeon.sm121a.dspark), served name qwen36, :8000, keyed
Start: ~/work/rene/serve-qwen36.sh  (auto-serve flags minus --speculative-config)
$ bash scripts/ready-check.sh      -> GO (12:41 PT)
$ export NIGHTSHIFT_MODEL_URL=http://localhost:8000/v1 NIGHTSHIFT_MODEL_KEY=$(cat ~/Downloads/vllm-api-key.txt)
$ python3 -m src.nightshift.main run --simulate
Night complete: 23 items → 8 clusters → 7 drafts queued. Nothing sent.   (8.2 s end to end)
7/7 drafts rewritten by qwen36 vs the template run, facts kept, 0 fallbacks.
```

- **Why no DFlash:** with `--speculative-config` (DFlash drafter) the container crash-looped 6+ times: `qwen3_dflash.py:96` passes `use_mm_prefix` to `FlashAttentionImpl.__init__`, which doesn't accept it in this image. Without the drafter the same body model loads and serves; decode is slower but a full night is still ~8 s.
- **Watchdog:** `tmux` session `watchdog` runs `scripts/model-keepalive.sh` status-only (no `SERVE_CMD`); Docker's `--restart unless-stopped` already restarts a crashed server, and a restart command would fire mid warm-up (~6 min). Status: `~/nightshift-ops/status.txt`.

### C2 notes (setup)

- **Model:** `~/models/qwen36-35b-a3b-heretic-nvfp4` = AEON-7/Qwen3.6-35B-A3B-heretic-NVFP4 (abliterated Qwen3.6 35B-A3B MoE, ~5/100 refusal rate per its card, NVFP4, ~23.4 GB). It is safetensors for vLLM, not a GGUF, so llama.cpp can't serve it as-is. Drafter for speculative decoding: `~/models/qwen36-35b-a3b-dflash-drafter`.
- **Server:** Russ's agent (`claude-mlfactory@russ-mbp`) holds the box's `gpu` claim for `vllm-serve` on port 8000 using `ghcr.io/aeon-7/aeon-vllm-ultimate:latest` (box rule: `--gpu-memory-utilization` 0.65). NightShift uses that server; it does not start its own.
- **Client** (`src/nightshift/model.py`): asks the server for its model name (`GET /v1/models`) unless `NIGHTSHIFT_MODEL` is set, sends `chat_template_kwargs.enable_thinking=false` so Qwen3.6 skips its reasoning pass, strips any `<think>` block, timeout `NIGHTSHIFT_MODEL_TIMEOUT` (default 20 s). On failure `LocalModel.last_error` says why and the template draft is used.
- **Run against the model:**
  ```
  cd ~/work/rene/nightshift-gb10
  NIGHTSHIFT_MODEL_URL=http://localhost:8000/v1 python3 -m src.nightshift.main run --simulate
  ```

```
Date/time: ____  Machine hostname: promaxgb10-8525
Python: ____  Model: ____ (check ~/models/ first — see what Russ already loaded)  Endpoint: ____
OpenClaw ver: ____  NemoClaw ver: ____  OpenShell policy: config/openshell/____
Commands that worked (paste exactly):
...
```

### C3/C4 — NemoClaw + OpenShell harness (RENE-CLAUDE, 13:15 PT)

```
Installer: curl -fsSL https://www.nvidia.com/nemoclaw.sh  (read before running; bootstraps github.com/NVIDIA/NemoClaw)
Env: NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1 (Rene accepted the notice) NEMOCLAW_NO_EXPRESS=1 NEMOCLAW_NON_INTERACTIVE=1
     NEMOCLAW_SANDBOX_NAME=nightshift NEMOCLAW_PROVIDER=custom NEMOCLAW_ENDPOINT_URL=http://localhost:8000/v1
     NEMOCLAW_MODEL=qwen36 COMPATIBLE_API_KEY=<read from ~/Downloads/vllm-api-key.txt at install time>
Result: NemoClaw v0.0.137, OpenShell 0.0.116 (docker driver), OpenClaw 2026.9.2, sandbox "nightshift" Ready
In-sandbox model URL: https://inference.local/v1  (OpenShell router -> host.openshell.internal:8000 -> qwen36; key injected by the gateway, not visible in the sandbox)
$ openshell policy set nightshift --policy config/openshell/nightshift-egress.yaml --wait   -> policy v4 active
Probe inside sandbox: qwen36 answers; api.github.com, integrate.api.nvidia.com, pypi.org, registry.npmjs.org, example.com all blocked
$ openshell sandbox upload nightshift ~/work/rene/nightshift-gb10 /sandbox/
$ openshell sandbox exec -n nightshift --workdir /sandbox/nightshift-gb10 --env NIGHTSHIFT_MODEL_URL=https://inference.local/v1 -- python3 -m src.nightshift.main run --simulate
Night complete: 23 items → 8 clusters → 7 drafts queued. Nothing sent.   (8 s, tests OK inside the sandbox)
```

- Gotchas: the upstream OpenShell apt package (0.1.5) conflicts with NemoClaw's pinned 0.0.116; remove it. The user systemd manager on this box predates dell's docker group, so a systemd-user OpenShell gateway can't see Docker (NemoClaw's own gateway is fine).
- **C3 ✅ OpenClaw drives the night:** the first `openclaw agent` turn hung because the sandbox CLI's request for a gateway scope upgrade (exec) sat unapproved. After `openclaw devices approve <requestId>`, inside the sandbox:
  ```
  $ openshell sandbox exec -n nightshift -- openclaw agent --session-id nightshift-c3d --message-file /sandbox/openclaw-night.txt --json
  finalAssistantVisibleText: "Night complete: 23 items → 8 clusters → 7 drafts queued. Nothing sent."   winnerModel: qwen36   (16 s)
  ```
  Chain: OpenClaw agent (qwen36 via inference.local) → exec tool → NightShift night → drafts via qwen36 → brief, all inside the OpenShell sandbox with egress denied. Prompt file: `scripts/openclaw-night.txt`.
