#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a single Chinese editorial review book; source files remain untouched."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = "localization/zh_CN/translations.json"
MODULES = {"物理基础", "力学", "热学", "电磁学", "振动与波动", "光学", "近代物理"}
REVIEW_STATE = "中文初译待双语复核"

def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def validate(root=ROOT):
    reg = json.loads((root / REGISTER).read_text(encoding="utf-8"))
    if reg.get("schema") != "ruoshui-physics-zh-editorial-drafts/v1":
        raise ValueError("Unsupported Chinese review schema")
    records = reg.get("additional_entries")
    if not isinstance(records, list):
        raise ValueError("Missing translation entries")
    seen = set()
    for item in records:
        ident = item["id"]
        if not re.fullmatch(r"(?:CP-\d{5}|IP-\d{4})", ident) or ident in seen:
            raise ValueError("Invalid or duplicate translated ID: " + ident)
        seen.add(ident)
        source = "college_physics" if ident.startswith("CP") else "intro_physics"
        path = item["raw_path"]
        if path != f"external_sources/{source}/raw/{ident}.md":
            raise ValueError("Unsafe or mismatched source path: " + path)
        raw = (root / path).read_bytes()
        if git_blob_sha(raw) != item["raw_blob_sha"]:
            raise ValueError("Source file changed; review original before publication: " + ident)
        if item["module"] not in MODULES or not item["subtopic"].strip():
            raise ValueError("Missing controlled topic classification: " + ident)
        if item.get("translation_status") != REVIEW_STATE:
            raise ValueError("Editorial translation cannot claim approval: " + ident)
        if item.get("exam_ready") is not False or item.get("physics_review") != "未审核":
            raise ValueError("Unreviewed OER cannot enter formal exams: " + ident)
        for field in ("title_zh", "question_zh"):
            s = item[field]
            if not isinstance(s, str) or not s.strip():
                raise ValueError("Missing Chinese translation: " + ident)
            if "<math" in s.lower() or s.count("$") % 2:
                raise ValueError("Unconverted markup or broken math delimiters: " + ident)
            if not re.search(r"[\u3400-\u9fff]", s):
                raise ValueError("No Chinese in translated field: " + ident)
        flags = item.get("risk_flags", [])
        if not isinstance(flags, list) or len(set(flags)) != len(flags) or any(not isinstance(flag, str) or not flag.strip() for flag in flags):
            raise ValueError("Invalid editorial risk flags: " + ident)
        if ident.startswith("CP-") and ident not in raw.decode("utf-8"):
            raise ValueError("Original excerpt ID mismatch: " + ident)
    return records

def build(root=ROOT, dest=None):
    records = validate(root)
    dest = dest or root / "generated" / "zh_review"
    dest.mkdir(parents=True, exist_ok=True)
    cols = ("id", "module", "subtopic", "title_zh", "raw_path",
            "translation_status", "physics_review", "exam_ready", "risk_flags")
    with (dest / "INDEX.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols)
        writer.writeheader()
        for item in records:
            writer.writerow({key: ("；".join(item.get("risk_flags", [])) if key == "risk_flags" else item[key]) for key in cols})
    lines = [
        "# 大学物理外部题源：中文编辑审校稿", "",
        "> 中文初译，仅供人工校对；尚未通过独立物理、答案和授权审核，不能作为正式组卷题源。", ""
    ]
    for module in sorted({p["module"] for p in records}):
        lines += ["## " + module, ""]
        for p in records:
            if p["module"] != module:
                continue
            lines += ["### " + p["id"] + " · " + p["title_zh"], "",
                      "**知识点：** " + p["subtopic"], "", p["question_zh"], "",
                      "**原件：** " + p["raw_path"], "",
                      "**原件 Git blob SHA：** " + p["raw_blob_sha"], "",
                      "**状态：** " + REVIEW_STATE, ""]
            if p.get("risk_flags"):
                lines += ["**题设／编辑风险：** " + "；".join(p["risk_flags"]), ""]
            if p.get("notes"):
                lines += ["**审校提示：** " + p["notes"], ""]
    (dest / "QUESTIONS_ZH.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = {"translations": len(records), "by_module": dict(Counter(
        p["module"] for p in records)), "source_sha_checked": len(records),
        "risk_flagged": sum(bool(p.get("risk_flags")) for p in records),
        "exam_ready_added": 0, "status": REVIEW_STATE}
    (dest / "report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report = ({"translations_verified": len(validate()), "exam_ready_added": 0}
              if args.check else build())
    print(json.dumps(report, ensure_ascii=False, indent=2))
