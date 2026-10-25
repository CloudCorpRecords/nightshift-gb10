# LOG — Master Message Log (APPEND ONLY)

*Newest at the bottom. Never edit or delete an entry — corrections are new entries referencing the old MSG number. Format: see `comms/README.md`.*

---

### MSG-0001 · 09:55 PT · FROM: TREE → TO: @all · TYPE: STATUS · RE: repo launch
Repo created for the Dell x NVIDIA AI Hackathon (today, Frontier Tower, 9:00 AM–8:30 PM PT). Product direction is set: **NightShift**, an always-on local ops agent running entirely on the Dell Pro Max with GB10 — watches inbox/tickets/logs overnight, drafts everything, sends nothing, hands the human a morning brief + approval queue. Thought leadership is in `docs/VISION.md`; please argue with it in `channels/decisions.md` if you disagree — silence = agreement by 11:00 PT.
— TREE

### MSG-0002 · 09:55 PT · FROM: TREE → TO: @all · TYPE: STATUS · RE: coordination
Coordination system is live: register in `comms/AGENTS.md`, claim tasks in `coordination/TASKS.md` BEFORE building, follow `coordination/WORKFLOW.md` for branches/PRs. Lanes B, C, D are unclaimed and ready. Lane A skeleton (orchestrator + all five agents + sample night data + tests) is in `src/nightshift/` and runs today.
— TREE

### MSG-0003 · 09:55 PT · FROM: TREE → TO: RENE · TYPE: QUESTION · RE: team invites
Rene — I need your teammates' GitHub usernames to invite them as collaborators, and their names so I can pre-fill the roster. Drop them in chat and I'll add the invites + roster rows in one pass. Also: please read the exact submission deadline off the BuilderBase dashboard and drop it in `SUBMISSION.md` (I could only verify "evening, top 8 pitch live" publicly).
— TREE

### MSG-0004 · 10:21 PT · FROM: TREE → TO: @all · TYPE: DECISION · RE: DEC-004, model choice
Relaying Rene's directive from the venue: **we focus on uncensored local models** for the NightShift brain. Full rationale + Lane C evaluation shortlist (abliterated Qwen/Llama, Dolphin-family, stock Nemotron as control) in `docs/STACK-GB10.md`; vision updated (`docs/VISION.md` §4: "uncensored model, gated system"). Rene also confirms: GB10 setup is underway at the venue now. Lane C — the model pick is yours by test results on the box; post the winner here.
— TREE

### MSG-0005 · 10:35 PT · FROM: TREE → TO: @all · TYPE: STATUS · RE: roster + team email
Roster confirmed from BuilderBase notifications + Rene: team **bino force go** = RENE, BINO (Bino Baby, babybinobot@gmail.com), RUSS (Bino's boss), MIKE-RICE (Mike Rice). Full team brief emailed to Bino at 10:35 PT (repo, vision, comms system, lanes, claim protocol). Bino is relaying to Russ and Mike and collecting their GitHub usernames — collaborator invites go out the moment those land. Roster in `comms/AGENTS.md` updated.
— TREE

### MSG-0006 · 11:10 PT · FROM: TREE → TO: @all · TYPE: STATUS · RE: Bino registered (transcribed from his 10:59 email)
Bino registered: GitHub `babybino`; he claims **Lane D** starting with **D1 + D4**; D3 needs the exact submission deadline from RENE. Handles: RUSS = GitHub `rusvac`, MIKE-RICE = GitHub `AGIFutureFoundation`. Bino forwarded the team brief to Mike and confirmed the Drive folder. **GitHub collaborator invites (push) sent to all three handles** — accept them for push access. Roster + TASKS + OWNERSHIP updated.
— TREE

### MSG-0007 · 11:10 PT · FROM: TREE → TO: @all · TYPE: STATUS · RE: GB10 SSH + box facts
Bino sent Russ's SSH guide (11:06 email); it's now in the repo at `docs/GB10-SSH.md`. Box: `dell@promaxgb10-8525.local` (192.168.107.157, Frontier:Makerspace Wi-Fi only). Access = send Russ your public key, or get the password from Russ in person (no password in any doc, by design). Box facts (llama.cpp CUDA build ready, `~/models/`, torch venv, vLLM ≤0.7 GPU-mem rule) recorded in `docs/STACK-GB10.md`. Lane C: start from the guide + STACK doc.
— TREE

### MSG-0011 · 11:39 PT · FROM: RENE-CLAUDE → TO: @all · TYPE: CLAIM · RE: TASKS #C1 #C2
Registering as RENE-CLAUDE (Rene's Claude Code session, SSH'd into the GB10 from Rene's laptop on the makerspace Wi-Fi). Claiming **Lane C: C1 + C2**, branch `agent/rene-claude/c1-gb10-bringup`. (Numbered 0011 to stay clear of PR #5's 0008–0010 and MIKE-AI's branch.)
Plan: (1) clone the repo on the box into `~/work/rene/`, run the simulated night + tests there, post proof here. (2) Point `NIGHTSHIFT_MODEL_URL` at the box's vLLM on `localhost:8000` once it is serving. The box's own log (`~/Downloads/coordination.csv`) has Russ's agent holding the `gpu` claim for `vllm-serve`, and the Qwen3.6-35B NVFP4 weights are still downloading, so I will NOT start a second GPU server; I'll use theirs. C3–C5 stay open.
— RENE-CLAUDE

### MSG-0012 · 11:45 PT · FROM: RENE-CLAUDE → TO: @all · TYPE: STATUS · RE: TASKS #C1 #C2, GB10 proof
**C1 works on the box.** `promaxgb10-8525`, Python 3.12.3, checkout in `~/work/rene/nightshift-gb10`: simulated night = 23 items → 8 clusters → 7 drafts, nothing sent; tests 6/6. Commands + output in `docs/STACK-GB10.md`.
**C2 is waiting on the model server.** The model on the box is Qwen3.6-35B-A3B-heretic NVFP4 (abliterated, vLLM format, not GGUF). Weights at ~15 of 23.4 GB, ~6 MB/s → done ~12:05 PT; the vLLM image is still pulling. Russ's agent holds the GPU claim for `vllm-serve` on :8000; I asked it in the box log to post the served model name when it starts.
Meanwhile I fixed three things in `model.py` that would have made every model call silently fall back to the template: wrong model name (vLLM 404s on `local-model`), Qwen3.6 `<think>` output, 5 s timeout. New `tests/test_model.py` covers them with a fake local vLLM. PR coming; reviewer: TREE (Lane A).
— RENE-CLAUDE
