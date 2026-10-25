# SUBMISSION — BuilderBase Checklist

*Owner: Lane D. Event: Dell x NVIDIA AI Hackathon, San Francisco — https://builderbase.com/track-dashboard/dell-x-nvidia-ai-hackathon-san-francisco/overview*

## ⚠️ First task: confirm and write down

- [ ] **Exact submission deadline TODAY: ______ PM PT** (read it off the BuilderBase dashboard — Rene's team view — and replace this line; also announce in LOG)
- [x] Team name on BuilderBase: **bino force go** (Rene Turcios, Bino Baby, Russ, Mike Rice)
- [ ] Team members on BuilderBase = team members in `comms/AGENTS.md`: ☐

## Submission contents (draft text lives below the checklist)

- [ ] Project name: **NightShift**
- [ ] Repo link: https://github.com/CloudCorpRecords/nightshift-gb10
- [ ] One-liner (below)
- [ ] Description (below)
- [ ] Demo: live on the GB10 + brief/approval flow per `DEMO.md`; top-8 live pitch if selected
- [ ] Stack declared: Dell Pro Max with GB10 · OpenClaw · NVIDIA NemoClaw · OpenShell · local open-weight model
- [ ] Screenshots/GIF of the morning brief + approval queue (Task D4)
- [x] Team photo/logo: `assets/team-bino-force-go.png` (also at the top of the README) — upload it to the BuilderBase team/project page too (dashboard is login-gated for agents; Rene/Bino do this tap)

## Draft copy (edit freely, keep it honest)

**One-liner:** The always-on local ops agent that works the night shift on your Dell Pro Max with GB10 — triaging inbox, tickets, and incidents overnight, drafting everything, sending nothing, and handing you a morning brief with an approval queue. No cloud. No leaks. Receipts for everything.

**Description:**
Every team has an overnight problem: customer email, support tickets, and incidents pile up while humans sleep, and the first hours of the morning are spent digging instead of deciding. Cloud agents offer to help — if you ship them your inbox, your tickets, and your internal runbooks.

NightShift is the local answer. Five agents (Watcher, Triager, Researcher, Drafter, Briefer) run entirely on one Dell Pro Max with GB10. Overnight they ingest inbox, support, logs, and CRM exports; cluster duplicates; link incidents to the tickets and emails they caused; root-cause from private local runbooks; and draft every reply and update. They never send anything: a human approves the queue in the morning, and every action writes an auditable receipt.

We demo with the network off. Privacy for NightShift isn't a policy page — it's physics: nothing leaves the box, because nothing has to.

**Built with:** OpenClaw (runtime), NVIDIA NemoClaw (agent framework), OpenShell (sandboxed, egress-denied execution), a local open-weight model on the GB10, and a deterministic core that guarantees the demo — and the product — works even with no model loaded.
