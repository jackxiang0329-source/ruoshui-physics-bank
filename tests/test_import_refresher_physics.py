import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import import_refresher_physics as importer


SAMPLE = """# Chapter
## Practice Problems
### Concept Questions
1. Explain why the force is directed radially in a rotating frame.

2. What changes if the object doubles in mass?

### Numerical Problems
1. A 5 kg cart moves at 2 m/s. Find its momentum.
2. The same cart as Problem 1 accelerates. Find its force.

### Challenge Problems
1. A spring oscillates after being compressed; derive its period.
---
## Formula Summary
1. This is a numbered list but not a question.
"""


class TestRefresher(unittest.TestCase):
    def test_extract_only_practice_questions(self):
        q = importer.extract(SAMPLE)
        self.assertEqual(5, len(q))
        self.assertEqual(("conceptual", 1), q[0][:2])
        self.assertEqual(("calculation", 2), q[3][:2])
        self.assertNotIn("Formula Summary", str(q))

    def test_normalization_and_git_integrity(self):
        self.assertEqual(importer.digest("A   Force"), importer.digest("a force"))
        self.assertEqual(importer.git_sha(b"test"), "30d74d258442c7c65512eafab474568dd706c430")

    def test_import_is_idempotent_and_unapproved(self):
        license_text = b"Creative Commons Attribution 4.0 International"
        readme_text = b"Under CC BY 4.0"
        data = SAMPLE.encode()
        docs = {"LICENSE": license_text, "README.md": readme_text,
                "module-2-mechanics/2.1.md": data}
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            folder = base / "physics_refresher"
            folder.mkdir()
            manifest = {
                "repository": importer.REPO, "revision": importer.REV,
                "license_sha": importer.git_sha(license_text),
                "readme_sha": importer.git_sha(readme_text),
                "documents": [{"path": "module-2-mechanics/2.1.md",
                               "sha": importer.git_sha(data), "processed": False}],
            }
            (folder / "source_manifest.json").write_text(json.dumps(manifest))
            get = docs.__getitem__
            a = importer.run(limit=3, base=base, getter=get)
            b = importer.run(limit=10, base=base, getter=get)
            c = importer.run(limit=10, base=base, getter=get)
            self.assertEqual((3, 2, 0), (a["added_count"], b["added_count"], c["added_count"]))
            index = json.loads((folder / "index.json").read_text())
            self.assertEqual(5, index["count"])
            self.assertTrue(all(not p["exam_eligible"] for p in index["records"]))
            self.assertTrue(all(p["license_review"] == "pending" for p in index["records"]))
            self.assertTrue(any(p["requires_context"] for p in index["records"]))

    def test_bad_license_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            folder = base / "physics_refresher"
            folder.mkdir()
            (folder / "source_manifest.json").write_text(json.dumps({
                "repository": importer.REPO, "revision": importer.REV,
                "license_sha": importer.git_sha(b"valid"),
                "readme_sha": importer.git_sha(b"CC BY 4.0"),
                "documents": [],
            }))
            with self.assertRaisesRegex(ValueError, "license"):
                importer.run(base=base, getter=lambda p: b"not the approved hash")


if __name__ == "__main__":
    unittest.main()
