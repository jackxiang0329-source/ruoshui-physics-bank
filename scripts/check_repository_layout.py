#!/usr/bin/env python3
"""Repository-wide naming and navigation checks; no source content is modified."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DOC_CATEGORIES = {"guides", "policies", "reports", "history", "reviews", "references"}
NAME = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*\.(?:md|json)$")
SCRIPT = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*\.py$")
WORKFLOW = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.yml$")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
BANK_ID = re.compile(r"^[A-Z]\d{3,5}$")
ARCHIVE = re.compile(r"^[a-z0-9_]+-raw\.tar\.gz$")
EXCEPTIONS = {"README.md", "manifest.json", "small_sources_manifest.json",
              "webwork_sources_manifest.json", "compaction_round_02.md",
              "compaction_round_03.md"}


def main() -> None:
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    tracked = [x for x in paths if x]
    errors = []
    group_count: dict[str, int] = {}
    for path in tracked:
        parts = path.split("/")
        category = parts[0]
        group_count[category] = group_count.get(category, 0) + 1
        if category == "docs":
            if path == "docs/README.md":
                continue
            if len(parts) != 3 or parts[1] not in DOC_CATEGORIES or not NAME.fullmatch(parts[2]):
                errors.append("docs naming/category: " + path)
        elif category == "scripts" and (len(parts) != 2 or not SCRIPT.fullmatch(parts[1])):
            errors.append("scripts require snake_case.py: " + path)
        elif category == "tests" and (len(parts) != 2 or not re.fullmatch(r"test_[a-z0-9_]+\.py", parts[1])):
            errors.append("test script naming: " + path)
        elif category == ".github":
            if len(parts) != 3 or parts[1] != "workflows" or not WORKFLOW.fullmatch(parts[2]):
                errors.append("workflow naming: " + path)
        elif parts[:2] == ["external_sources", "_bundles"]:
            if len(parts) != 3 or (parts[2] not in EXCEPTIONS and not ARCHIVE.fullmatch(parts[2])):
                errors.append("bundle naming: " + path)

    # Keep the repository homepage focused on eight stable functional folders.
    allowed_top_folders = {".github", "bank", "data", "docs", "external_sources",
                           "scripts", "tests", "tex"}
    actual_top_folders = {p.split("/", 1)[0] for p in tracked if "/" in p}
    if actual_top_folders != allowed_top_folders:
        errors.append(f"unexpected repository root folders: {sorted(actual_top_folders ^ allowed_top_folders)}")

    moved_required = (
        "data/localization/zh_CN/translations.json",
        "data/localization/zh_CN/术语表.md",
        "data/localized/zh_CN/合订/README.md",
        "data/localized/zh_CN/中文译稿报告.json",
        "data/taxonomy/physics_taxonomy.json",
        "data/qa/README.md",
    )
    for path in moved_required:
        if path not in tracked or not (ROOT / path).is_file():
            errors.append("missing consolidated data file: " + path)
    report_path = ROOT / "data/localized/zh_CN/中文译稿报告.json"
    if report_path.is_file():
        report = json.loads(report_path.read_text(encoding="utf-8"))
        refs = report.get("book_index", {})
        if report.get("translated_drafts") != len(refs):
            errors.append("bilingual index count differs from unique translated IDs")
        for uid, ref in refs.items():
            text_path, sep, anchor = ref.partition("#")
            if not sep or anchor != uid.lower() or not text_path.startswith("data/localized/zh_CN/合订/"):
                errors.append(f"incorrect new bilingual source path: {uid}")
                continue
            if not (ROOT / text_path).is_file():
                errors.append(f"missing consolidated bilingual book for {uid}")

    # This is intentionally an audit of names, not a quota or evidence of academic approval.
    b = {}
    for p in tracked:
        if p.startswith("bank/"):
            pieces = p.split("/")
            if len(pieces) < 3 or not BANK_ID.fullmatch(pieces[1]):
                errors.append("bank ID path violates stable format: " + p)
                continue
            b.setdefault(pieces[1], set()).add("/".join(pieces[2:]))
    required = {"meta.json", "question.tex", "solution.tex"}
    for uid, actual in b.items():
        if not required.issubset(actual):
            errors.append(f"{uid}: missing canonical source(s): {sorted(required-actual)}")
    if len(b) != 452:
        errors.append(f"formal bank count drift: {len(b)} != 452")

    for source, count in (("webwork_opl", 59), ("webwork_thermal", 21)):
        archive = ROOT / "external_sources" / "_bundles" / f"{source}-raw.tar.gz"
        manifest = ROOT / "external_sources" / "_bundles" / "webwork_sources_manifest.json"
        raws = [p for p in tracked if p.startswith(f"external_sources/{source}/raw/") and (ROOT / p).exists()]
        if not archive.is_file() or not manifest.is_file() or raws:
            errors.append(f"{source}: expected packed .pg archive and no tracked raw ({len(raws)} remain)")
        idx = json.loads((ROOT / "external_sources" / source / "index.json").read_text())
        if len(idx["records"]) != count or idx.get("count") != count:
            errors.append(f"{source}: unexpected indexed PG count")

    checked_links = 0
    for p in tracked:
        if not (p == "README.md" or p == "external_sources/README.md"
                or p == "external_sources/catalog_index.md"
                or p in ("data/README.md", "data/qa/README.md", "data/localized/zh_CN/合订/README.md")
                or p.startswith("docs/") and p.endswith(".md")
                or p.startswith("external_sources/_bundles/") and p.endswith(".md")):
            continue
        source = ROOT / p
        for raw in LINK.findall(source.read_text(encoding="utf-8")):
            target = raw.split("#", 1)[0].split("?", 1)[0].strip("<>")
            if not target or urlparse(target).scheme or target.startswith("//"):
                continue
            # Skip known Markdown media refs interpreted as URI paths only.
            dest = (source.parent / unquote(target)).resolve()
            if not dest.is_relative_to(ROOT.resolve()) or not dest.exists():
                errors.append(f"broken relative Markdown link: {p} -> {raw}")
            checked_links += 1

    print(json.dumps({"tracked_files": len(tracked), "top_level": group_count,
                      "bank_problem_count": len(b), "markdown_links_checked": checked_links,
                      "errors": errors[:30]}, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(f"layout rejected: {len(errors)} problems")
    print("PASS: naming classes, 452 stable source IDs, archived .pg and local links")


if __name__ == "__main__":
    main()
