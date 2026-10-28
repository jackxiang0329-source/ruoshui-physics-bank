import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from export_zh_review import build, validate, git_blob_sha

class ChineseReviewTests(unittest.TestCase):
    def fixture(self, root):
        raw = root / "external_sources" / "college_physics" / "raw" / "CP-00001.md"
        raw.parent.mkdir(parents=True)
        content = b"# Displacement - CP-00001\n\nExample\n"
        raw.write_bytes(content)
        item = {
            "id": "CP-00001", "module": "力学", "subtopic": "运动学／位移",
            "title_zh": "位移", "question_zh": "什么是位移？",
            "raw_path": "external_sources/college_physics/raw/CP-00001.md",
            "raw_blob_sha": git_blob_sha(content),
            "translation_status": "中文初译待双语复核",
            "physics_review": "未审核", "exam_ready": False
        }
        reg = root / "localization" / "zh_CN" / "translations.json"
        reg.parent.mkdir(parents=True)
        reg.write_text(json.dumps({"schema": "ruoshui-physics-zh-editorial-drafts/v1",
                                   "additional_entries": [item]}, ensure_ascii=False), encoding="utf-8")
        return raw, reg

    def test_export_preserves_source_and_review_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            raw, _ = self.fixture(root)
            before = raw.read_bytes()
            report = build(root)
            self.assertEqual(report["source_sha_checked"], 1)
            self.assertEqual(report["exam_ready_added"], 0)
            self.assertEqual(raw.read_bytes(), before)
            self.assertIn("什么是位移", (root / "generated/zh_review/QUESTIONS_ZH.md").read_text())

    def test_sha_drift_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            raw, _ = self.fixture(root)
            raw.write_text("changed CP-00001", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Source file changed"):
                validate(root)

    def test_cannot_claim_approval(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, reg = self.fixture(root)
            obj = json.loads(reg.read_text(encoding="utf-8"))
            obj["additional_entries"][0]["exam_ready"] = True
            reg.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "cannot enter formal exams"):
                validate(root)

    def test_invalid_risk_flag_shape_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, reg = self.fixture(root)
            obj = json.loads(reg.read_text(encoding="utf-8"))
            obj["additional_entries"][0]["risk_flags"] = "unreviewed condition"
            reg.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid editorial risk flags"):
                validate(root)

    def test_module_name_cannot_replace_subtopic(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, reg = self.fixture(root)
            obj = json.loads(reg.read_text(encoding="utf-8"))
            obj["additional_entries"][0]["subtopic"] = "力学"
            reg.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "controlled topic"):
                validate(root)

    def test_unknown_topic_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, reg = self.fixture(root)
            obj = json.loads(reg.read_text(encoding="utf-8"))
            obj["additional_entries"][0]["module"] = "未知电学"
            reg.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "controlled topic"):
                validate(root)
