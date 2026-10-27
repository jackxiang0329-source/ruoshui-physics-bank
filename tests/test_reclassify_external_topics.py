import sys, tempfile, json, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from reclassify_external_topics import backfill

class ClassificationTests(unittest.TestCase):
 def test_backfill_is_idempotent_and_preserves_review_gate(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)
   for path in ("hf_physics_dpo","college_physics"):
    (root/path).mkdir()
   def write(name,records):
    (root/name/"index.json").write_text(json.dumps({"records":records}),encoding="utf-8")
   write("hf_physics_dpo",[{"id":"HFDPO-00001","domain":"gauss_law","module":"待分类","exam_ready":False},{"id":"HFDPO-00002","domain":"kinetic_theory","module":"待分类","exam_ready":False}])
   write("college_physics",[{"id":"CP-00001","title":"Bernoulli’s Equation","module":"待分类","exam_ready":False},{"id":"CP-00002","title":"Convection","module":"待分类","exam_ready":False}])
   x=backfill(root)
   self.assertEqual(x["sources"]["hf_physics_dpo"]["updated"],2)
   self.assertEqual(x["sources"]["college_physics"]["updated"],2)
   self.assertEqual(backfill(root)["sources"]["hf_physics_dpo"]["updated"],0)
   rec=json.loads((root/"hf_physics_dpo"/"index.json").read_text())
   self.assertEqual(rec["records"][0]["module"],"电磁学")
   self.assertFalse(rec["records"][0]["exam_ready"])
