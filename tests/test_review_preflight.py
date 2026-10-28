import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import review_preflight as p
class PreflightTests(unittest.TestCase):
    def test_ubc_answer_flagged_and_not_misread_from_yaml(self):
        raw="---\ntitle: Demo\n---\n# Motion\nA plane travels {{params.x}} km.\n## Part 1\nFind the distance and direction.\n### Answer Section\n- 2 km\n## Attribution\nCC BY 4.0"
        part=p.question_part(raw,"UBC OPBP")
        self.assertNotIn("title: Demo",part)
        flags=p.inspect(part,"UBC OPBP")["risk_flags"]
        self.assertIn("parameter_template",flags)
        self.assertIn("embedded_answer_section",flags)
    def test_mathml_and_figure_are_manual(self):
        q="<math><mfrac><mn>1</mn><mn>2</mn></mfrac></math> Calculate acceleration using Figure 4."
        x=p.inspect(q,"OpenStax College Physics (historical mirror)")
        self.assertIn("mathml_requires_conversion",x["risk_flags"])
        self.assertIn("media_or_figure_reference",x["risk_flags"])
    def test_contextual_dependent_exercises_are_flagged(self):
        q="The same cart as Problem 1 is now accelerated. Find its new speed given an additional net force."
        self.assertIn("cross_reference",p.inspect(q,"Physics Refresher (CC BY 4.0)")["risk_flags"])
    def test_clean_still_requires_manual_review(self):
        q="Give an example distinguishing total distance travelled from displacement over a closed path and explain the difference."
        self.assertEqual(p.inspect(q,"OpenStax")["review_complexity"],"standard_manual_review")
    def test_worklist_generation_and_near_text_signal(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);ext=root/"external_sources";(ext/"catalog").mkdir(parents=True)
            (ext/"college_physics"/"raw").mkdir(parents=True)
            q="Explain how conservation of momentum applies to two identical moving bodies in an isolated system during a one-dimensional elastic collision with equal masses and initial velocities."
            for i in [1,2]:
                (ext/"college_physics"/"raw"/f"CP-{i:05d}.md").write_text(
                    f"# Test\n\n{q}\n\n---\nSource: CC BY 3.0")
            with (ext/"curation_queue.csv").open("w") as f:f.write("")
            with (ext/"catalog"/"review_priority.csv").open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=["id","source","module","original_topic","raw_path","pending_checks","exam_ready"])
                w.writeheader()
                for i in [1,2]:
                    w.writerow({"id":f"CP-{i:05d}","source":"OpenStax College Physics (historical mirror)","module":"力学","original_topic":"Collision","raw_path":f"external_sources/college_physics/raw/CP-{i:05d}.md","pending_checks":"rights_chain","exam_ready":"no"})
            a=p.run(root)
            self.assertEqual(a["total_reviewed_by_static_checks"],2)
            self.assertEqual(len(a["near_textual_duplicate_pairs"]),1)
            self.assertEqual(a["exam_ready_added"],0)
