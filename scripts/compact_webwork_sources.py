#!/usr/bin/env python3
"""Losslessly bundle unreviewed WeBWorK PG source programs, keeping original bytes.

Only two noncanonical raw candidate directories are affected:
  external_sources/webwork_opl/raw/*.pg (59 items)
  external_sources/webwork_thermal/raw/*.pg (21 items)

Independent SHA-256 checks of each logical file stream, the compressed bundles,
and source indices run BEFORE removing originals. The complete original bytes
and filename can be recovered with --restore. No formal bank, Irodov, PDFs,
WeBWorK PG sources, or the three previously compacted large corpora are changed.
"""
from __future__ import annotations

import argparse
import gzip
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
MANIFEST = BUNDLES / "webwork_sources_manifest.json"
SOURCES = {"webwork_opl": ("pg", 59), "webwork_thermal": ("pg", 21)}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def names_from_index(source: str) -> list[str]:
    extension, count = SOURCES[source]
    index_path = EXTERNAL / source / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    records = index["records"]
    names = sorted(str(rec["id"]) + "." + extension for rec in records)
    if len(names) != count or len(set(names)) != count:
        raise RuntimeError(f"{source}: indexed count or unique IDs drift")
    if index.get("count", count) != count:
        raise RuntimeError(f"{source}: index count drift")
    if any(not re.fullmatch(r"[A-Za-z0-9-]+\." + extension, x) for x in names):
        raise RuntimeError(f"{source}: suspicious source filename")
    return names


def add_logical(sha, name: str, raw: bytes) -> None:
    label = name.encode("utf-8")
    sha.update(len(label).to_bytes(4, "big"))
    sha.update(label)
    sha.update(len(raw).to_bytes(8, "big"))
    sha.update(raw)


def verify_source(source: str, record: dict, check_raw: bool = False) -> dict:
    names = names_from_index(source)
    path = BUNDLES / (source + "-raw.tar.gz")
    content = path.read_bytes()
    if digest(content) != record["archive_sha256"]:
        raise RuntimeError(f"{source}: archive hash mismatch")
    found: set[str] = set()
    stream_hash = hashlib.sha256()
    total = 0
    with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as bundle:
        for item in bundle:
            if not item.isfile() or item.name not in names or item.name in found:
                raise RuntimeError(f"{source}: invalid or duplicate member {item.name}")
            raw = bundle.extractfile(item).read()
            if len(raw) != item.size:
                raise RuntimeError(f"{source}: truncated member {item.name}")
            if check_raw and raw != (EXTERNAL / source / "raw" / item.name).read_bytes():
                raise RuntimeError(f"{source}: nonlossless copy of {item.name}")
            add_logical(stream_hash, item.name, raw)
            total += len(raw)
            found.add(item.name)
    if found != set(names):
        raise RuntimeError(f"{source}: missing {len(set(names) - found)} original files")
    if len(names) != record["count"] or total != record["raw_bytes"]:
        raise RuntimeError(f"{source}: count or byte length drift")
    if stream_hash.hexdigest() != record["logical_sha256"]:
        raise RuntimeError(f"{source}: raw logical digest mismatch")
    if digest((EXTERNAL / source / "index.json").read_bytes()) != record["index_sha256"]:
        raise RuntimeError(f"{source}: index modified after packing; restore and repack")
    return {"source": source, "files": len(names), "raw_bytes": total,
            "archive_bytes": len(content), "verified": True}


def pack(source: str) -> dict:
    names = names_from_index(source)
    rawdir = EXTERNAL / source / "raw"
    actual = sorted(p.name for p in rawdir.iterdir())
    if actual != names or any(not p.is_file() or p.is_symlink() for p in rawdir.iterdir()):
        raise RuntimeError(f"{source}: raw files do not match index or contain symlinks")
    BUNDLES.mkdir(parents=True, exist_ok=True)
    archive = BUNDLES / (source + "-raw.tar.gz")
    partial = archive.with_name(archive.name + ".partial")
    stream_hash = hashlib.sha256()
    total = 0
    try:
        with partial.open("wb") as out, gzip.GzipFile(fileobj=out, mode="wb", filename="", mtime=0, compresslevel=6) as gz, tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tar:
            for name in names:
                content = (rawdir / name).read_bytes()
                item = tarfile.TarInfo(name)
                item.size = len(content)
                item.mode = 0o644
                item.mtime = item.uid = item.gid = 0
                item.uname = item.gname = ""
                tar.addfile(item, io.BytesIO(content))
                add_logical(stream_hash, name, content)
                total += len(content)
        partial.replace(archive)
    finally:
        partial.unlink(missing_ok=True)
    rec = {"count": len(names), "raw_bytes": total,
           "archive_sha256": digest(archive.read_bytes()),
           "logical_sha256": stream_hash.hexdigest(),
           "index_sha256": digest((EXTERNAL / source / "index.json").read_bytes()),
           "archive_path": str(archive.relative_to(ROOT)),
           "format": "tar.gz/ID.pg; gzip-mtime=0"}
    verify_source(source, rec, check_raw=True)
    return rec


def verify_all() -> list[dict]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("schema") != 1 or set(manifest.get("sources", {})) != set(SOURCES):
        raise RuntimeError("unexpected archive manifest source scope")
    return [verify_source(s, manifest["sources"][s]) for s in SOURCES]


def apply() -> None:
    present = [s for s in SOURCES if (EXTERNAL / s / "raw").exists()]
    if not present:
        print(json.dumps(verify_all(), indent=2))
        print("Already bundled; no modifications")
        return
    if set(present) != set(SOURCES):
        raise RuntimeError("partial raw source restoration; restore both or neither before applying")
    records = {s: pack(s) for s in SOURCES}
    MANIFEST.write_text(json.dumps({
        "schema": 1,
        "scope": "noncanonical-unreviewed-candidates-only",
        "not_included": ["bank/", "tex/", "data/", "external_sources/irodov-zh-elegant/",
                         "external_sources/ubc_opbp/", "external_sources/intro_physics/"],
        "sources": records,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # This confirms exact source bytes while they are still in place.
    for source in SOURCES:
        verify_source(source, records[source], check_raw=True)
    # Only after every check succeeds may the worktree originals be removed.
    for source in SOURCES:
        shutil.rmtree(EXTERNAL / source / "raw")
    print(json.dumps(verify_all(), ensure_ascii=False, indent=2))
    print("Removed 80 unreviewed PG source files after lossless verification")


def restore(source: str) -> None:
    if source not in SOURCES:
        raise RuntimeError("unknown source")
    rec = json.loads(MANIFEST.read_text(encoding="utf-8"))["sources"][source]
    verify_source(source, rec)
    dest = EXTERNAL / source / "raw"
    if dest.exists():
        raise RuntimeError("restore destination exists; refusing overwrite")
    dest.mkdir()
    with tarfile.open(BUNDLES / (source + "-raw.tar.gz"), "r:gz") as bundle:
        for member in bundle:
            (dest / member.name).write_bytes(bundle.extractfile(member).read())
    verify_source(source, rec, check_raw=True)
    print(f"Restored {rec['count']} exact WeBWorK PG programs to {dest}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--verify", action="store_true")
    mode.add_argument("--restore", choices=list(SOURCES))
    args = parser.parse_args()
    if args.apply:
        apply()
    elif args.verify:
        print(json.dumps(verify_all(), ensure_ascii=False, indent=2))
    else:
        restore(args.restore)


if __name__ == "__main__":
    main()
