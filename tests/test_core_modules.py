"""Direct tests for the pipeline modules that previously only had indirect
coverage through the end to end pipeline tests: watchers (ingest + night
ordering), triage (scoring, red flags, clustering), research (term
extraction + local doc search), draft (per topic drafters + model polish
rules) and the livewatch staging merge, plus the approval gate edge cases
in the orchestrator.

Stdlib only, no network, no model. Run with:
    python3 -m unittest discover tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.nightshift import draft, livewatch, research, triage, watchers
from src.nightshift.orchestrator import approve

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DOCS = ROOT / "data" / "sample" / "docs"


def item(id="X1", source="inbox", time="23:00", subject="Hello",
         body="", topic="general", author="a@b.example"):
    return {"id": id, "source": source, "time": time, "author": author,
            "subject": subject, "body": body, "topic": topic}


class FakeModel:
    """Records polish calls and returns a fixed reply (or None)."""

    def __init__(self, reply="Polished text."):
        self.reply = reply
        self.calls = []

    def complete(self, prompt):
        self.calls.append(prompt)
        return self.reply


# ---------------------------------------------------------------- watchers --

class NightKeyTest(unittest.TestCase):
    def test_evening_times_sort_before_after_midnight(self):
        # The night starts in the evening: 18:00 and 23:59 belong to the
        # evening, 00:30 and 11:59 are the small hours of the same night.
        ordered = sorted(["02:00", "23:59", "12:00", "00:30", "18:00"],
                         key=watchers.night_key)
        self.assertEqual(ordered, ["12:00", "18:00", "23:59", "00:30", "02:00"])

    def test_noon_is_not_shifted_but_morning_is(self):
        self.assertEqual(watchers.night_key("12:00"), 720)
        self.assertEqual(watchers.night_key("11:59"), 719 + 1440)
        self.assertEqual(watchers.night_key("00:00"), 1440)

    def test_unparseable_times_sort_first(self):
        self.assertEqual(watchers.night_key(""), 0)
        self.assertEqual(watchers.night_key("not-a-time"), 0)
        self.assertEqual(watchers.night_key(None), 0)
        self.assertEqual(watchers.night_key("23"), 0)


class LoadItemsTest(unittest.TestCase):
    def _write(self, data_dir, source, rows):
        Path(data_dir, f"{source}.json").write_text(json.dumps(rows))

    def test_missing_source_files_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write(tmp, "inbox", [{"id": "A", "time": "22:00"}])
            items = watchers.load_items(tmp)
            self.assertEqual([i["id"] for i in items], ["A"])
            self.assertEqual(items[0]["source"], "inbox")

    def test_defaults_are_filled_and_source_comes_from_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write(tmp, "tickets", [{"id": "T9", "time": "21:00",
                                          "source": "inbox"}])
            (loaded,) = watchers.load_items(tmp)
            self.assertEqual(loaded["source"], "tickets")
            self.assertEqual(loaded["author"], "unknown")
            self.assertEqual(loaded["subject"], "(no subject)")
            self.assertEqual(loaded["body"], "")
            self.assertEqual(loaded["topic"], "general")

    def test_items_come_back_in_night_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write(tmp, "inbox", [{"id": "LATE", "time": "01:30"},
                                       {"id": "EARLY", "time": "20:00"}])
            self._write(tmp, "incidents", [{"id": "MID", "time": "23:45"}])
            ids = [i["id"] for i in watchers.load_items(tmp)]
            self.assertEqual(ids, ["EARLY", "MID", "LATE"])

    def test_sample_night_loads_every_source(self):
        items = watchers.load_items(ROOT / "data" / "sample")
        self.assertEqual(len(items), 23)
        self.assertEqual({i["source"] for i in items},
                         {"inbox", "tickets", "crm", "incidents"})


# ------------------------------------------------------------------ triage --

class ScoreTest(unittest.TestCase):
    def test_topic_base_scores(self):
        self.assertEqual(triage.score(item(topic="incident")), 50)
        self.assertEqual(triage.score(item(topic="billing")), 30)
        self.assertEqual(triage.score(item(topic="noise")), 0)
        self.assertEqual(triage.score(item(topic="unlisted-topic")), 10)

    def test_urgent_words_add_ten_each_case_insensitive(self):
        scored = triage.score(item(topic="support", subject="OUTAGE",
                                   body="the checkout is down"))
        self.assertEqual(scored, 20 + 10 + 10)

    def test_incidents_source_gets_a_bonus(self):
        base = triage.score(item(topic="support"))
        boosted = triage.score(item(topic="support", source="incidents"))
        self.assertEqual(boosted, base + 20)

    def test_score_is_capped_at_100(self):
        loud = item(topic="incident", source="incidents",
                    subject=" ".join(triage.URGENT_WORDS),
                    body=" ".join(triage.URGENT_WORDS))
        self.assertEqual(triage.score(loud), 100)


class RedFlagsTest(unittest.TestCase):
    def test_flags_come_back_in_word_list_order(self):
        flagged = triage.red_flags_for(item(
            subject="We will cancel", body="and file a lawsuit"))
        self.assertEqual(flagged, ["cancel", "lawsuit"])

    def test_matching_is_case_insensitive_and_searches_the_body(self):
        flagged = triage.red_flags_for(item(
            subject="Invoice question", body="Please REFUND this charge"))
        self.assertEqual(flagged, ["refund"])

    def test_benign_item_has_no_flags(self):
        self.assertEqual(triage.red_flags_for(item(
            subject="Thanks", body="all good here")), [])


class ClusterTest(unittest.TestCase):
    def test_items_group_by_topic_and_general_stays_singleton(self):
        items = [item(id="B1", topic="billing", time="22:00"),
                 item(id="B2", topic="billing", time="22:30"),
                 item(id="G1", topic="general"),
                 item(id="G2", topic="general")]
        clusters = triage.cluster(items)
        by_topic = {c["topic"]: c for c in clusters}
        self.assertEqual(len(by_topic["billing"]["items"]), 2)
        generals = [c for c in clusters if c["topic"] == "general"]
        self.assertEqual(len(generals), 2)
        self.assertTrue(all(len(c["items"]) == 1 for c in generals))

    def test_cluster_urgency_is_the_max_member_score(self):
        items = [item(id="S1", topic="support", subject="question"),
                 item(id="S2", topic="support", subject="urgent outage")]
        (cluster,) = triage.cluster(items)
        self.assertEqual(cluster["urgency"], triage.score(items[1]))

    def test_clusters_sort_by_urgency_and_items_by_night_order(self):
        items = [item(id="LOW", topic="noise", time="21:00"),
                 item(id="HI2", topic="incident", time="01:00"),
                 item(id="HI1", topic="incident", time="22:00")]
        clusters = triage.cluster(items)
        self.assertEqual(clusters[0]["topic"], "incident")
        self.assertEqual([i["id"] for i in clusters[0]["items"]],
                         ["HI1", "HI2"])

    def test_cluster_red_flags_are_the_sorted_union(self):
        items = [item(id="A", topic="sales", body="we will cancel"),
                 item(id="B", topic="sales", body="a refund please")]
        (cluster,) = triage.cluster(items)
        self.assertEqual(cluster["red_flags"], ["cancel", "refund"])


# ---------------------------------------------------------------- research --

class ExtractTermsTest(unittest.TestCase):
    def test_stopwords_short_words_and_case_are_normalised(self):
        terms = research._extract_terms(
            "The customer would please reply about the Webhook Queue")
        self.assertEqual(terms, {"webhook", "queue"})

    def test_punctuation_is_stripped_from_term_edges(self):
        terms = research._extract_terms('Checkout, failed. "Payments" (again):')
        self.assertEqual(terms, {"checkout", "failed", "payments"})


class SearchTest(unittest.TestCase):
    def _docs(self, tmp, files):
        docs = Path(tmp)
        for name, text in files.items():
            (docs / name).write_text(text)
        return docs

    def test_missing_or_empty_docs_dir_returns_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(research.search(Path(tmp, "nope"), ["payments"]), [])
            self.assertEqual(research.search(tmp, ["payments"]), [])

    def test_strong_match_returns_doc_line_and_term_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = self._docs(tmp, {
                "runbook.md": "Payments webhook queue\nRestart the workers\n",
                "other.md": "Lunch menu for the office kitchen\n",
            })
            findings = research.search(docs, ["payments", "webhook", "queue"])
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0]["doc"], "runbook.md")
            self.assertEqual(findings[0]["line"], "Payments webhook queue")
            self.assertEqual(findings[0]["term_matches"], 3)
            self.assertGreaterEqual(findings[0]["quality"],
                                    research.MIN_QUALITY)

    def test_unrelated_query_finds_nothing_above_the_threshold(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = self._docs(tmp, {"a.md": "alpha bravo charlie delta\n"})
            self.assertEqual(research.search(docs, ["zebra", "xylophone"]), [])

    def test_limit_and_quality_ordering(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = self._docs(tmp, {
                "best.md": "payments webhook queue saturation\n",
                "mid.md": "payments queue\npayments webhook\n",
                "weak.md": "payments\n",
            })
            findings = research.search(
                docs, ["payments", "webhook", "queue"], limit=2)
            self.assertEqual(len(findings), 2)
            self.assertEqual(findings[0]["doc"], "best.md")
            qualities = [f["quality"] for f in findings]
            self.assertEqual(qualities, sorted(qualities, reverse=True))

    def test_sample_docs_answer_an_incident_cluster(self):
        cluster = {"topic": "incident", "items": [
            item(subject="Payments returning 502 at checkout",
                 body="webhook errors for customers")]}
        findings = research.research(cluster, SAMPLE_DOCS)
        self.assertTrue(findings)
        self.assertEqual(findings[0]["doc"], "runbook-payments.md")


# ------------------------------------------------------------------- draft --

def cluster(topic, *members):
    return {"topic": topic, "items": list(members)}


class DraftTopicsTest(unittest.TestCase):
    def test_incident_draft_counts_only_customer_facing_items(self):
        c = cluster("incident",
                    item(id="I1", source="incidents", time="23:00",
                         subject="502s at checkout"),
                    item(id="C1", source="inbox", time="23:20"),
                    item(id="C2", source="tickets", time="23:40"))
        d = draft.draft_for(c, [])
        self.assertEqual(d["kind"], "Incident update to 2 affected customers")
        self.assertIn("our internal runbook", d["text"])
        self.assertEqual(d["sources"], ["I1", "C1", "C2"])

    def test_incident_without_customers_is_a_summary(self):
        c = cluster("incident",
                    item(id="I1", source="incidents", time="23:00",
                         subject="502s at checkout"))
        self.assertEqual(draft.draft_for(c, [])["kind"], "Incident summary")

    def test_incident_draft_cites_a_strong_finding(self):
        c = cluster("incident",
                    item(id="I1", source="incidents", subject="502s"))
        d = draft.draft_for(c, [{"doc": "runbook-payments.md", "line": "x",
                                  "quality": 0.5}])
        self.assertIn("runbook-payments.md", d["text"])

    def test_remaining_topic_kinds(self):
        cases = {"billing": "Reply to billing report",
                 "sales": "Follow-up draft",
                 "noise": "No action"}
        for topic, kind in cases.items():
            with self.subTest(topic=topic):
                d = draft.draft_for(cluster(topic, item()), [])
                self.assertEqual(d["kind"], kind)

    def test_crm_draft_uses_singular_for_one_record(self):
        d = draft.draft_for(cluster("crm-hygiene", item()), [])
        self.assertIn("1 record look", d["text"])
        d2 = draft.draft_for(cluster("crm-hygiene", item(), item(id="X2")), [])
        self.assertIn("2 records look", d2["text"])

    def test_unknown_topic_falls_back_to_acknowledgement(self):
        d = draft.draft_for(cluster("mystery", item(subject="Hello there.")), [])
        self.assertEqual(d["kind"], "Acknowledgement")
        self.assertIn('"Hello there"', d["text"])


class DraftModelPolishTest(unittest.TestCase):
    def test_model_polish_replaces_text_but_keeps_kind_and_sources(self):
        model = FakeModel()
        d = draft.draft_for(cluster("billing", item()), [], model=model)
        self.assertEqual(d["text"], "Polished text.")
        self.assertEqual(d["kind"], "Reply to billing report")
        self.assertEqual(d["sources"], ["X1"])
        self.assertEqual(len(model.calls), 1)

    def test_model_returning_none_keeps_the_template(self):
        model = FakeModel(reply=None)
        d = draft.draft_for(cluster("billing", item()), [], model=model)
        self.assertIn("finance review", d["text"])

    def test_noise_is_never_polished(self):
        model = FakeModel()
        d = draft.draft_for(cluster("noise", item()), [], model=model)
        self.assertEqual(model.calls, [])
        self.assertEqual(d["text"], "Filed as low priority. No draft needed.")


# --------------------------------------------------------------- livewatch --

class StageTest(unittest.TestCase):
    def test_stage_merges_exports_and_single_item_drops(self):
        with tempfile.TemporaryDirectory() as tmp:
            watch, stage_dir = Path(tmp, "watch"), Path(tmp, "stage")
            watch.mkdir()
            (watch / "inbox.json").write_text(json.dumps(
                [{"id": "E1", "source": "inbox"}]))
            (watch / "one.item.json").write_text(json.dumps(
                {"id": "D1", "source": "tickets"}))
            (watch / "two.item.json").write_text(json.dumps({"id": "D2"}))
            count = livewatch.stage(watch, stage_dir)
            self.assertEqual(count, 3)
            inbox = json.loads((stage_dir / "inbox.json").read_text())
            tickets = json.loads((stage_dir / "tickets.json").read_text())
            self.assertEqual([r["id"] for r in inbox], ["E1", "D2"])
            self.assertEqual([r["id"] for r in tickets], ["D1"])
            # Every known source gets a file, even when empty, so the
            # loader downstream sees a complete data dir.
            for source in watchers.SOURCES:
                self.assertTrue((stage_dir / f"{source}.json").exists())

    def test_snapshot_changes_when_a_file_is_dropped(self):
        with tempfile.TemporaryDirectory() as tmp:
            watch = Path(tmp)
            before = livewatch._snapshot(watch)
            (watch / "new.item.json").write_text("{}")
            after = livewatch._snapshot(watch)
            self.assertNotEqual(before, after)
            self.assertIn("new.item.json", after)


# ------------------------------------------------------------- approve gate --

class ApproveEdgeCasesTest(unittest.TestCase):
    def _queue_dir(self, tmp, statuses=("pending", "pending")):
        out = Path(tmp)
        queue = [{"queue_id": f"Q{n}", "topic": "billing", "kind": "Reply",
                  "text": "t", "sources": ["X1"], "status": s}
                 for n, s in enumerate(statuses, 1)]
        (out / "approval-queue.json").write_text(json.dumps(queue))
        return out

    def test_approve_with_no_ids_approves_everything_pending(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._queue_dir(tmp)
            self.assertEqual(approve(out), ["Q1", "Q2"])
            receipts = (out / "receipts.log").read_text()
            self.assertEqual(receipts.count("APPROVED"), 2)

    def test_approve_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._queue_dir(tmp)
            approve(out, ids=["Q1"])
            self.assertEqual(approve(out, ids=["Q1"]), [])
            after = json.loads((out / "approval-queue.json").read_text())
            self.assertEqual([q["status"] for q in after],
                             ["approved", "pending"])

    def test_unknown_ids_approve_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._queue_dir(tmp)
            self.assertEqual(approve(out, ids=["Q99"]), [])
            after = json.loads((out / "approval-queue.json").read_text())
            self.assertTrue(all(q["status"] == "pending" for q in after))

    def test_already_approved_entries_are_left_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._queue_dir(tmp, statuses=("approved", "pending"))
            self.assertEqual(approve(out), ["Q2"])


if __name__ == "__main__":
    unittest.main()
