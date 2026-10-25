"""Orchestrator — runs the night loop and owns the approval gate + receipts.

Invariants enforced here:
- Drafts are never executed without a queue entry a human approved.
- Every execution (and rejection) appends a receipt.
"""
import json
from datetime import datetime
from pathlib import Path

from . import watchers, triage, research, draft as drafter, brief as briefer
from .model import LocalModel


def _receipt(out_dir, msg):
    line = f"{datetime.now().isoformat(timespec='seconds')} · {msg}"
    with open(Path(out_dir) / "receipts.log", "a") as fh:
        fh.write(line + "\n")
    return line


def run_night(data_dir, docs_dir, out_dir, model=None):
    items = watchers.load_items(data_dir)
    clusters = triage.cluster(items)
    model = model if model is not None else LocalModel()
    entries = []
    for c in clusters:
        findings = research.research(c, docs_dir)
        d = drafter.draft_for(c, findings, model=model)
        entries.append({"cluster": c, "findings": findings, "draft": d})
    queue = briefer.render(entries, out_dir)
    _receipt(out_dir, f"night run: {len(items)} items, {len(clusters)} clusters, "
                      f"{len(queue)} drafts queued, 0 sent")
    return {"items": len(items), "clusters": len(clusters), "queued": len(queue)}


def approve(out_dir, ids=None):
    """Execute approved queue items against local mock systems (receipts only
    in the skeleton) and mark them approved. Returns executed queue ids."""
    out_dir = Path(out_dir)
    queue_path = out_dir / "approval-queue.json"
    queue = json.loads(queue_path.read_text())
    done = []
    for entry in queue:
        if entry["status"] != "pending":
            continue
        if ids is not None and entry["queue_id"] not in ids:
            continue
        entry["status"] = "approved"
        _receipt(out_dir, f"APPROVED {entry['queue_id']} [{entry['topic']}] "
                          f"{entry['kind']} sources={','.join(entry['sources'])}")
        done.append(entry["queue_id"])
    queue_path.write_text(json.dumps(queue, indent=2))
    return done
