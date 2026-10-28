import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import college_tex_draft as d
class CollegeDraftTests(unittest.TestCase):
 def test_mathml_tokens_and_degrees(self):
  raw='<math xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mtext>60</mtext><mtext>.</mtext><mn>0</mn><mspace width="0.25em"/><mtext>Hz</mtext></mrow><annotation>DO NOT COPY</annotation></semantics></math>'
  tex,issues=d.mathml_to_tex(raw)
  self.assertEqual(issues,[])
  self.assertIn("60.0",tex)
  self.assertIn(r"\mathrm{Hz}",tex)
  self.assertNotIn("DO NOT COPY",tex)
 def test_fraction_and_power(self):
  raw="<math><mfrac><mn>1</mn><msup><mi>t</mi><mn>2</mn></msup></mfrac></math>"
  tex,issues=d.mathml_to_tex(raw)
  self.assertEqual(tex,r"\frac{1}{{t}^{2}}")
  self.assertEqual(issues,[])
 def test_unknown_math_is_flagged(self):
  tex,issues=d.mathml_to_tex("<math><mtable><mtr><mtd><mn>1</mn></mtd></mtr></mtable></math>")
  self.assertIn("unsupported_mathml:mtable",issues)
  self.assertIn("[CHECK MATH]",tex)
 def test_safe_nonmath_escape(self):
  tex,issues,n=d.render_question("Find $20 of x_0 at <math><mn>3</mn></math> seconds.")
  self.assertEqual(n,1)
  self.assertIn(r"\$20",tex)
  self.assertIn(r"x\_0",tex)
  self.assertEqual(issues,[])

 def test_generates_standalone_editorial_xelatex_wrapper(self):
  import csv, tempfile
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   cat=root/"external_sources"/"catalog";cat.mkdir(parents=True)
   raw=root/"external_sources"/"college_physics"/"raw";raw.mkdir(parents=True)
   (raw/"CP-00001.md").write_text("# The Sample\n\nWhat is the period of <math><mn>3</mn></math> Hz electrical power?\n\n---\nAttribution",encoding="utf-8")
   with (cat/"review_priority.csv").open("w",newline="",encoding="utf-8") as f:
    writer=csv.DictWriter(f,fieldnames=["id","source","module","original_topic","source_url","raw_path","exam_ready"])
    writer.writeheader()
    writer.writerow({"id":"CP-00001","source":"OpenStax College Physics (historical mirror)","module":"振动与波动","original_topic":"Oscillations","source_url":"https://github.com/philschatz/physics-book/blob/main/contents/m42033.md","raw_path":"external_sources/college_physics/raw/CP-00001.md","exam_ready":"no"})
   z=d.build(root)
   self.assertEqual(z["question_count"],1)
   wrapper=(cat/"college_review_preview.tex").read_text()
   snippets=(cat/"college_review_tex_draft.tex").read_text()
   self.assertIn(r"\documentclass[UTF8,11pt]{ctexart}",wrapper)
   self.assertIn("NOT EXAM READY",wrapper)
   self.assertIn(r"\input{college_review_tex_draft.tex}",wrapper)
   self.assertIn(r"\href{https://github.com/philschatz/physics-book/blob/main/contents/m42033.md}{Original chapter}",snippets)
   self.assertEqual(z["exam_ready_added"],0)
