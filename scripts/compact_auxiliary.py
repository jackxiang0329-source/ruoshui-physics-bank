#!/usr/bin/env python3
"""Reversible, byte-checked ZIP storage for derived catalog views and historical QA."""
import argparse
import hashlib
import json
import os
from urllib.parse import unquote, urlparse
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    "catalog_views": (r"external_sources/catalog/(?:按学科|按知识点)/.+\.csv",),
    "round_qa": (r"scripts/check_(?:round(?:0[5-8]|10|11|12|13)[a-z0-9_]*|batch_04_physics|bulk_composite|composite_expansion)\.py",
                 r"data/round1[23]_[a-z0-9_]+\.json"),
    "irodov_regressions": (r"external_sources/irodov-zh-elegant/(?:[a-z0-9_]+_regression|[a-z0-9_]+_qa_common)\.py",),
    "irodov_chapters": (r"external_sources/irodov-zh-elegant/chapters/\d{2}-[a-z-]+\.tex",),
    "zhao_wang_chapters": (r"external_sources/zhao-wang-physics-5e-elegant/chapters/(?:guide-(?:ch|selftest)|textbook-ch)\d{2}\.tex",),
    "three_college_chapters": (r"external_sources/three-college-physics-elegant/chapters/(?:czu|hust|tjut)-ch\d{2}\.tex",),
    "test_suite": (r"tests/test_[a-z0-9_]+\.py",),
    "large_indexes": (r"external_sources/(?:hf_physics_dpo|college_physics|physics_refresher)/index\.json",
                      r"external_sources/catalog/college_corpus_audit\.csv",
                      r"external_sources/curation_queue\.csv"),
    "reference_docs": (r"docs/guides/auto_import_oer\.md|docs/guides/bulk_200_workflow\.md|docs/guides/college_physics_import\.md|docs/guides/college_tex_draft\.md|docs/guides/curation_triage\.md|docs/guides/exam_assembly\.md|docs/guides/huggingface_import\.md|docs/guides/oer_discovery\.md|docs/guides/project_plan\.md|docs/guides/review_preflight\.md|docs/guides/tex_architecture\.md|docs/history/batch_04_complex_models\.md|docs/history/bulk_advanced_12\.md|docs/history/composite_batch_02\.md|docs/history/round_12_worklog\.md|docs/references/textbook_references\.md|docs/reports/college_corpus_audit\.md|docs/reports/coverage_report\.md|docs/reports/legacy_filter_report\.json|docs/reviews/round_01_independent_derivations\.md|docs/reviews/round_01_triage\.md",),
    "source_tools": (r"scripts/audit_college_corpus\.py|scripts/auto_import_oer\.py|scripts/college_tex_draft\.py|scripts/curation_triage\.py|scripts/discover_hf_physics\.py|scripts/discover_oer_sources\.py|scripts/export_zh_review\.py|scripts/external_inventory\.py|scripts/import_college_physics\.py|scripts/import_hf_physics\.py|scripts/import_intro_physics\.py|scripts/import_refresher_physics\.py|scripts/import_seephys\.py|scripts/materialize_zh_drafts\.py|scripts/organize_physics_catalog\.py|scripts/rebuild_external_queue\.py|scripts/reclassify_external_topics\.py|scripts/report_external_coverage\.py|scripts/review_preflight\.py|scripts/sync_external_physics\.py",),
    "round14_qa": (r"data/round14_402_content_similarity_screen\.json|data/round14_core_model_draft_audit\.json|data/round14_draft_validation_report\.json|data/round14_extra6_validation_report\.json|data/round14_final8_validation_report\.json|data/round14_group3_validation_report\.json|data/round14_group4_validation_report\.json|data/round14_group5_validation_report\.json|data/round14_next6_validation_report\.json|data/round14_validation_report\.json|scripts/check_round14_draft\.py|scripts/check_round14_extra6\.py|scripts/check_round14_final8\.py|scripts/check_round14_group3\.py|scripts/check_round14_group4\.py|scripts/check_round14_group5\.py|scripts/check_round14_next6\.py",),
    "source_metadata": (r"external_sources/college_physics/source_manifest\.json|external_sources/hf_physics_dpo/manifest\.json|external_sources/hf_seephys/index\.json|external_sources/hf_seephys/manifest\.json|external_sources/hf_seephys/raw/SEEP-00001\.md|external_sources/intro_physics/README\.md|external_sources/intro_physics/index\.json|external_sources/intro_physics/source_manifest\.json|external_sources/physics_refresher/README\.md|external_sources/physics_refresher/source_manifest\.json|external_sources/ubc_opbp/index\.json|external_sources/webwork_opl/README\.md|external_sources/webwork_opl/index\.json|external_sources/webwork_thermal/README\.md|external_sources/webwork_thermal/index\.json",),
    "catalog_working": (r"external_sources/catalog/auto_import_decisions\.json|external_sources/catalog/college_corpus_audit_report\.json|external_sources/catalog/college_next_review\.csv|external_sources/catalog/college_review_preview\.tex|external_sources/catalog/college_review_tex_draft\.tex|external_sources/catalog/college_review_tex_report\.json|external_sources/catalog/coverage_report\.json|external_sources/catalog/discovered_repositories\.json|external_sources/catalog/huggingface_datasets\.json|external_sources/catalog/review_preflight\.csv|external_sources/catalog/review_preflight_report\.json|external_sources/catalog/review_priority\.csv|external_sources/catalog/review_triage_report\.json|external_sources/catalog/upstream_manifest\.json",),
    "retired_migrations": (r"\.github/workflows/compact-auxiliary-migration\.yml|\.github/workflows/compact-bank-migration\.yml|\.github/workflows/compact-textbooks-migration\.yml",),
    "source_logs": (r"external_sources/logs/college_physics_latest\.json|external_sources/logs/history_2026_10\.json|external_sources/logs/huggingface_import_latest\.json|external_sources/logs/intro_physics_latest\.json|external_sources/logs/refresher_physics_latest\.json|external_sources/logs/seephys_import_latest\.json|external_sources/logs/topic_backfill_latest\.json",),
}
MANIFEST = "_manifest.json"

