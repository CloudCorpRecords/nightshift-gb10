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

```
Date/time: ____  Machine hostname: ____
Python: ____  Model: ____  Endpoint: ____
OpenClaw ver: ____  NemoClaw ver: ____  OpenShell policy: config/openshell/____
Commands that worked (paste exactly):
...
```
