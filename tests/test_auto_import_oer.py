import hashlib
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import auto_import_oer as oer


class SafeImportTests(unittest.TestCase):
    def test_license_explicit_by(self):
        t = "---\nauthor: Alice Example\n---\nA simple problem.\n## Attribution\nUnder CC-BY 4.0."
        self.assertEqual(oer.license_verdict(t), ("CC BY 4.0", None))

    def test_license_blocks_noncommercial_and_ambiguous(self):
        t = "---\nauthor: Alice Example\n---\n## Attribution\nCC-BY-NC-SA 4.0."
        self.assertIsNotNone(oer.license_verdict(t)[1])
        self.assertIsNotNone(oer.license_verdict("CC-BY 4.0")[1])

    def test_license_blocks_missing_author(self):
        self.assertIsNotNone(oer.license_verdict("## Attribution\nCC-BY 4.0")[1])

    def test_subject_classification(self):
        self.assertEqual(oer.category("004.Kinematics(1D)"), "力学")
        self.assertEqual(oer.category("019.Magnetism"), "电磁学")
        self.assertEqual(oer.category("022.Light"), "光学")
        self.assertIsNone(oer.category("001.Math"))

    def test_duplicate_normalization_and_blob_integrity(self):
        a = "---\ntitle: A\n---\n# Question\nA ball falls.\n## Attribution\nCC-BY 4.0"
        b = "---\ntitle: B\n---\n# Question\nA  ball   falls.\n## Attribution\nCC-BY 4.0"
        self.assertEqual(oer.canonical(a), oer.canonical(b))
        raw = b"hello\n"
        self.assertEqual(oer.git_blob_sha(raw),
                         hashlib.sha1(b"blob 6\0hello\n").hexdigest())

    def test_media_is_never_silently_approved(self):
        self.assertTrue(oer.media_required("assets:\n- figure.png\n"))
        self.assertTrue(oer.media_required('Here: <img src="x.png">'))
        self.assertFalse(oer.media_required("assets: null\n"))


if __name__ == "__main__":
    unittest.main()
