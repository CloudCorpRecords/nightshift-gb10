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
