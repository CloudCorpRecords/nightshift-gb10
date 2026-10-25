"""Briefer agent — renders the morning brief + the approval queue.

The brief is the product's main interface: what happened, what matters,
what's drafted, what needs a human decision. The queue is machine-readable
so the approval gate (orchestrator.approve) executes exactly what was shown.
"""
import json
from pathlib import Path


def render(clusters_with_drafts, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = ["# Morning Brief — NightShift", "",
             "_Generated locally. Nothing was sent overnight. "
             "Everything below is a draft awaiting approval._", ""]
    queue = []
    for n, entry in enumerate(clusters_with_drafts, 1):
        c, findings, draft = entry["cluster"], entry["findings"], entry["draft"]
        lines.append(f"## {n}. [{c['topic']}] urgency {c['urgency']}/100 — "
                     f"{len(c['items'])} item(s)")
        for i in c["items"]:
            lines.append(f"- {i['time']} · {i['source']} · {i['author']}: {i['subject']}")
        for f in findings:
            lines.append(f"- Research (local doc `{f['doc']}`): {f['line']}")
        lines.append(f"- **Draft — {draft['kind']}:** {draft['text']}")
        lines.append("")
        if c["topic"] != "noise":
            queue.append({"queue_id": f"Q{n}", "topic": c["topic"],
                          "kind": draft["kind"], "text": draft["text"],
                          "sources": draft["sources"], "status": "pending"})
    (out_dir / "morning-brief.md").write_text("\n".join(lines))
    (out_dir / "approval-queue.json").write_text(json.dumps(queue, indent=2))
    return queue
