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

    def test_red_flags_surface_in_brief(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_night(DATA, DATA / "docs", tmp, model=LocalModel(url=""))
            brief = Path(tmp, "morning-brief.md").read_text()
            # sample night has a "charged twice" billing item -> red flag
            self.assertIn("Red flags", brief)
            self.assertIn("charged twice", brief)

    def test_live_watch_rebuilds_on_drop(self):
        from src.nightshift.livewatch import rebuild
        with tempfile.TemporaryDirectory() as tmp:
            watch_dir = Path(tmp, "live")
            watch_dir.mkdir()
            (watch_dir / "drop1.item.json").write_text(json.dumps({
                "id": "L1", "source": "inbox", "time": "23:15",
                "author": "ceo@bigco.example", "subject": "We will cancel",
                "body": "Unless this is fixed tonight we will cancel the "
                        "contract and switch to a competitor.",
                "topic": "sales"}))
            out = Path(tmp, "out")
            result = rebuild(watch_dir, Path(tmp, "stage"), DATA / "docs", out)
            self.assertEqual(result["items"], 1)
            brief = Path(out, "morning-brief.md").read_text()
            self.assertIn("cancel", brief)
            self.assertIn("Red flags", brief)


if __name__ == "__main__":
    unittest.main()
