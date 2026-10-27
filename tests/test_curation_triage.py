import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import curation_triage as triage

class TriageTests(unittest.TestCase):
    def test_license_signal_excludes_noncommercial(self):
        self.assertTrue(triage.permissible_signal("CC BY 4.0 (manual review pending)"))
        self.assertTrue(triage.permissible_signal("CC BY 3.0 Unported"))
        self.assertFalse(triage.permissible_signal("CC BY-NC-SA 4.0"))
        self.assertFalse(triage.permissible_signal("MIT"))
        self.assertFalse(triage.permissible_signal("CC BY 4.0; noncommercial"))
    def test_spread_subjects(self):
        items=[{"module":"力学","id":"A"},{"module":"力学","id":"B"},
               {"module":"光学","id":"C"},{"module":"光学","id":"D"}]
        selected=triage.spread(items, 3)
        self.assertEqual(len({x["module"] for x in selected[:2]}), 2)
    def test_index_digest_collisions(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d)
            for source in ("hf_physics_dpo","college_physics"):
                (base/source).mkdir()
                (base/source/"index.json").write_text(json.dumps({"records":[
                    {"id":source,"question_sha256":"a"*64}]}))
            result=triage.digest_overlaps(base)
            self.assertEqual(result["cross_source_digest_groups"],1)
    def test_human_review_only(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d)/"external_sources"
            (base/"college_physics"/"raw").mkdir(parents=True)
            (base/"college_physics"/"raw"/"CP-00001.md").write_text("Example")
            row={"id":"CP-00001","source":"OpenStax College Physics (historical mirror)",
                 "module":"力学","original_topic":"Displacement","license":"CC BY 3.0 Unported",
                 "author":"OpenStax","source_url":"https://example.org/source",
                 "raw_path":"external_sources/college_physics/raw/CP-00001.md",
                 "exam_ready":"no"}
            with (base/"curation_queue.csv").open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=row.keys());w.writeheader();w.writerow(row)
            result=triage.generate(base)
            self.assertEqual(result["priority_review_count"],1)
            report=(base/"catalog"/"review_priority.csv").read_text(encoding="utf-8-sig")
            self.assertIn("CP-00001",report)
            self.assertIn("semantic_dedup",report)
