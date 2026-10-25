"""B3 tests — MIKE-SNOOCH, TASKS #B3, LOG MSG-0030."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "generate_spike", ROOT / "scripts" / "generate_spike.py")
generate_spike_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(generate_spike_mod)


class SpikeTest(unittest.TestCase):
    def test_six_p0_items_one_per_minute(self):
        items = generate_spike_mod.generate_spike(6, "02:14", "payments")
        self.assertEqual(len(items), 6)
        self.assertEqual([i["time"] for i in items],
                         ["02:14", "02:15", "02:16", "02:17", "02:18", "02:19"])
        self.assertTrue(all(i["priority"] == "P0" for i in items))
        self.assertTrue(all(i["topic"] == "incident" for i in items))
        self.assertTrue(all(i["thread_id"] == "payments-outage" for i in items))

    def test_livewatch_stage_counts_spike(self):
        from src.nightshift.livewatch import stage
        with tempfile.TemporaryDirectory() as tmp:
            watch = Path(tmp) / "live"
            watch.mkdir()
            items = generate_spike_mod.generate_spike(6, "02:14", "payments")
            (watch / "incidents.json").write_text(json.dumps(items))
            self.assertEqual(stage(str(watch), str(Path(tmp) / "staging")), 6)


if __name__ == "__main__":
    unittest.main()
