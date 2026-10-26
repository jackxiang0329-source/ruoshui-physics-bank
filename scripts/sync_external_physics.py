#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Incrementally download pinned, attributed external university physics problems.

Defaults to a no-network dry run. Changes only external_sources/, never bank/.
Examples:
  python scripts/sync_external_physics.py --source ubc_opbp --limit 20
  python scripts/sync_external_physics.py --source ubc_opbp --limit 50 --download --include-noncommercial
  python scripts/sync_external_physics.py --source webwork_brockphysics --limit 30 --download --include-noncommercial

Never treats downloaded problems as approved or safe for exam assembly.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "external_sources"
MANIFEST = BASE / "catalog" / "upstream_manifest.json"

SETTINGS = {
    "ubc_opbp": {
        "source_dir": "ubc_opbp",
        "root_path": "content/public",
        "extension": ".md",
        "prefix": "UBC",
    },
    "webwork_brockphysics": {
        "source_dir": "webwork_opl",
        "root_path": "Contrib/BrockPhysics/University_Physics_Ling",
        "extension": ".pg",
        "prefix": "OPL",
    },
}


def license_signal(text, source):
    if source == "webwork_brockphysics":
        # This is the OPL default only. Contributors may specify exceptions.
        return "CC BY-NC-SA 3.0 default, subject to source overrides"
    if not re.search(r"^## Attribution", text, re.M):
        return None
    match = re.search(r"CC[- ]BY(?:[- ]NC[- ]SA)? 4[.]0", text, re.I)
    return match.group() if match else None


def file_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def metadata_field(text, field, fmt):
    pattern = (r"^" + re.escape(field) + r":\s*(.*)$" if fmt == "md"
               else r"^##?\s*" + re.escape(field) + r"\(([^)]*)\)")
    match = re.search(pattern, text, re.M)
    return match.group(1).strip() if match else ""


def sync(source, limit, download=False, include_noncommercial=False):
    opts = SETTINGS[source]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    row = next(x for x in manifest["sources"] if x["id"] == source)
    index_path = BASE / opts["source_dir"] / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    existing = {x["path"] for x in index["records"]}
    targets = []
    for item in row["files"]:
        if item.get("downloaded"):
            continue
        # Confirm the upstream path is within its pinned root.
        rel = item["path"]
        if rel.startswith("/") or ".." in Path(rel).parts or not rel.endswith(opts["extension"]):
            continue
        fullpath = row["root"] + "/" + rel
        if fullpath in existing:
            raise ValueError("manifest downloaded flag drift: " + fullpath)
        targets.append(item)
        if len(targets) >= limit:
            break
    if not download:
        return {"mode": "dry-run", "source": source, "candidates": len(targets),
                "next_paths": [x["path"] for x in targets], "network_calls": 0}

    # Avoid accidentally mixing source licenses into a commercial application.
    if source == "webwork_brockphysics" and not include_noncommercial:
        raise ValueError("OPL默认含NC许可。仅在可遵守非商业条款时使用--include-noncommercial。")

    accepted, blocked, failed = [], [], []
    id_number = max([int(x["id"].split("-")[-1]) for x in index["records"]] or [0])
    for item in targets:
        rel = item["path"]
        fullpath = row["root"] + "/" + rel
        uri = "https://raw.githubusercontent.com/" + row["repository"] + "/" + \
              row["revision"] + "/" + "/".join(quote(p, safe="") for p in fullpath.split("/"))
        try:
            req = Request(uri, headers={"User-Agent": "Ruoshui-Physics-OER-Importer/1.0"})
            with urlopen(req, timeout=25) as response:
                raw = response.read()
            if file_blob_sha(raw) != item["sha"]:
                raise ValueError("git blob SHA mismatch (source changed or invalid): " + fullpath)
            text = raw.decode("utf-8")
            license_name = license_signal(text, source)
            if not license_name:
                blocked.append({"path": rel, "reason": "no per-file grant/attribution"})
                continue
            if "NC" in license_name.upper() and not include_noncommercial:
                blocked.append({"path": rel, "reason": "non-commercial restrictions"})
                continue
            id_number += 1
            pid = opts["prefix"] + "-" + str(id_number).zfill(3)
            output = BASE / opts["source_dir"] / "raw" / (pid + opts["extension"])
            if output.exists():
                raise ValueError("would overwrite existing import: " + str(output))
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(raw)
            if source == "ubc_opbp":
                sourceinfo = {
                    "id":pid, "path":fullpath, "license":license_name,
                    "license_source":"per-file Attribution",
                    "author":metadata_field(text,"author","md"),
                    "source":metadata_field(text,"source","md"),
                    "requires_media":bool(re.search(r"^assets:\s*(?!null\b|undefined\b)[^\n]+",text,re.M|re.I)),
                    "source_sha":item["sha"],
                    "source_url":uri.replace("raw.githubusercontent.com/","github.com/").replace(
                        "/" + row["revision"] + "/", "/blob/" + row["revision"] + "/", 1),
                    "topic":rel.split("/")[0],
                    "format":"ubc-myst-markdown",
                    "review_status":"needs_academic_review",
                    "import_status":"raw_imported_not_exam_ready",
                    "copyright_notice_preserved":True,
                }
            else:
                sourceinfo = {
                    "id":pid, "path":fullpath,
                    "author":metadata_field(text,"Author","pg"),
                    "subject":metadata_field(text,"DBsubject","pg"),
                    "chapter":metadata_field(text,"DBchapter","pg"),
                    "section":metadata_field(text,"DBsection","pg"),
                    "textbook":metadata_field(text,"TitleText","pg"),
                    "source_sha":item["sha"], "license":license_name,
                    "license_review":"pending",
                    "upstream_url":uri.replace("raw.githubusercontent.com/","github.com/").replace(
                        "/" + row["revision"] + "/", "/blob/" + row["revision"] + "/", 1),
                    "runtime":"WeBWorK/PG; macros may be missing",
                    "exam_eligible":False,
                    "integrity":"raw_pg_copied_no_engine_validation",
                }
            index["records"].append(sourceinfo)
            item["downloaded"] = True
            accepted.append(pid)
        except Exception as exc:
            failed.append({"path": rel, "error": str(exc)[:250]})

    if source == "ubc_opbp":
        index["imported_questions"] = len(index["records"])
    else:
        index["count"] = len(index["records"])
    row["raw_imported"] = len(index["records"])
    index_path.write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"mode":"download", "source":source, "added":accepted,
            "blocked":blocked, "failed":failed, "raw_total":row["raw_imported"],
            "warning":"Imported raw sources are NOT approved for exam use."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=sorted(SETTINGS), required=True)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--include-noncommercial", action="store_true",
                        help="Only if project use complies with CC non-commercial licenses")
    args = parser.parse_args()
    if not 1 <= args.limit <= 500:
        parser.error("--limit must be between 1 and 500")
    try:
        report = sync(args.source,args.limit,args.download,args.include_noncommercial)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        if report.get("failed"):
            sys.exit(1)
    except Exception as exc:
        parser.error(str(exc))
