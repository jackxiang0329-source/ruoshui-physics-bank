#!/usr/bin/env python3
"""Create bilingual drafts from carefully edited Chinese text and pinned English."""
import hashlib,json,re,unicodedata
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
TERMS=(
 ("average velocity","平均速度"),("instantaneous velocity","瞬时速度"),
 ("kinetic energy","动能"),("electric potential energy","电势能"),
 ("electric potential","电势"),("wave number","波数"),("angular frequency","角频率"),
 ("electric charge","电荷"),("simple harmonic motion","简谐运动"),
 ("free-body diagram","受力分析图"),("capacitance","电容"),
 ("displacement","位移"),("distance traveled","路程"),
 ("conventional current","约定电流"),
 ("gravitational potential energy","重力势能"),
 ("elastic potential energy","弹性势能"),
 ("work-energy theorem","动能定理"),
 ("conservative force","保守力"),
 ("non-conservative force","非保守力"),
 ("average power","平均功率"),("instantaneous power","瞬时功率"),
)
def digest(text):
    norm=re.sub(r"\s+"," ",unicodedata.normalize("NFKC",text).casefold()).strip()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()
def original(raw):
    part=raw.split("\n---\n",1)[0]
    lines=part.splitlines()
    if len(lines)<3 or not lines[0].startswith("# PREF-"):
        raise ValueError("unexpected upstream format")
    return "\n".join(lines[2:]).strip()
