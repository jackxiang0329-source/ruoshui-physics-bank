import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import import_hf_physics as hf
from unittest.mock import patch
from urllib.error import HTTPError
import discover_hf_physics as discover
class Tests(unittest.TestCase):
 def test_classes(self):
  self.assertEqual(hf.category("gravitation"),"力学")
  self.assertEqual(hf.category("wave_optics"),"光学")
  self.assertEqual(hf.category("electromagnetism"),"电磁学")
 def test_media_and_dedup(self):
  self.assertIsNone(hf.eligible({"prompt":"Compute the acceleration from Figure 2 and explain what is shown in the diagram."}))
  self.assertEqual(hf.checksum("A   Force"),hf.checksum("a force"))
 def test_resume(self):
  with tempfile.TemporaryDirectory() as d:
   base=Path(d)
   question="A satellite travels in a circular orbit at an altitude of 500 kilometers. Determine the required centripetal acceleration from its orbital velocity."
   def page(offset,length):
    rows=[{"row_idx":i,"row":{"prompt":question if i<2 else question+" Case "+str(i),"domain":"gravitation"}} for i in range(offset,min(offset+length,4))]
    return {"features":[{"name":"prompt"},{"name":"domain"}],"rows":rows,"num_rows_total":4,"partial":False}
   f=lambda:"0"*40
   a=hf.run(100,4,revision_provider=f,page_provider=page,base=base)
   self.assertEqual(a["added_count"],3)
   b=hf.run(100,4,revision_provider=f,page_provider=page,base=base)
   self.assertEqual(b["added_count"],0)
 def test_discovery_restrictions(self):
  with tempfile.TemporaryDirectory() as d:
   report=discover.scan(lambda q:[{"id":"UGPhysics/ugphysics","tags":["license:cc-by-nc-sa-4.0"]}],Path(d)/"hf.json")
   self.assertEqual(report["records"][0]["status"],"NC_restricted_review")

 def test_502_retry_then_resume_without_changing_row_cursor(self):
  class Reply:
   def __enter__(self):return self
   def __exit__(self,*args):return False
   def read(self,n):return b'{"success":true}'
  with patch.object(hf,"urlopen",side_effect=[
          HTTPError("mock",502,"bad gateway",None,None),Reply()]) as opener, patch.object(hf.time,"sleep") as sleeper:
   self.assertEqual(hf.api("https://example.org/rows")["success"],True)
   self.assertEqual(opener.call_count,2)
   self.assertEqual(sleeper.call_count,1)
 def test_404_is_not_retried(self):
  with patch.object(hf,"urlopen",side_effect=HTTPError("mock",404,"missing",None,None)) as opener, patch.object(hf.time,"sleep") as sleeper:
   with self.assertRaises(HTTPError):
    hf.api("https://example.org/not-found")
   self.assertEqual(opener.call_count,1)
   self.assertEqual(sleeper.call_count,0)
