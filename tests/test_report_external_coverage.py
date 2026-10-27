import csv
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from report_external_coverage import audit

class AuditTests(unittest.TestCase):
    def test_valid_candidate_and_closed_exam_gate(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            directory=root/"external_sources"
            (directory/"example"/"raw").mkdir(parents=True)
            (directory/"example"/"raw"/"P-001.md").write_text("Question",encoding="utf-8")
            with (directory/"curation_queue.csv").open("w",encoding="utf-8",newline="") as file:
                out=csv.DictWriter(file,fieldnames=["id","source","module","license","license_review","answer_verified","semantic_dedup","exam_ready","raw_path"])
                out.writeheader()
                out.writerow({"id":"P-001","source":"example","module":"力学","license":"CC BY 4.0","license_review":"pending","answer_verified":"no","semantic_dedup":"pending","exam_ready":"no","raw_path":"external_sources/example/raw/P-001.md"})
            report=audit(root)
            self.assertEqual(report["raw_candidate_count"],1)
            self.assertEqual(report["by_module"]["力学"],1)
            self.assertEqual(report["exam_ready_external_count"],0)
