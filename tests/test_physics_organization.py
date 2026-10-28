import csv
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import materialize_zh_drafts as localize
import organize_physics_catalog as catalog

class OrganizationTests(unittest.TestCase):
    def test_english_digest(self):
        self.assertEqual(localize.digest("Kinetic  Energy"),localize.digest("kinetic energy"))
        self.assertEqual(localize.original("# PREF-00001 · conceptual\n\nQuestion.\n\n---\nSource: X"),"Question.")

    def test_chapter_map(self):
        t=json.loads((ROOT/"taxonomy/physics_taxonomy.json").read_text(encoding="utf-8"))
        self.assertEqual(28,len(t["refresher_lessons"]))
        self.assertEqual(28,len({x["source_path"] for x in t["refresher_lessons"]}))

    def test_two_source_type_corrections(self):
        cfg=catalog.configs(ROOT)
        for pid in ("PREF-00011","PREF-00019"):
            row={"id":pid,"module":"物理基础","source":"Physics Refresher (CC BY 4.0)",
                 "raw_path":"external_sources/physics_refresher/raw/"+pid+".md"}
            result=catalog.classify(row,cfg,ROOT)
            self.assertEqual("概念辨析题",result["题型"])
            self.assertEqual("否",result["组卷资格"])

    def test_drafts_and_full_index(self):
        a=localize.create(ROOT)
        self.assertGreaterEqual(a["translated_drafts"],88)
        b=catalog.generate(ROOT)
        self.assertGreaterEqual(b["candidate_total"],17000)
        self.assertEqual(a["translated_drafts"],b["translated_drafts"])
        self.assertEqual(0,b["approved_external"])
        with (ROOT/"external_sources/catalog/题目总索引.csv").open(encoding="utf-8-sig",newline="") as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),b["candidate_total"])
        self.assertTrue(all(r["组卷资格"]=="否" for r in rows))

if __name__=="__main__":
    unittest.main()
