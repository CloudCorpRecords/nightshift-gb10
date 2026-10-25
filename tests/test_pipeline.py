import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.nightshift.orchestrator import run_night, approve
from src.nightshift.model import LocalModel

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sample"


class PipelineTest(unittest.TestCase):
    def test_night_run_produces_brief_and_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_night(DATA, DATA / "docs", tmp, model=LocalModel(url=""))
            self.assertEqual(result["items"], 23)
            brief = Path(tmp, "morning-brief.md").read_text()
            self.assertIn("Morning Brief", brief)
            self.assertIn("incident", brief.lower())
            queue = json.loads(Path(tmp, "approval-queue.json").read_text())
            self.assertTrue(queue)
            # incident cluster must sort first by urgency
            self.assertEqual(queue[0]["topic"], "incident")
            self.assertTrue(Path(tmp, "receipts.log").exists())

    def test_approval_gate_executes_only_approved(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_night(DATA, DATA / "docs", tmp, model=LocalModel(url=""))
            queue = json.loads(Path(tmp, "approval-queue.json").read_text())
            done = approve(tmp, ids=[queue[0]["queue_id"]])
            self.assertEqual(done, [queue[0]["queue_id"]])
            after = json.loads(Path(tmp, "approval-queue.json").read_text())
            self.assertEqual(after[0]["status"], "approved")
            self.assertTrue(all(q["status"] == "pending" for q in after[1:]))

    def test_model_fallback_when_endpoint_dead(self):
        model = LocalModel(url="http://127.0.0.1:9")
        self.assertIsNone(model.complete("anything"))


if __name__ == "__main__":
    unittest.main()
