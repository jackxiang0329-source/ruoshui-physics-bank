#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Losslessly pack three unreviewed external raw candidate corpora.

Only the external *raw* Markdown candidates are packed. The canonical
bank/ID/{meta.json,question.tex,solution.tex}, Irodov, Zhang Sanhui PR, indices,
licenses, reports, tests and workflows are not touched.

  python scripts/compact_external_candidates.py --apply
  python scripts/compact_external_candidates.py --verify
  python scripts/compact_external_candidates.py --restore college_physics

The archive manifest and stored exact-bytes SHA256 are verified *before* any
raw path is removed. Tar member paths are deliberately only ID.md, never
absolute or relative parent paths. Restore is explicit; extracted raw content
is intentionally gitignored and should be repacked after edits.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import shutil
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT / "external_sources"
BUNDLES = EXTERNAL / "_bundles"
MANIFEST = BUNDLES / "manifest.json"
SOURCES = ("hf_physics_dpo", "college_physics", "physics_refresher")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def expected(source: str) -> list[str]:
    idx = EXTERNAL / source / "index.json"
    data = json.loads(idx.read_text(encoding="utf-8"))
    records = data["records"]
    ids = [row["id"] for row in records]
    if len(set(ids)) != len(ids):
        raise RuntimeError(f"{source}: duplicate IDs in the index")
    if data.get("count", len(ids)) != len(ids):
        raise RuntimeError(f"{source}: index count differs from indexed records")
    names = sorted(f"{i}.md" for i in ids)
    if any(not re.fullmatch(r"[A-Z0-9-]+\.md", n) for n in names):
        raise RuntimeError(f"{source}: suspicious ID")
    return names


def logical_add(digest, name: str, data: bytes) -> None:
    encoded = name.encode("utf-8")
    digest.update(len(encoded).to_bytes(4, "big"))
    digest.update(encoded)
    digest.update(len(data).to_bytes(8, "big"))
    digest.update(data)


def verify_source(source: str, record: dict, check_raw: bool = False) -> dict:
    names = expected(source)
    expected_set = set(names)
    archive = BUNDLES / f"{source}-raw.tar.gz"
    if not archive.is_file():
        raise RuntimeError(f"{source}: archive absent: {archive}")
    raw_archive = archive.read_bytes()
    if sha(raw_archive) != record["archive_sha256"]:
        raise RuntimeError(f"{source}: compressed archive checksum mismatch")

    actual_names: set[str] = set()
    digest = hashlib.sha256()
    nbytes = 0
    with tarfile.open(fileobj=io.BytesIO(raw_archive), mode="r:gz") as tf:
        for item in tf:
            name = item.name
            if not item.isfile() or name not in expected_set or name in actual_names:
                raise RuntimeError(f"{source}: unsafe, duplicate or unindexed member: {name}")
            blob = tf.extractfile(item).read()
            if len(blob) != item.size:
                raise RuntimeError(f"{source}: truncated tar member {name}")
            if check_raw:
                original = (EXTERNAL / source / "raw" / name).read_bytes()
                if original != blob:
                    raise RuntimeError(f"{source}: archive is not byte-for-byte lossless: {name}")
            actual_names.add(name)
            logical_add(digest, name, blob)
            nbytes += len(blob)
    if actual_names != expected_set:
        missing = sorted(expected_set - actual_names)
        raise RuntimeError(f"{source}: {len(missing)} missing archive members: {missing[:4]}")
    if record["count"] != len(names) or record["raw_bytes"] != nbytes:
        raise RuntimeError(f"{source}: record count or uncompressed byte count mismatch")
    if record["logical_sha256"] != digest.hexdigest():
        raise RuntimeError(f"{source}: archive content digest mismatch")
    current_index_hash = sha((EXTERNAL / source / "index.json").read_bytes())
    if record["index_sha256"] != current_index_hash:
        raise RuntimeError(
            f"{source}: index updated without repacking raw; run --restore then --apply"
        )
    return {"source": source, "candidates": len(names), "raw_bytes": nbytes,
            "bundle_bytes": len(raw_archive), "status": "verified"}


