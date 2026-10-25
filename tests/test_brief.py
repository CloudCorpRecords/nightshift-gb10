import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.nightshift import brief, draft
from src.nightshift.model import LocalModel
from src.nightshift.orchestrator import run_night

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sample"


def _cluster(topic, *items):
    return {"topic": topic, "urgency": 20,
            "items": [{"id": f"X{n}", "source": "inbox", "time": "03:00", "author": "a@b.example",
                       "subject": s, "body": "", "topic": topic} for n, s in enumerate(items)]}


class BriefTest(unittest.TestCase):
    def test_brief_has_summary_queue_table_and_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_night(DATA, DATA / "docs", tmp, model=LocalModel(url=""))
            md = Path(tmp, "morning-brief.md").read_text()
            queue = json.loads(Path(tmp, "approval-queue.json").read_text())
            self.assertIn("## At a glance", md)
            self.assertIn("## Approval queue", md)
            self.assertIn("| Sent | 0 |", md)
            for q in queue:  # every queued draft is in the table and has a section
                self.assertIn(f"| {q['queue_id']} |", md)
                self.assertIn(f"approve --ids {q['queue_id']}`", md)
            html = Path(tmp, "morning-brief.html").read_text()
            self.assertTrue(html.startswith("<!doctype html>"))
            self.assertIn('id="Q1"', html)
            self.assertIn("Nothing was sent overnight", html)

    def test_weak_findings_are_not_cited(self):
        entries = [{"cluster": _cluster("support", "Login loop"),
                    "findings": [{"doc": "unrelated.md", "line": "- noise line", "hits": 1}],
                    "draft": {"kind": "Support reply", "text": "t", "sources": ["X0"]}}]
        b = brief.build(entries)
        self.assertEqual(b["sections"][0]["findings"], [])
        self.assertNotIn("unrelated.md", brief.render_markdown(b))

    def test_noise_has_no_queue_entry(self):
        entries = [{"cluster": _cluster("noise", "Newsletter"), "findings": [],
                    "draft": {"kind": "No action", "text": "t", "sources": ["X0"]}}]
        b = brief.build(entries)
        self.assertEqual(b["queue"], [])
        self.assertIn("Filed as noise", brief.render_markdown(b))


class DraftTest(unittest.TestCase):
    def test_general_items_get_an_acknowledgement_not_a_fix(self):
        d = draft.draft_for(_cluster("general", "Feature request: export to CSV"), [])
        self.assertEqual(d["kind"], "Acknowledgement")
        self.assertNotIn("fix", d["text"].lower())
        self.assertIn('"Feature request: export to CSV"', d["text"])

    def test_support_claims_a_fix_only_with_a_strong_finding(self):
        c = _cluster("support", "Can't log in since yesterday")
        weak = draft.draft_for(c, [{"doc": "support-macros.md", "line": "x", "hits": 1}])
        self.assertIn("looking into it", weak["text"])
        strong = draft.draft_for(c, [{"doc": "support-macros.md", "line": "x", "hits": 3}])
        self.assertIn("support-macros.md", strong["text"])
        self.assertIn('"Can\'t log in since yesterday"', strong["text"])

    def test_drafts_keep_sources(self):
        c = _cluster("billing", "Charged twice", "Duplicate charge")
        d = draft.draft_for(c, [])
        self.assertEqual(d["sources"], ["X0", "X1"])


if __name__ == "__main__":
    unittest.main()