def match(group, name):
    p = PurePosixPath(name)
    return (not p.is_absolute() and ".." not in p.parts and p.as_posix() == name
            and any(re.fullmatch(rx, name) for rx in GROUPS[group]))

def archive(root, group):
    return root / "data" / "archives" / (group + ".zip")

def hashes(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()}

def load(root, group):
    with zipfile.ZipFile(archive(root, group)) as z:
        names = z.namelist()
        if len(names) != len(set(names)) or z.testzip() is not None:
            raise ValueError("ZIP duplicate member or CRC mismatch")
        m = json.loads(z.read(MANIFEST))
        if m["schema"] != 1 or m["group"] != group:
            raise ValueError("archive group/schema mismatch")
        entries = m["files"]
        if not entries or set(names) != set(entries) | {MANIFEST}:
            raise ValueError("archive member set mismatch")
        result = {}
        for name, info in entries.items():
            if not match(group, name):
                raise ValueError("unexpected member: " + name)
            raw = z.read(name)
            if hashes(raw) != info:
                raise ValueError("checksum mismatch: " + name)
            result[name] = raw
        return result

def checked_path(root, name):
    path = root / name
    if not path.resolve().is_relative_to(root.resolve()) or any(
            p.is_symlink() for p in [path, *path.parents] if p != root.parent):
        raise ValueError("unsafe path: " + name)
    return path

def restore(root, groups):
    data = {}
    for group in groups:
        data.update(load(root, group))
    for name, raw in data.items():
        path = checked_path(root, name)
        if path.exists() and (not path.is_file() or path.read_bytes() != raw):
            raise ValueError("local changes exist; repack or resolve before restore: " + name)
    for name, raw in data.items():
        path = checked_path(root, name)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
    assert all((root / p).read_bytes() == raw for p, raw in data.items())
    print("restored", len(data), "byte-identical files")

def tracked(root):
    return subprocess.check_output(["git","ls-files","-z"], cwd=root).decode("utf-8").strip("\0").split("\0")

