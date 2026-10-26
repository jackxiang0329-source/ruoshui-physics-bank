#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild candidate exam curation queue from attributed raw-source manifests.

Never promotes imported third-party questions to the independent approved bank.
Run: python scripts/rebuild_external_queue.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "external_sources"
MODULES = {
    "003":"力学","004":"力学","005":"力学","006":"力学","007":"力学",
    "008":"力学","009":"力学","010":"力学","011":"力学","012":"力学",
    "013":"力学","014":"力学","015":"振动与波动","016":"振动与波动",
    "018":"电磁学","019":"电磁学","020":"电磁学","021":"电磁学","022":"光学",
}
COLUMNS = ["id","source","module","original_topic","author","license",
           "requires_media","requires_engine","answer_verified","semantic_dedup",
           "license_review","exam_ready","source_url","raw_path"]


def candidates(root=BASE):
    ubc = json.loads((root/"ubc_opbp"/"index.json").read_text(encoding="utf-8"))
    opl = json.loads((root/"webwork_opl"/"index.json").read_text(encoding="utf-8"))
    rows=[]
    for p in ubc["records"]:
        rows.append({
            "id":p["id"],"source":"UBC OPBP",
            "module":MODULES.get(p["topic"][:3],"待分类"),
            "original_topic":p["topic"],"author":p.get("author",""),
            "license":p["license"],"requires_media":"yes" if p["requires_media"] else "no",
            "requires_engine":"no","answer_verified":"no","semantic_dedup":"pending",
            "license_review":"pending","exam_ready":"no","source_url":p["source_url"],
            "raw_path":f"external_sources/ubc_opbp/raw/{p['id']}.md",
        })
    for p in opl["records"]:
        rows.append({
            "id":p["id"],"source":"WeBWorK BrockPhysics","module":"近代物理",
            "original_topic":p["chapter"],"author":p.get("author",""),
            "license":p["license"],"requires_media":"unknown","requires_engine":"yes",
            "answer_verified":"no","semantic_dedup":"pending",
            "license_review":"pending","exam_ready":"no","source_url":p["upstream_url"],
            "raw_path":f"external_sources/webwork_opl/raw/{p['id']}.pg",
        })
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("Duplicated external problem IDs")
    return rows


def main():
    rows=candidates()
    output=BASE/"curation_queue.csv"
    with output.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=COLUMNS,lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} third-party candidate rows. None approved for exam use.")


if __name__ == "__main__":
    main()