def pack_source(source: str) -> dict:
    raw = EXTERNAL / source / "raw"
    names = expected(source)
    real_names = sorted(p.name for p in raw.iterdir() if p.is_file())
    if names != real_names:
        raise RuntimeError(f"{source}: index/raw drift: indexed={len(names)}, files={len(real_names)}")
    if any(p.is_symlink() or not p.is_file() for p in raw.iterdir()):
        raise RuntimeError(f"{source}: non-regular input encountered")
    BUNDLES.mkdir(parents=True, exist_ok=True)
    path = BUNDLES / f"{source}-raw.tar.gz"
    temp = BUNDLES / f"{source}-raw.tar.gz.partial"
    digest = hashlib.sha256()
    nbytes = 0
    try:
        with tarfile.open(temp, mode="w:gz", compresslevel=6,
                          format=tarfile.PAX_FORMAT) as tar:
            for name in names:
                content = (raw / name).read_bytes()
                item = tarfile.TarInfo(name=name)
                item.size = len(content)
                item.mode = 0o644
                item.mtime = item.uid = item.gid = 0
                item.uname = item.gname = ""
                tar.addfile(item, io.BytesIO(content))
                logical_add(digest, name, content)
                nbytes += len(content)
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)
    record = {
        "count": len(names),
        "raw_bytes": nbytes,
        "archive_sha256": sha(path.read_bytes()),
        "logical_sha256": digest.hexdigest(),
        "index_sha256": sha((EXTERNAL / source / "index.json").read_bytes()),
        "archive_path": str(path.relative_to(ROOT)),
        "format": "deterministic-tar-gz/ID.md",
    }
    # Independently re-read the compressed archive and compare every byte
    # before ANY deletion from the Git worktree is considered.
    verify_source(source, record, check_raw=True)
    return record


def verify_all() -> list[dict]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if sorted(manifest["sources"]) != sorted(SOURCES):
        raise RuntimeError("bundle manifest must cover exactly three selected corpora")
    return [verify_source(s, manifest["sources"][s]) for s in SOURCES]


def apply() -> None:
    if MANIFEST.is_file() and not any((EXTERNAL / s / "raw").exists() for s in SOURCES):
        print(json.dumps(verify_all(), ensure_ascii=False, indent=2))
        print("Already compacted; no data modified.")
        return

    for source in SOURCES:
        if not (EXTERNAL / source / "raw").is_dir():
            raise RuntimeError(f"{source}: raw missing; restore all three sources before repacking")
    records = {s: pack_source(s) for s in SOURCES}
    BUNDLES.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({
        "schema": 1,
        "scope": "unreviewed-external-candidates-only",
        "not_included": ["bank/", "external_sources/irodov-zh-elegant/",
                         "tex/", "data/", "data/localized/"],
        "sources": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    verified = verify_all()
    # Files are removed only after all three archives and their complete
    # indexed input bytes have been independently read back and verified.
    for source in SOURCES:
        shutil.rmtree(EXTERNAL / source / "raw")
    print(json.dumps(verified, ensure_ascii=False, indent=2))
    print("All three raw directories replaced by verified lossless archives.")


def restore(source: str) -> None:
    if source not in SOURCES:
        raise RuntimeError("source must be one of: " + ", ".join(SOURCES))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rec = manifest["sources"][source]
    verify_source(source, rec)
    target = EXTERNAL / source / "raw"
    if target.exists():
        raise RuntimeError("restore target already exists; refusing overwrite")
    target.mkdir(parents=True)
    path = BUNDLES / f"{source}-raw.tar.gz"
    with tarfile.open(path, "r:gz") as tar:
        for member in tar:
            # The archive has already passed the name/index/regular-file gate.
            (target / member.name).write_bytes(tar.extractfile(member).read())
    verify_source(source, rec, check_raw=True)
    print(f"Restored {rec['count']} exact original Markdown files into {target}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--apply", action="store_true")
    group.add_argument("--verify", action="store_true")
    group.add_argument("--restore", choices=SOURCES, metavar="SOURCE")
    args = parser.parse_args()
    if args.apply:
        apply()
    elif args.verify:
        print(json.dumps(verify_all(), ensure_ascii=False, indent=2))
    else:
        restore(args.restore)


if __name__ == "__main__":
    main()