def create(root=ROOT):
    t=json.loads((root/"taxonomy/physics_taxonomy.json").read_text(encoding="utf-8"))
    lessons={x["source_path"]:x for x in t["refresher_lessons"]}
    items=json.loads((root/"localization/zh_CN/translations.json").read_text(encoding="utf-8"))["entries"]
    idx=json.loads((root/"external_sources/physics_refresher/index.json").read_text(encoding="utf-8"))
    records={x["id"]:x for x in idx["records"]}
    if len({x["id"] for x in items})!=len(items):raise ValueError("duplicate translations")
    paths=[]
    for item in items:
        pid=item["id"]
        if pid not in records:raise ValueError("unknown source id "+pid)
        rec=records[pid]
        if item["source_sha256"]!=rec["question_sha256"]:
            raise ValueError("source translation mismatch "+pid)
        english=original((root/"external_sources/physics_refresher/raw"/(pid+".md")).read_text(encoding="utf-8"))
        if digest(english)!=rec["question_sha256"]:
            raise ValueError("original text hash mismatch "+pid)
        zh=item["zh"].strip()
        if len(zh)<8 or "待翻译" in zh or "TODO" in zh:
            raise ValueError("invalid Chinese translation "+pid)
        for english_term,zh_term in TERMS:
            if re.search(r"\b"+re.escape(english_term)+r"\b",english,re.I) and zh_term not in zh:
                raise ValueError("critical term mismatch "+pid+": "+english_term+" -> "+zh_term)
        lesson=lessons[rec["source_path"]]
        module=next(x["name"] for x in t["modules"] if x["code"]==lesson["module"])
        correction=t["verified_type_overrides"].get(pid)
        ptype=t["problem_types"].get(correction["type"] if correction else rec["section"],"未核验")
        dest=root/"localized/zh_CN"/lesson["module"]/lesson["topic"]/(pid+".md")
        dest.parent.mkdir(parents=True,exist_ok=True)
        body=("# "+pid+"｜"+lesson["label"]+"\n\n"+
          "**学科：** "+module+"　**知识点：** "+lesson["label"]+"　**题型：** "+ptype+"\n\n"+
          "**审核状态：** 术语初校；待独立双语审核、物理答案审核及版权审核；不可正式组卷。\n\n"+
          "## 中文译题\n\n"+zh+"\n\n"+
          "## 英文原题（原文对照）\n\n"+english+"\n\n"+
          "## 来源\n\n"+
          "- 源文件：external_sources/physics_refresher/raw/"+pid+".md\n"+
          "- 上游链接："+rec["source_url"]+"\n"+
          "- 原始 Git SHA："+rec["source_sha"]+"\n"+
          "- 题目文本指纹："+rec["question_sha256"]+"\n"+
          "- 来源标示 CC BY 4.0；单题权利链仍须核验。\n"+
          "- 不含任何未经审定的标准答案。\n")
        dest.write_text(body,encoding="utf-8")
        paths.append(str(dest.relative_to(root)))
    # Consolidate all source-pinned Chinese drafts within the existing module tree.
    from export_zh_review import validate as validate_additional
    extra = validate_additional(root)
    module_codes = {m["name"]: m["code"] for m in t["modules"]}
    for item in extra:
        pid = item["id"]
        rel = ("localized/zh_CN/" + module_codes[item["module"]]
               + "/supplementary/" + pid + ".md")
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        raw = (root / item["raw_path"]).read_text(encoding="utf-8")
        english = raw.split("\n---\n", 1)[0].strip()
        body = (
            "# " + pid + "｜" + item["title_zh"] + "\n\n"
            "**学科：** " + item["module"] + "　**知识点：** " + item["subtopic"] + "\n\n"
            "**审核状态：** 中文初译；待独立双语、物理、答案及版权复核；不可正式组卷。\n\n"
            "## 中文译题\n\n" + item["question_zh"] + "\n\n"
            "## 英文原题（存档摘录）\n\n" + english + "\n\n"
            "## 来源\n\n- 原件：" + item["raw_path"] + "\n"
            "- 原件 Git blob SHA：" + item["raw_blob_sha"] + "\n"
            "- 上游署名与许可证见原件；尚未完成单题权利审查。\n"
        )
        if item.get("risk_flags"):
            body += "- 题设／编辑风险：" + "；".join(item["risk_flags"]) + "\n"
        if item.get("notes"):
            body += "- 审校提示：" + item["notes"] + "\n"
        dest.write_text(body, encoding="utf-8")
        paths.append(rel)
    # Generated publication views are 7 subject books, not one Markdown file per problem.
    # Read the already-validated drafts, consolidate, then remove the old generated
    # per-question views. Never touch the pinned English raw/ source tree.
    grouped=defaultdict(list)
    for rel in paths:
        grouped[Path(rel).parts[2]].append(rel)
    books=[]
    book_index={}
    collection=root/"localized/zh_CN/合订"
    collection.mkdir(parents=True,exist_ok=True)
    for module in t["modules"]:
        code=module["code"]
        if not grouped.get(code):
            continue
        rel_book=f"localized/zh_CN/合订/{code}.md"
        sections=[f"# 大学物理中英对照初译｜{module['name']}","",
                  "> 仅供编辑复核：尚未通过独立双语、答案或版权审核；不可正式组卷。","",
                  f"共 {len(grouped[code])} 道。英文原文均以保留源指纹的上游快照为依据。",""]
        for rel in sorted(grouped[code],key=lambda x:Path(x).stem):
            pid=Path(rel).stem
            original_body=(root/rel).read_text(encoding="utf-8")
            if not original_body.startswith("# "+pid):
                raise ValueError("generated draft ID mismatch: "+pid)
            sections.append(f'<a id="{pid.lower()}"></a>')
            sections.append("")
            sections.append(original_body.replace("# "+pid,"## "+pid,1).rstrip())
            sections.append("")
            sections.append("---")
            sections.append("")
            book_index[pid]=rel_book+"#"+pid.lower()
        (root/rel_book).write_text("\n".join(sections)+"\n",encoding="utf-8")
        books.append(rel_book)
    if len(book_index)!=len(paths) or len(books)!=len(grouped):
        raise ValueError("collection lost source-bound translations")
    # Include stale generated IDs from earlier runs, not just the current manifest.
    # Source files and the canonical translations.json are strictly out of scope.
    for old in (root/"localized/zh_CN").rglob("*.md"):
        if re.fullmatch(r"(?:PREF-\d{5}|CP-\d{5}|IP-\d{4})\.md",old.name):
            old.unlink()
    links=["# 大学物理中英对照｜按学科合订","",
           "仅供审校；所有外部题尚未获正式组卷资格。","",
           "译文的唯一可编辑主档：`../../../localization/zh_CN/translations.json`；原始英文文件不移动。",""]
    for module in t["modules"]:
        book=f"localized/zh_CN/合订/{module['code']}.md"
        if book in books:
            links.append(f"- [{module['name']}]({module['code']}.md)（{len(grouped[module['code']])} 道）")
    (collection/"README.md").write_text("\n".join(links)+"\n",encoding="utf-8")
    report={"translated_drafts":len(paths),"original_hash_checks_passed":len(paths),
            "independently_bilingual_approved":0,"exam_ready":0,
            "consolidated_books":len(books),"per_question_files":0,
            "files":books,"book_index":book_index}
    output=root/"localized/zh_CN/中文译稿报告.json"
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"translated_drafts":len(paths),"approved":0},ensure_ascii=False))
    return report
if __name__=="__main__":create()
