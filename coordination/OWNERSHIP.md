# OWNERSHIP — Who Writes Where

Ownership = "ask this lane before changing it" (in their inbox + a LOG note). It prevents parallel edits and merge wars. Within your own lane, move fast.

| Path | Lane | Owner |
|---|---|---|
| `src/nightshift/orchestrator.py`, `main.py`, approval/receipts | A | TREE |
| `src/nightshift/model.py` | C (client contract by A) | Lane C owner |
| `src/nightshift/watchers.py`, `data/` | B | Lane B owner |
| `src/nightshift/triage.py` | B (with A review) | Lane B owner |
| `src/nightshift/research.py` | C | Lane C owner |
| `src/nightshift/draft.py`, `brief.py` | D (drafting prompts with C) | Lane D owner |
| `outputs/` | — generated, never hand-edit | — |
| `docs/STACK-GB10.md`, `config/` | C | Lane C owner |
| `docs/VISION.md`, `README.md` pitch sections | Lead | TREE / RENE |
| `DEMO.md`, `SUBMISSION.md` | D | Lane D owner |
| `comms/BOARD.md` | Everyone edits *own* section | Lead curates |
| `comms/LOG.md`, `channels/`, `inbox/` | Everyone appends | — |
| `coordination/` | Lead | TREE |

Unclaimed lanes default to TREE until claimed — claim in TASKS.md and this table gets your name.
