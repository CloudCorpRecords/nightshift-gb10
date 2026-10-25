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

Everything runs locally on the GB10. All inference (drafting, summarization, tool selection) runs on the box against a local open-weight model served by a CUDA-built llama.cpp; there are no cloud LLM calls — the demo runs with the network off. A deterministic core guarantees the pipeline end to end even if no model is loaded, so the product never depends on a model behaving. The stack: Dell Pro Max with GB10 (128 GB unified memory), CUDA 13, llama.cpp, OpenClaw as the agent runtime, NVIDIA NemoClaw as the agent framework, and OpenShell for sandboxed, egress-denied execution.

## 6. Getting started with the DGX Spark — walkthrough ✅ ready (feedback for NVIDIA)
Our box was on the venue's Makerspace Wi-Fi as `promaxgb10-8525`, user `dell`. Getting in: generate an SSH key, then either hand the box owner your public key or take the password in person and `ssh-copy-id` once — after that, key-only login just works, and the host key fingerprint was published so first-connect verification was a real check, not a leap of faith. The pleasant surprises: CUDA 13 already on PATH, a CUDA build of llama.cpp already compiled (`~/src/llama.cpp/build/bin/`), a `~/models/` directory ready for GGUFs, and a PyTorch venv waiting (`~/.venvs/torch`). From power-on to a running local inference stack was minutes, not hours.
Friction worth fixing: the box's IP can change and it is reachable only from the venue Wi-Fi, so remote teammates and agents need a bridge (we used Tailscale) — collecting SSH public keys at registration, or pre-installing a mesh tool, would erase that entirely. And one sharp edge: vLLM above ~0.8 `--gpu-memory-utilization` stalls the box; 0.7 or lower is the safe line. A one-page "your box already has X, watch out for Y" sheet in the box would have saved every team real time.

## 7. Pitch deck ✅ ready
Public Slides link (anyone with the link can view): https://docs.google.com/presentation/d/1dPPzcf0FzjSiLcGEJHP-4UH7Xjtp9OnwXvX2XDJ7yg8/edit — 8 slides, also lives in the team Drive folder.

## 8. Resources that helped most / wished we'd had ✅ ready
Helped most: the organizer-provided SSH guide for the box (exact commands, host fingerprint, failure table — it got four people in without a single support ticket); the preinstalled CUDA llama.cpp build and model directory; OpenClaw, NemoClaw, and OpenShell documentation for the agent runtime, framework, and sandboxing story; and llama.cpp's OpenAI-compatible server, which let our pipeline treat the local model as a drop-in endpoint.
Wished we'd had: SSH key collection at check-in (or Tailscale preinstalled) so remote agents could reach the box from minute one; a published list of what is preinstalled on the box before the event; and a starter set of local models on USB — including uncensored/abliterated builds, which matter for ops agents that must process real, messy customer language faithfully (venue Wi-Fi is not where you want to download 40 GB of weights).

## 9. What would have got you there faster? ✅ ready
Three things. (1) Remote access to the box arranged at registration — public keys collected with the signup form would have put every team's agents on the hardware immediately; we spent the first hour on access logistics instead of building. (2) A reserved, stable hostname/IP per team instead of an address that can change. (3) The submission checklist published before the event — knowing a sub-2-minute on-box demo video and a public deck were required would have shaped our morning, not our afternoon.

## 10. What model(s) did you move forward with, and for what? ⚠️ confirm after box inventory
*Fill the exact names/sizes from `~/models/` when Lane C reports (TREE/BINO). Current honest state:*
We moved forward with a local open-weight model served by llama.cpp on the GB10 for the language work — drafting replies and incident updates, and summarizing clusters for the morning brief. We deliberately chose an uncensored (abliterated) build as the primary: an overnight ops agent reads the rawest text a company produces — profane churn threats, breach chatter, abuse reports — and a safety filter that silently drops or sanitizes the angriest customer of the night is a product failure, not a safety feature. Our safety story is architectural instead: OpenShell egress-deny, a hard human approval gate (agents draft, humans send), and a receipt for every action — an uncensored model inside a gated system. A stock model runs as the honest control in our bake-off harness, which counts items dropped, mangled, or refused by each model on the same nasty-night input. All deterministic triage, clustering, and red-flag detection runs without any model, so the pipeline is provable end to end with the model removed. *(Exact model name + size: ______)*

## Remaining dashboard items (7 below the fold on Rene's screenshot)
Rene/Bino: scroll the dashboard list and send TREE the remaining field names — copy will be drafted same-hour. Paste order for Lane D: fields 1–3 and 5 now (they don't depend on the box), deck + video links last.

**One-liner (short form, for anywhere a single sentence is needed):** The always-on local ops agent that works the night shift on your Dell Pro Max with GB10 — triaging inbox, tickets, and incidents overnight, drafting everything, sending nothing, and handing you a morning brief with an approval queue. No cloud. No leaks. Receipts for everything.
