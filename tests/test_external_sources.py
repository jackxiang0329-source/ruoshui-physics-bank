"""Offline integrity checks for external physics source ingestion."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from external_inventory import inventory
from sync_external_physics import SETTINGS, file_blob_sha, license_signal, sync


class ExternalPhysicsTests(unittest.TestCase):
    def test_imported_sources_are_separate_from_original_100(self):
        report = inventory(ROOT / "external_sources")
        self.assertGreaterEqual(report["imported_raw_files"], 52)
        self.assertEqual(0, report["exam_eligible"])
        self.assertEqual([], report["blocking_issues"])

    def test_manifest_download_flags_match_actual_index(self):
        base = ROOT / "external_sources"
        manifest = json.loads((base / "catalog" / "upstream_manifest.json").read_text(encoding="utf-8"))
        for row in manifest["sources"]:
            opts = SETTINGS[row["id"]]
            index = json.loads((base / opts["source_dir"] / "index.json").read_text(encoding="utf-8"))
            imported = {record["path"].split(row["root"] + "/",1)[-1]
                        for record in index["records"]}
            declared = {record["path"] for record in row["files"] if record.get("downloaded")}
            self.assertEqual(imported, declared)
            self.assertEqual(row["raw_imported"], len(imported))
            self.assertLessEqual(len(imported), row["listed"])

    def test_strict_git_blob_integrity(self):
        data = b"simple physics equation test\n"
        import hashlib
        expected = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        self.assertEqual(expected, file_blob_sha(data))

    def test_rights_gate_and_dry_run(self):
        example = "## Attribution\nProblem is licensed under CC-BY-NC-SA 4.0.\n"
        self.assertIn("NC", license_signal(example, "ubc_opbp"))
        self.assertIsNone(license_signal("Not licensed", "ubc_opbp"))
        info = sync("ubc_opbp", limit=3, download=False)
        self.assertEqual("dry-run", info["mode"])
        self.assertEqual(0, info["network_calls"])


if __name__ == "__main__":
    unittest.main()
