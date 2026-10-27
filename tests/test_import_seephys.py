import sys, json, unittest, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import import_seephys as sp
class SeePhysTests(unittest.TestCase):
    def test_excludes_images_and_references(self):
        self.assertIsNone(sp.valid({"question":"Examine Figure 2 and calculate the net acceleration from the graph of force against time.", "images":[]}))
        self.assertIsNone(sp.valid({"question":"Find the force on an object traveling around a circular path at a fixed speed.","images":[{"src":"fake"}]}))
        self.assertTrue(sp.valid({"question":"Calculate the force on a charged particle moving at a constant speed in a uniform magnetic field.", "images":[]}))
    def test_topic(self):
        self.assertEqual(sp.topic("quantum physics"),"近代物理")
        self.assertEqual(sp.topic("electromagnetism"),"电磁学")
    def test_offline_cursor_and_cross_source_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            doc={"question":"Calculate the acceleration of a falling mass subject only to uniform gravity near the surface of a planet.","images":[],"subject":"classical mechanics","level":5}
            def page(offset,count):
                rows=[{"row_idx":i,"row":doc if i<2 else {**doc,"question":doc["question"]+" Case "+str(i)}} for i in range(offset,min(offset+count,3))]
                return {"partial":False,"features":[{"name":"question"},{"name":"images"},{"name":"subject"}],"num_rows_total":3,"rows":rows}
            ver=lambda:"a"*40
            first=sp.run(100,10,version_getter=ver,page_getter=page,base=root)
            self.assertEqual(first["added_count"],2)
            second=sp.run(100,10,version_getter=ver,page_getter=page,base=root)
            self.assertEqual(second["added_count"],0)
