#!/usr/bin/env python3
"""Verify and optionally restore exact archived historical QA report bytes.

The archives contain machine-generated historical checks, not evidence of
independent academic approval. This tool does not change canonical bank files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COUNTS = {12: 6, 13: 8, 14: 9}


def read_round(round_number: int) -> list[tuple[Path, bytes]]:
    archive = ROOT / "data" / "rounds" / f"historical_reports_round{round_number}.json"
    document = json.loads(archive.read_text(encoding="utf-8"))
    if document.get("format") != "ruoshui-physics-qa-history-v1":
        raise ValueError(f"{archive}: unexpected format")
    if document.get("round") != round_number:
        raise ValueError(f"{archive}: incorrect round")
    entries = document.get("files")
    if not isinstance(entries, list) or len(entries) != EXPECTED_COUNTS[round_number]:
        raise ValueError(f"{archive}: missing/extra entries")
    checked: list[tuple[Path, bytes]] = []
    seen: set[str] = set()
    for item in entries:
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            raise ValueError(f"{archive}: invalid path")
        path = Path(raw_path)
        if len(path.parts) != 2 or path.parts[0] != "data" or not path.name.startswith(f"round{round_number}_"):
            raise ValueError(f"{archive}: unsafe or wrong source path {raw_path!r}")
        if raw_path in seen:
            raise ValueError(f"{archive}: duplicate report {raw_path}")
        seen.add(raw_path)
        data = item["content"].encode("utf-8")
        json.loads(data.decode("utf-8"))
        git_blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
        if git_blob != item["git_blob_sha"]:
            raise ValueError(f"{archive}: original byte hash differs for {raw_path}")
        checked.append((path, data))
    return checked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--verify", action="store_true", help="validate all archival entries and hashes")
    modes.add_argument("--restore", choices=("12", "13", "14", "all"),
                       help="restore selected original generated reports to the working tree")
    parser.add_argument("--force", action="store_true", help="replace different existing report files on restore")
    args = parser.parse_args()
    rounds = list(EXPECTED_COUNTS) if args.verify or args.restore == "all" else [int(args.restore)]
    total = 0
    for num in rounds:
        entries = read_round(num)
        for relative, data in entries:
            target = ROOT / relative
            if args.restore:
                if target.exists() and target.read_bytes() != data and not args.force:
                    raise FileExistsError(f"{relative} differs: use --force only after review")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            total += 1
        print(f"Round {num}: {len(entries)} original reports verified" +
              (" and restored" if args.restore else ""))
    print(f"PASS: {total} losslessly preserved QA reports; canonical physics sources unchanged")


if __name__ == "__main__":
    main()
