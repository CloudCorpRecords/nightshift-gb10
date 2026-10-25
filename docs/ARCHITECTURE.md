# Architecture

```
        ┌──────────────────── Dell Pro Max with GB10 (one box, offline-capable) ───────────────────┐
        │                                                                                            │
  data/ │   ┌─────────┐   ┌─────────┐   ┌────────────┐   ┌─────────┐   ┌─────────┐                   │
 inbox ─┼──▶│ Watcher │──▶│ Triager │──▶│ Researcher │──▶│ Drafter │──▶│ Briefer │──▶ morning brief  │
 tickets│   └─────────┘   └─────────┘   └────────────┘   └─────────┘   └────┬────┘    + approval queue│
 logs ──┼──▶  ingest       cluster/     local docs       drafts only       │                          │
 crm ───┘                  urgency      (runbooks)       (never sends)     ▼                          │
        │                                                    ┌──────────────────┐                     │
        │   Orchestrator: night loop, scheduling, ──────────▶│ APPROVAL GATE  │ human approves      │
        │   receipts log, model fallback                     └───────┬──────────┘                     │
        │                                                            ▼ approved actions only        │
        │                                                    mock systems (local files) + receipts    │
        │                                                                                            │
        │   Model layer: local OpenAI-compatible endpoint (GB10) ⇄ deterministic fallback          │
        │   Runtime: OpenClaw loop · Framework: NemoClaw · Sandbox/policy: OpenShell (egress deny)  │
        └────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Data flow (one night)

1. Watchers load new items from `data/sample/` (demo) or `data/incoming/` (live file-drop) into a common `Item` shape: `{id, source, time, author, subject, body, raw}`.
2. Triager dedupes (same subject/author clustering), scores urgency (keywords + source + age rules; model assist if available), and links related items into `Cluster`s (e.g. incident ↔ tickets ↔ emails).
3. Researcher searches local docs (`data/sample/docs/`) for each cluster — keyword retrieval in the skeleton; Lane C upgrades to local embeddings. Answers carry doc citations.
4. Drafter produces one draft per actionable cluster: reply, incident summary, or CRM update note. **Drafts only.** Each draft cites its source items.
5. Briefer renders `outputs/morning-brief.md` (what happened, what matters, drafts) + `outputs/approval-queue.json`.
6. Approval: `main.py approve` executes approved items against local mock outboxes/CRMs and appends to `outputs/receipts.log`. Rejected items are logged too — receipts cover decisions, not just actions.

## Design invariants

- **Offline**: no socket in the product path except `localhost` model endpoint. OpenShell policy enforces egress-deny at demo time.
- **Deterministic core**: triage/research/draft all have rule-based implementations; the local LLM (when present) *enhances* draft text via `model.py` with timeout + fallback.
- **Stdlib skeleton**: the core runs on bare Python 3 — zero install risk on the GB10. Extra deps only inside Lane C upgrades, isolated and optional.
- **Receipts**: every stage appends structured lines the Briefer can quote. Auditability is a feature, not debug output.
