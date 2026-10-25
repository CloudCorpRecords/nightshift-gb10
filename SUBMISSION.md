# SUBMISSION — BuilderBase (field-by-field, ready to paste)

*Owner: Lane D (BINO) + TREE. Event: Dell x NVIDIA AI Hackathon, San Francisco — https://builderbase.com/track-dashboard/dell-x-nvidia-ai-hackathon-san-francisco/overview*
*Dashboard state seen 11:28 PT (Rene's screenshot): 0/17 items, timer "0d 9h left" → hard deadline ≈ **8:30 PM PT**. Team plan stays stricter: build till **5:00 PM PT**, expedited mode 3:00 PM, code freeze 4:30 PM, submission pasted in by 5:00 PM, top-8 pitches in the evening.*

Team on BuilderBase: **bino force go** — Rene Turcios, Bino Baby, Russ, Mike Rice.

---

## 1. Project name ✅ ready
**NightShift**

## 2. One-line pitch ✅ ready
NightShift is the always-on local ops agent for support, ops, and engineering teams — it works the night shift on a Dell Pro Max with GB10, triaging inbox, tickets, and incidents overnight, drafting everything, sending nothing, and handing you a morning brief with an approval queue.

## 3. Repository URL ✅ ready
https://github.com/CloudCorpRecords/nightshift-gb10 (public, MIT — judges can open it)

## 4. Demo video URL ⏳ team films at the venue
*Required: under 2 minutes, the agent working end to end on the GB10. No screen share during live pitches — the video + deck carry the story.*
Script: see `DEMO.md` → "Demo video (under 2:00)". Paste the final link here: ______

## 5. What you built, and what runs locally ✅ ready
NightShift is a five-agent system that runs a company's overnight operations on one Dell Pro Max with GB10. A Watcher ingests the night's inbox, support tickets, CRM exports, and incident alerts into one item stream (a live drop-folder mode rebuilds the night in real time as files arrive). A Triager clusters duplicates and related items, scores urgency deterministically, and raises red flags for churn, legal, breach, and refund language so business-risk items can never sit quietly in a queue. A Researcher root-causes incidents against private local runbooks. A Drafter writes every reply, customer update, and internal note. A Briefer renders the morning brief and a machine-readable approval queue. An orchestrator with a hard approval gate executes only what a human approves — the agents send nothing, ever — and every action writes an auditable receipt.

Everything runs locally on the GB10. All inference (drafting, summarization, tool selection) runs on the box against a local open-weight model served by vLLM at an OpenAI-compatible endpoint on localhost; there are no cloud LLM calls — the demo runs with the network off. Verified live on the box: a full simulated night (23 items → 8 clusters → 7 drafts) completes in ~8 seconds, every draft written by the local model. A deterministic core guarantees the pipeline end to end even if no model is loaded, so the product never depends on a model behaving. The stack: Dell Pro Max with GB10 (128 GB unified memory), CUDA 13, vLLM, a dependency-free Python core, an endpoint watchdog, and egress discipline by design — nothing in the product path can reach the network.

## 6. Getting started with the DGX Spark — walkthrough ✅ ready (feedback for NVIDIA)
Our box was on the venue's Makerspace Wi-Fi as `promaxgb10-8525`, user `dell`. Getting in: generate an SSH key, then either hand the box owner your public key or take the password in person and `ssh-copy-id` once — after that, key-only login just works, and the host key fingerprint was published so first-connect verification was a real check, not a leap of faith. The pleasant surprises: CUDA 13 already on PATH, a CUDA build of llama.cpp already compiled (`~/src/llama.cpp/build/bin/`), a `~/models/` directory ready for GGUFs, and a PyTorch venv waiting (`~/.venvs/torch`). From power-on to a running local inference stack was minutes, not hours.
Friction worth fixing: the box's IP can change and it is reachable only from the venue Wi-Fi, so remote teammates and agents need a bridge (we used Tailscale) — collecting SSH public keys at registration, or pre-installing a mesh tool, would erase that entirely. And one sharp edge: vLLM above ~0.8 `--gpu-memory-utilization` stalls the box; 0.7 or lower is the safe line. A one-page "your box already has X, watch out for Y" sheet in the box would have saved every team real time.

## 7. Pitch deck ✅ ready
Public Slides link (anyone with the link can view): https://docs.google.com/presentation/d/1dPPzcf0FzjSiLcGEJHP-4UH7Xjtp9OnwXvX2XDJ7yg8/edit — 8 slides, also lives in the team Drive folder.

## 8. Resources that helped most / wished we'd had ✅ ready
Helped most: the organizer-provided SSH guide for the box (exact commands, host fingerprint, failure table — it got four people in without a single support ticket); the preinstalled stack (CUDA 13 on PATH, a CUDA llama.cpp build, a ready ~/models/ directory, a PyTorch venv); and vLLM's OpenAI-compatible server, which let our pipeline treat the local model as a drop-in endpoint — our model client needed no GB10-specific code at all.
Wished we'd had: SSH key collection at check-in (or Tailscale preinstalled) so remote agents could reach the box from minute one; a published list of what is preinstalled on the box before the event; and a starter set of local models on USB — including uncensored/abliterated builds, which matter for ops agents that must process real, messy customer language faithfully (venue Wi-Fi is not where you want to download 40 GB of weights).

## 9. What would have got you there faster? ✅ ready
Three things. (1) Remote access to the box arranged at registration — public keys collected with the signup form would have put every team's agents on the hardware immediately; we spent the first hour on access logistics instead of building. (2) A reserved, stable hostname/IP per team instead of an address that can change. (3) The submission checklist published before the event — knowing a sub-2-minute on-box demo video and a public deck were required would have shaped our morning, not our afternoon.

## 10. What model(s) did you move forward with, and for what? ✅ ready
We moved forward with **Qwen3.6-35B-A3B-heretic (NVFP4)** — the abliterated (uncensored) build of Qwen3.6 35B — served by **vLLM on the GB10** at an OpenAI-compatible endpoint (`:8000/v1`, model id `qwen36`). It does the language work: drafting replies and incident updates, and summarizing clusters for the morning brief. We deliberately chose an uncensored build as the primary: an overnight ops agent reads the rawest text a company produces — profane churn threats, breach chatter, abuse reports — and a safety filter that silently drops or sanitizes the angriest customer of the night is a product failure, not a safety feature. Our safety story is architectural instead: the product path can reach nothing but localhost, a hard human approval gate (agents draft, humans send), and a receipt for every action — an uncensored model inside a gated system. NightShift's model client discovers the served model name from the server, disables Qwen's thinking pass for drafting latency, and records why any call fell back. All deterministic triage, clustering, and red-flag detection runs without any model, so the pipeline is provable end to end with the model removed.

## 11. What drove your model choices? ✅ ready (added 12:54 PT from Rene's full-dashboard screenshots)
Three drivers. (1) It had to run entirely on one GB10: Qwen3.6-35B-A3B's mixture-of-experts layout (35B total, ~3B active per token) gives 35B-class drafting quality at small-model latency on the GB10's unified memory — our full night run (23 items → 7 drafts) completes in ~8 seconds, and the NVFP4 weights are ~21.75 GB, leaving headroom for KV cache and the rest of the stack. (2) It had to handle real ops language faithfully: an overnight agent reads the rawest text a company produces — profane churn threats, breach chatter, abuse reports — and a stock aligned model can refuse or quietly sanitize exactly the drafts that matter most, so we chose the abliterated (uncensored) "heretic" build and put safety in the architecture instead: the model may draft anything, but it can send nothing — the product path reaches only localhost, and every external action waits in a human approval queue with receipts. (3) It had to be servable as a boring endpoint: an OpenAI-compatible vLLM server meant our agent code treats the GB10 model like any other endpoint, with a deterministic fallback when it's down.

## 12. How did you get set up with your models? ✅ ready
Models live in ~/models/ on the box. The Qwen3.6-35B-A3B-heretic NVFP4 weights (~21.75 GB) were downloaded to the box and are served by vLLM as an OpenAI-compatible endpoint on localhost:8000 (served model id `qwen36`, API-key gated; the key stays in a box-local file, never in the repo). Two setup lessons: the box's auto-serve initially crash-looped — its DFlash speculative-decoding config hit a TypeError in FlashAttention on this build — so we serve without `--speculative-config` via a small serve script; and vLLM's `--gpu-memory-utilization` stays at or below 0.7, per the box's known stall behavior above 0.8. NightShift connects through two env vars (model URL + key). A ready-check script gates every run and demo: the endpoint must answer, `qwen36` must be the served model, and a keyed 1-token completion must return real content — that check caught the classic trap where a keyed endpoint silently 401s an unkeyed client and the agent falls back to templates without anyone noticing.

## 13–17. NemoClaw / OpenShell questions ⏳ depends on C3/C4 (timeboxed, cut 14:18 PT)
*Fill LAST, from RENE-CLAUDE's C3/C4 log entries — never claim the harness before it runs.*
- **13. Did you use NemoClaw and/or OpenShell today?** — YES variant: "Yes." NO variant: "No."
- **14. Likelihood to recommend (1–10, optional)** — only if YES; pick from the C3/C4 experience notes.
- **15. Share why / additional feedback (required)** — YES variant skeleton: what the harness made easier (policy-as-code egress, agent framework) + the day's real friction (nothing preinstalled on the box — no Node/npm; installs over shared venue Wi-Fi). NO variant: "We timeboxed a 90-minute integration attempt and prioritized the working agent + local model serving, which shipped. Our equivalent controls live in the product itself (localhost-only product path, human approval gate, receipts). What would have changed the answer: NemoClaw/OpenShell preinstalled on the box, or a 10-minute quickstart that starts from a running local vLLM endpoint."
- **16. How secure did you feel building with it (1–10, required)** — only meaningful if YES; if NO and the form forces a value, use the NO-variant note in 17 to explain.
- **17. What influenced your rating? (optional)** — mirror 15 in one or two sentences.

## Dashboard state (verified 12:54 PT, Rene's screenshots)
All 17 items enumerated: 1–3 ✅, 4 video ⏳ (venue), 5 ✅ (corrected to the vLLM truth 12:54 — no llama.cpp serving, no harness claims), 6 ✅, 7 ✅, 8 ✅ (corrected), 9 ✅, 10 ✅, 11 ✅, 12 ✅, 13–17 ⏳ (C3/C4 outcome, fill last). Timer on dashboard: "0d 7h left" → hard deadline ≈ 8:00 PM PT. Team plan unchanged: everything filled by 5:00 PM PT.

**One-liner (short form, for anywhere a single sentence is needed):** The always-on local ops agent that works the night shift on your Dell Pro Max with GB10 — triaging inbox, tickets, and incidents overnight, drafting everything, sending nothing, and handing you a morning brief with an approval queue. No cloud. No leaks. Receipts for everything.
