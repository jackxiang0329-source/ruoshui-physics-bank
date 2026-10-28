import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from import_college_physics import group
from reclassify_external_topics import backfill

class EditorialClassificationTests(unittest.TestCase):
    def test_title_radiation_is_ambiguous(self):
        self.assertEqual(group("Radiation"), "待分类")
        self.assertEqual(group("Thermal Radiation"), "热学")

    def test_contextual_exceptions_are_idempotent_and_safe(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "college_physics" / "index.json"
            target.parent.mkdir(parents=True)
            source = [
                {"id": "CP-00898", "title": "Radiation",
                 "module": "近代物理", "exam_ready": False},
                {"id": "CP-00080", "title": "Problem-Solving Strategies",
                 "module": "物理基础", "exam_ready": False},
                {"id": "CP-99999", "title": "Radiation",
                 "module": "待分类", "exam_ready": False}
            ]
            target.write_text(json.dumps({"records": source}), encoding="utf-8")
            result = backfill(root)
            self.assertEqual(result["sources"]["college_physics"]["updated"], 2)
            output = json.loads(target.read_text(encoding="utf-8"))["records"]
            self.assertEqual([r["module"] for r in output],
                             ["热学", "力学", "待分类"])
            self.assertEqual(backfill(root)["sources"]["college_physics"]["updated"], 0)

    def test_override_refuses_different_upstream_title(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "college_physics" / "index.json"
            target.parent.mkdir(parents=True)
            target.write_text(json.dumps({"records": [
                {"id": "CP-00898", "title": "Nuclear Radiation",
                 "module": "近代物理", "exam_ready": False}]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Pinned title mismatch"):
                backfill(root)
