import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from check_tex_controls import invisible,nested_strings
class ControlTests(unittest.TestCase):
 def test_vertical_tab_rejected(self):
  self.assertEqual(invisible("x\x0barepsilon"),[(1,11)])
  self.assertEqual(invisible("a\nb\tc"),[])
 def test_nested_json(self):
  parts=list(nested_strings({"choices":[["A","x\x0bhere"]]}))
  self.assertTrue(any(invisible(x) for x in parts))
