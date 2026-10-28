#!/usr/bin/env python3
"""Create bilingual drafts from carefully edited Chinese text and pinned English."""
import hashlib,json,re,unicodedata
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
    report={"translated_drafts":len(paths),"original_hash_checks_passed":len(paths),
            "independently_bilingual_approved":0,"exam_ready":0,"files":paths}
    output=root/"localized/zh_CN/中文译稿报告.json"
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"translated_drafts":len(paths),"approved":0},ensure_ascii=False))
    return report
if __name__=="__main__":create()
