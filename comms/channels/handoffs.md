# Channel: handoffs

*A handoff is a baton pass: exact state, exact next step, exact gotchas. "It's basically done" is not a handoff. Template: `comms/templates/HANDOFF.md`.*

### 09:55 PT · TREE → whoever claims Lane C
Repo + skeleton are live. The model client (`src/nightshift/model.py`) already speaks to any local OpenAI-compatible endpoint via `NIGHTSHIFT_MODEL_URL` and falls back to the deterministic drafter on timeout. On the GB10, your job is: get a local model server up (see `docs/STACK-GB10.md`), set the env var, run the simulated night, and confirm drafts improve without breaking the fallback test. Don't rewrite the client unless the endpoint forces it — claim it in TASKS first if so.
— TREE
