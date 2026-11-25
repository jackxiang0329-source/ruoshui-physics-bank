#!/usr/bin/env python3
"""Lossless six-subject bank storage. Only explicit restore writes legacy files."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIXES = "METWOQ"
NAMES = ("meta.json", "question.tex", "solution.tex")
ID = re.compile(r"[METWOQ]\d{3,5}")
def digest(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def archive_path(root, prefix):
    return root / "bank" / (prefix + ".json")

def read_archives(root):
    records = {}
    for prefix in PREFIXES:
        obj = json.loads(archive_path(root, prefix).read_text(encoding="utf-8"))
        if obj["schema"] != 1 or obj["prefix"] != prefix:
            raise ValueError("archive schema/prefix mismatch")
        for uid, files in obj["items"].items():
            if not ID.fullmatch(uid) or uid[0] != prefix or uid in records:
                raise ValueError("invalid or duplicate ID: " + uid)
            if set(files) != set(NAMES):
                raise ValueError("missing or extra file: " + uid)
            for name, entry in files.items():
                raw = entry["text"].encode("utf-8")
                if len(raw) != entry["bytes"] or digest(raw) != entry["git_blob"]:
                    raise ValueError("archive checksum mismatch: " + uid + "/" + name)
            if json.loads(files["meta.json"]["text"])["id"] != uid:
                raise ValueError("metadata ID mismatch: " + uid)
            records[uid] = files
    if not records:
        raise ValueError("empty archive")
    return records

def legacy_files(root):
    bank = root / "bank"
    return {p.relative_to(bank).as_posix(): p for p in bank.glob("*/*")
            if p.is_file() and ID.fullmatch(p.parent.name)}

def pack(root):
    paths = legacy_files(root)
    ids = sorted({p.split("/")[0] for p in paths})
    if not ids or set(paths) != {uid + "/" + name for uid in ids for name in NAMES}:
        raise ValueError("incomplete legacy file set or unexpected file")
    if all(archive_path(root, p).exists() for p in PREFIXES):
        old = read_archives(root)
        if not set(old).issubset(ids):
            raise ValueError("existing IDs missing; restore before editing")
    objs = {p: {"schema": 1, "prefix": p, "items": {}} for p in PREFIXES}
    for uid in ids:
        files = {}
        for name in NAMES:
            raw = paths[uid + "/" + name].read_bytes()
            files[name] = {"bytes": len(raw), "git_blob": digest(raw), "text": raw.decode("utf-8")}
        if json.loads(files["meta.json"]["text"])["id"] != uid:
            raise ValueError("metadata ID mismatch: " + uid)
        objs[uid[0]]["items"][uid] = files
    for p, obj in objs.items():
        archive_path(root, p).write_bytes((json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    records = read_archives(root)
    verify_worktree(root, records)
    print("packed", len(records), "problems,", len(paths), "byte-identical files")

def verify_worktree(root, records):
    paths = legacy_files(root)
    expected = {uid + "/" + name: entry for uid, files in records.items() for name, entry in files.items()}
    if set(paths) != set(expected):
        raise ValueError("restored file set mismatch")
    for rel, path in paths.items():
        if path.read_bytes() != expected[rel]["text"].encode("utf-8"):
            raise ValueError("restored bytes differ: " + rel)

def restore(root):
    records = read_archives(root)
    expected = {uid + "/" + name: entry for uid, files in records.items() for name, entry in files.items()}
    # Check all conflicts before writing anything; never overwrite local edits.
    for rel, path in legacy_files(root).items():
        if rel not in expected or path.read_bytes() != expected[rel]["text"].encode("utf-8"):
            raise ValueError("unpacked local changes exist: " + rel + "; pack or resolve first")
    for rel, entry in expected.items():
        path = root / "bank" / rel
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(entry["text"].encode("utf-8"))
    verify_worktree(root, records)
    print("restored", len(records), "problems,", len(expected), "files")

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pack", action="store_true")
    group.add_argument("--restore", action="store_true")
    group.add_argument("--verify", action="store_true")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.project_root.resolve()
    if args.pack:
        pack(root)
    elif args.restore:
        restore(root)
    else:
        records = read_archives(root)
        print("verified", len(records), "problems,", sum(map(len, records.values())), "blob checksums")
if __name__ == "__main__":
    main()
