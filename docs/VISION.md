# Vision — Thought Leadership

*Authored by Tree (lead agent) for the team, Oct 25, 2026. Argue with it in `comms/channels/decisions.md` — if we change our mind, we change this file in the same PR.*

## The problem nobody demos honestly

Every team already has an "overnight problem": between 6pm and 9am, a small company receives the customer email that churns, the ticket that duplicates five times, the log spike that becomes tomorrow's outage, and the CRM record that rots. The current answers are bad:

- **A human on call** — expensive, exhausted, and still asleep for the first two hours of the incident.
- **A cloud agent** — capable, but it asks the company to ship its inbox, tickets, and internal runbooks to someone else's computer, governed by a policy page.
- **A chatbot** — waits to be prompted. The work doesn't need a conversation; it needs to be *done and waiting for approval*.

## Our thesis

**The winning agent is not the smartest one in the room. It's the one that's still working when the room is empty — on hardware the company owns, with a gate a human controls.**

Three claims we will defend to judges:

### 1. Local is a feature you can prove, cloud privacy is a promise you can't

On the Dell Pro Max with GB10 we can run a capable open-weight model, retrieval over private docs, and a full agent team with the network cable pulled. In the demo we do exactly that. "Your data never leaves this box" stops being marketing and becomes physics.

### 2. The unit of value is the morning brief, not the chat turn

Ops, sales, support, and engineering leads don't want to interview an agent at 9am. They want: *what happened, what matters, what I drafted for you, approve or edit.* NightShift optimizes for that artifact — a brief with sources and a receipts log — not for conversation.

### 3. The approval gate is the product

Full autonomy demos well and deploys never. Every business owner we describe this to asks the same question: "what stops it from emailing a customer something wrong at 3am?" Our answer is architectural: the Drafter physically cannot send; the Orchestrator executes only items a human approved, and logs every execution. The trust ladder — draft → approve → (later, per-category) auto-approve with receipts — is how this becomes a real product on Monday.

## Why GB10 specifically

- Unified memory big enough for a real local model + retrieval index + agent runtime on one desk machine.
- Always-on economics: a deskside box idling overnight costs almost nothing vs per-token cloud agents watching empty inboxes.
- Clusterable later (2–4 systems) — the roadmap slide: one box per team → a rack of NightShifts per company.

## What we are NOT building today

- No real Gmail/CRM integrations (mock local data only — honest scope, working demo).
- No auto-send, ever, in v1.
- No fine-tuning. Off-the-shelf local model, great orchestration, great UX of the brief.
- No dashboard-itis. The brief + approval queue is the interface.

## If we win the room, it's because

1. The demo runs **on the box, offline**, end to end, in under 3 minutes.
2. A judge from ops/support/eng can say "I would use that tomorrow morning."
3. Every claim is backed by a receipt in the repo: logs, tests, and this document's honesty about scope.

## Roadmap (say it in the pitch, build none of it today)

- Real connectors (IMAP, Zendesk/Help Scout exports, PagerDuty webhooks — all local-network).
- Per-category trust ladder with auto-approve + receipts.
- Multi-box clustering; a NightShift per department sharing one private index.
- OpenShell policy packs per industry (HIPAA-shaped, SOC2-shaped egress rules).