def pack(root, group):
    target = archive(root, group)
    old = set(load(root, group)) if target.exists() else set()
    names = sorted(old | {p for p in tracked(root) if match(group, p)})
    if not names:
        raise ValueError("no source files in " + group)
    data = {p: checked_path(root, p).read_bytes() for p in names}
    manifest = {"schema": 1, "group": group, "files": {p: hashes(b) for p,b in data.items()}}
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_suffix(".tmp")
    def put(z, name, raw):
        info = zipfile.ZipInfo(name, (1980,1,1,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        z.writestr(info, raw, compresslevel=9)
    with zipfile.ZipFile(temp, "w") as z:
        put(z, MANIFEST, (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2)+"\n").encode())
        for name, raw in data.items():
            put(z, name, raw)
    temp.replace(target)
    assert load(root, group) == data
    print(group, len(data), "files", sum(map(len,data.values())), "->", target.stat().st_size, "bytes")


def rewrite_links(root, groups):
    """Keep direct GitHub navigation usable when an old path becomes archived."""
    destinations = {}
    for group in groups:
        for name in load(root, group):
            destinations[name] = archive(root, group)
    # Also route links to directories that no longer have any tracked files.
    remaining = set(tracked(root))
    for name, target in list(destinations.items()):
        for parent in PurePosixPath(name).parents:
            p = parent.as_posix()
            if p != "." and not any(x.startswith(p + "/") for x in remaining):
                destinations.setdefault(p, target)
    pattern = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)")
    changed = []
    for rel in sorted(remaining):
        if not rel.endswith(".md"):
            continue
        path = root / rel
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        def repl(m):
            link = m.group(2)
            target = unquote(link.split("#",1)[0].split("?",1)[0].strip("<>"))
            if not target or urlparse(target).scheme or target.startswith("//"):
                return m.group(0)
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(root.resolve()):
                return m.group(0)
            key = resolved.relative_to(root).as_posix()
            if key not in destinations:
                return m.group(0)
            archive_rel = os.path.relpath(destinations[key], path.parent).replace(os.sep,"/")
            return "[" + m.group(1) + "（归档）](" + archive_rel + ")"
        new = pattern.sub(repl, text)
        if new != text:
            path.write_bytes(new.encode("utf-8"))
            changed.append(rel)
    if changed:
        subprocess.run(["git","add","--",*changed],cwd=root,check=True)
    print("updated archive navigation:", changed)


def migrate(root):
    expected = {"reference_docs":21,"source_tools":20,"round14_qa":17,"source_metadata":15,"catalog_working":14,"retired_migrations":3,"source_logs":7}
    original = {}
    for record in subprocess.check_output(["git","ls-tree","-r","-z","HEAD"],cwd=root).split(b"\0"):
        if record:
            meta, name = record.split(b"\t",1)
            original[name.decode("utf-8")] = meta.split()[2].decode()
    removed = []
    for group, count in expected.items():
        if archive(root,group).exists():
            raise ValueError("migration only accepts unpacked initial state")
        pack(root,group)
        data = load(root,group)
        assert len(data) == count
        assert all(original[p] == hashes(b)["git_blob"] for p,b in data.items())
        removed.extend(data)
    assert len(set(removed)) == sum(expected.values()) == 97
    # Workflow changes are finalized by the repository owner after the archive is verified.
    # The Actions token may lack permission to delete workflow definitions.
    removed = [p for p in removed if not match('retired_migrations', p)]
    subprocess.run(["git","rm","--",*sorted(removed)],cwd=root,check=True,stdout=subprocess.DEVNULL)
    subprocess.run(["git","add","--","data/archives"],cwd=root,check=True)
    restore(root,list(GROUPS))
    rewrite_links(root, expected)
    print("migration: all 97 original Git blobs match; 94 ordinary members untracked; three archived workflow definitions await owner removal")

def main():
    p=argparse.ArgumentParser()
    modes=p.add_mutually_exclusive_group(required=True)
    for mode in ("pack","restore","verify","migrate"):
        modes.add_argument("--"+mode,action="store_true")
    p.add_argument("--group",choices=GROUPS)
    p.add_argument("--project-root",type=Path,default=ROOT)
    a=p.parse_args()
    root=a.project_root.resolve()
    groups=[a.group] if a.group else list(GROUPS)
    if a.migrate:
        if a.group: p.error("--migrate requires all groups")
        migrate(root)
    elif a.pack:
        for g in groups: pack(root,g)
    elif a.restore:
        restore(root,groups)
    else:
        for g in groups:
            print(g, len(load(root,g)), "verified files")

if __name__ == "__main__":
    main()
