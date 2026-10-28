import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import import_college_physics as cp
import audit_college_corpus as audit

class FullCorpusAuditTests(unittest.TestCase):
 def sample(self,root,corrupt=False):
  base=root/"external_sources"
  raw=base/"college_physics"/"raw";raw.mkdir(parents=True)
  folder=base/"catalog";folder.mkdir(parents=True)
  entries=[]
  for i in (1,2):
   pid=f"CP-{i:05d}"
   question=("A block of mass 5 kilograms moves at a speed of 3 meters per second. "
             "Calculate its linear momentum and state the SI units of the answer. "
             + ("Use 7 kilograms instead." if i==2 else "Assume inertial motion."))
   digest=hashlib.sha256(cp.norm(question).encode()).hexdigest()
   sha="a"*40
   content=f"# Momentum — {pid}\n\n{question}\n\n---\nAttribution: OpenStax College, *College Physics* (2014); CC BY 3.0 Unported.\nGit source blob SHA: {sha}\n"
   (raw/(pid+".md")).write_text(content,encoding="utf-8")
   entries.append({"id":pid,"title":"Momentum","module":"力学",
                   "question_type":"calculation","source_url":"https://example.org",
                   "source_sha":sha,"source_revision":cp.REV,
                   "license":"CC BY 3.0 Unported","exam_ready":False,
                   "answer_verified":False,
                   "question_sha256":("b"*64 if i==2 and corrupt else digest)})
  (base/"college_physics"/"index.json").write_text(json.dumps({"count":2,"records":entries}))
  return base
 def test_all_source_rows_and_review_queue(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);self.sample(root)
   report=audit.audit(root)
   self.assertEqual(report["total_corpus_candidates"],2)
   self.assertEqual(report["next_manual_review_count"],2)
   self.assertEqual(report["total_raw_file_integrity_mismatches"],0)
   worklist=(root/"external_sources"/"catalog"/"college_next_review.csv").read_text(encoding="utf-8-sig")
   self.assertIn("CP-00002",worklist)
   self.assertIn("verify_physics_and_solution",worklist)
 def test_tampered_question_hash_blocks_audit(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);self.sample(root,corrupt=True)
   with self.assertRaisesRegex(ValueError,"Source corpus integrity failed"):
    audit.audit(root)
 def test_numeric_template_is_not_semantic_dedup(self):
  a="An airplane flies 45 kilometers north before travelling 31 kilometers west in steady motion"
  b="An airplane flies 56 kilometers north before travelling 27 kilometers west in steady motion"
  self.assertEqual(audit.number_template(a),audit.number_template(b))
