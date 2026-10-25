# DEMO — The 3-Minute Script

*Owner: Lane D. Rehearse twice minimum. The demo must run ON the GB10, offline segment included.*

## Setup (before judges arrive)

- NightShift core running on the GB10; terminal + brief output ready.
- Sample night loaded (`data/sample/`). A second "live drop" file ready for B2's watcher moment if built.
- Wi-Fi ON at start (we turn it off live — that's the point).

## Script

**0:00 — The problem (say it, show nothing yet)**
"Every night, your company's inbox, tickets, and servers keep working. You don't. By 9am there's a pile — and somewhere in it is the one thing that actually matters. The current fix is a cloud agent, which means shipping your inbox and your runbooks to someone else's computer. We built the other answer."

**0:30 — Meet NightShift (show the box)**
"This is NightShift, running entirely on this Dell Pro Max with GB10. Five agents — Watcher, Triager, Researcher, Drafter, Briefer. No cloud API. And to prove that isn't a slide—" *(disable Wi-Fi / pull cable)* "—network's off. It stays off."

**0:50 — The night, accelerated (run it)**
`python3 -m src.nightshift.main run --simulate`
Narrate the timeline: "23 items land overnight — inbox, tickets, CRM… at 2:14am the payments service starts throwing 502s… watch the Triager link the incident alerts to the two tickets and three customer emails it caused — one cluster of seven, not seven separate fires."

**1:40 — The morning brief (open `outputs/morning-brief.html` in the browser; `outputs/morning-brief.md` is the same brief for the terminal)**
"9am. This is what the human gets. Four numbers at the top: 23 in, 8 clusters, 7 drafts, 0 sent. What happened, what matters — the incident is #1, root-caused against *our own runbook* by the Researcher, locally. Every draft is here: the customer reply, the incident summary, the CRM clean-ups. And notice—" *(point at the gate)* "—**nothing has been sent.** NightShift can't send. It can only draft."

**2:20 — The approval gate (approve live)**
Approve the queue (one action). "One click. The replies execute against our systems, and every single action writes a receipt — source, reason, timestamp. If it happened overnight, you can audit it over coffee."

**2:45 — Close**
"Cloud agents ask for trust. NightShift earns it structurally: your data never left this box, because it never had to. Give every team a NightShift on a GB10, and the night shift is finally staffed — by an agent you'd actually trust with the keys, because you hold the gate."

## Failure drills

- Model hiccup mid-demo → fallback drafter is already the default path; keep talking, don't debug on stage.
- Terminal trouble → printed brief backup + screenshots in the submission; Lane D keeps both within arm's reach.
- Judge asks "is that real data?" → "Simulated night, real pipeline — the same code runs the file-drop watcher live if you'd like to drop a file in now." (B2 shipped 11:35 PT — offer it.)

## Demo video (under 2:00) — REQUIRED by BuilderBase, film on the GB10

*One continuous screen recording on the box, voiceover live or dubbed. The requirement: "the agent working end to end on the GB10." Target 1:45.*

- **0:00–0:15 — The claim.** Terminal on the GB10 (`nvidia-smi` visible). "This is a Dell Pro Max with GB10. Everything you're about to see runs on this box — watch: Wi-Fi off." Toggle the network off on camera.
- **0:15–0:45 — The night runs.** `python3 -m src.nightshift.main run --simulate` → "23 items → 8 clusters → 7 drafts queued. Nothing sent." Open `outputs/morning-brief.md`: incident cluster first, runbook citation, red-flag section calling out the charged-twice billing item.
- **0:45–1:15 — Always-on, live.** Start `python3 -m src.nightshift.main watch --dir data/live`. Drag one nasty item file in (the profane cancel-threat `.item.json` from `data/live-seeds/` if present, else any sample item): the night rebuilds itself on camera — new cluster, red flag raised, draft written. "A censored model would soften that message. Ours reads it as-is — and still sends nothing."
- **1:15–1:40 — The gate.** `python3 -m src.nightshift.main approve --ids Q1` → receipt lines print. Show `outputs/receipts.log`. "Humans hold the gate. Every action has a receipt."
- **1:40–1:55 — Close.** "NightShift. The night shift, staffed — privately, on one GB10." Team logo frame.

Film in one take if possible; retakes allowed, dignity optional. Upload, set public/unlisted, paste the link into SUBMISSION.md field 4 and the BuilderBase dashboard.
