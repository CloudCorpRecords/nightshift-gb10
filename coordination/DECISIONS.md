# DECISIONS — Formal Record

*Fast discussion in `comms/channels/decisions.md`; the settled outcome lands here. Format: ID, date/time PT, decision, who, why, what it overrides.*

## DEC-001 · 2026-10-25 09:55 PT · Product = NightShift
**Decision:** Build NightShift — always-on local ops agent (inbox + tickets + incident + CRM → morning brief + approval queue), running entirely on the Dell Pro Max with GB10, no cloud API in the product path.
**By:** RENE (direction) + TREE (concept). **Why:** Direct hit on the official challenge ("always-on agent someone in ops, sales, support or engineering would want tomorrow"); local-only turns GB10 from a constraint into the headline feature (privacy by architecture); differentiated from generic single-purpose inbox bots by the cross-source incident story + approval gate.

## DEC-002 · 2026-10-25 09:55 PT · Coordination via Markdown in git
**Decision:** All team coordination (humans + their AI agents) happens in `comms/` Markdown files with signed, numbered messages, a claim board, and lane ownership.
**By:** RENE (requirement) + TREE (design). **Why:** Every agent tool can read/write Markdown; git provides history/authorship; the coordination itself becomes demo evidence of a multi-agent team working well.

## DEC-004 · 2026-10-25 10:21 PT · Uncensored local models are the primary brain
**Decision:** NightShift's primary local model is an uncensored/abliterated open-weight model run on the GB10 (Lane C evaluates the shortlist in `docs/STACK-GB10.md` against a stock-model control). Safety is enforced architecturally — OpenShell egress-deny, human approval gate, receipts — not by model refusals.
**By:** RENE (directive, relayed by TREE). **Why:** an overnight ops agent must faithfully process real, messy business data (angry customers, security incidents, adult spam) without a filter silently dropping or mangling the most urgent items; local-only means no third-party review of private data either.

## DEC-003 · 2026-10-25 09:55 PT · Deterministic fallback is a product rule
**Decision:** Every model-dependent feature must work (degraded, honestly) with no model loaded. No feature may require network access.
**By:** TREE. **Why:** Venue Wi-Fi + one-day model loads are the top demo-killer risks. The demo must never die.
