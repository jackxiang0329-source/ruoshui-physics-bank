#!/usr/bin/env python3
"""Create stable Chinese catalogue views; never move original source files."""
import csv, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
HEADER=("id","学科","知识点","题型","题型证据","知识点分类依据","原始来源","英文原件","中文译稿","中文状态","答案复核","版权复核","组卷资格")

def configs(root=ROOT):
    taxonomy=json.loads((root/"taxonomy/physics_taxonomy.json").read_text(encoding="utf-8"))
    docs={x["source_path"]:x for x in taxonomy["refresher_lessons"]}
    modules={x["name"]:x for x in taxonomy["modules"]}
    src=json.loads((root/"external_sources/physics_refresher/index.json").read_text(encoding="utf-8"))
    by_id={x["id"]:x for x in src["records"]}
    translations_file=root/"localization/zh_CN/translations.json"
    trans=json.loads(translations_file.read_text(encoding="utf-8"))["entries"] if translations_file.exists() else []
    translation_map={x["id"]:x for x in trans}
    if len(translation_map)!=len(trans):
        raise ValueError("duplicate translation identifiers")
    extra_doc=json.loads(translations_file.read_text(encoding="utf-8")) if translations_file.exists() else {}
    supplements=extra_doc.get("additional_entries",[])
    supplemental_map={x["id"]:x for x in supplements}
    if len(supplemental_map)!=len(supplements) or set(translation_map)&set(supplemental_map):
        raise ValueError("duplicate source-bound translation identifiers")
    return taxonomy,docs,modules,by_id,translation_map,supplemental_map

def classify(row,configs,root=ROOT):
    taxonomy,lessons,modules,pref,translations,supplemental=configs
    pid=row["id"]
    module=row.get("module","待分类")
    if module not in modules:
        module="待分类"
    topic="未细分（待核验）"
    chapter_basis="仅上游一级学科；缺少可靠细分"
    ptype="未核验"
    type_basis="来源题型缺少独立确认"
    zh_path=""
    status="尚未翻译"
    if row.get("source")=="Physics Refresher (CC BY 4.0)":
        rec=pref.get(pid)
        if not rec or rec["source_path"] not in lessons:
            raise ValueError("unmapped pinned Refresher id: "+pid)
        lesson=lessons[rec["source_path"]]
        expected=next(x["name"] for x in taxonomy["modules"] if x["code"]==lesson["module"])
        if expected!=module:
            raise ValueError("source/module conflict: "+pid)
        topic=lesson["label"]
        chapter_basis="固定上游章节映射；单题内容待独立审核"
        cat=taxonomy["verified_type_overrides"].get(pid)
        code=cat["type"] if cat else rec["section"]
        ptype=taxonomy["problem_types"].get(code,"未核验")
        type_basis="逐题编辑纠偏；非物理答案审核" if cat else "上游题型；待独立核验"
        if pid in translations:
            entry=translations[pid]
            if entry["source_sha256"]!=rec["question_sha256"]:
                raise ValueError("stale translated source: "+pid)
            zh_path=f'localized/zh_CN/{lesson["module"]}/{lesson["topic"]}/{pid}.md'
            if not (root/zh_path).is_file():
                raise ValueError("translation manifest has no bilingual file: "+pid)
            status="中英对照初校；待独立复核"
    if pid in supplemental:
        entry=supplemental[pid]
        if row["raw_path"]!=entry["raw_path"]:
            raise ValueError("source path mismatch: "+pid)
        module=entry["module"]
        topic=entry["subtopic"]
        chapter_basis="逐题英文摘录初核；仍待独立双语审稿"
        ptype="未核验"
        type_basis="题型尚未独立确认"
        code=modules[module]["code"]
        zh_path=f"localized/zh_CN/{code}/supplementary/{pid}.md"
        if not (root/zh_path).is_file():
            raise ValueError("missing supplementary bilingual file: "+pid)
        status="中英对照初校；待独立复核"
    if module=="待分类":
        chapter_basis="一级学科未确认；隔离待分类"
    return {
      "id":pid,"学科":module,"知识点":topic,"题型":ptype,"题型证据":type_basis,
      "知识点分类依据":chapter_basis,"原始来源":row["source"],"英文原件":row["raw_path"],
      "中文译稿":zh_path,"中文状态":status,"答案复核":"待核验","版权复核":"待核验","组卷资格":"否"
    }

def generate(root=ROOT):
    with (root/"external_sources/curation_queue.csv").open(encoding="utf-8-sig",newline="") as f:
        raw=list(csv.DictReader(f))
    if len({r["id"] for r in raw})!=len(raw):
        raise ValueError("duplicate external candidate ID")
    cfg=configs(root)
    rows=[classify(r,cfg,root) for r in raw]
    out=root/"external_sources/catalog"
    def save(path,records):
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=HEADER,lineterminator="\n")
            w.writeheader();w.writerows(records)
    save(out/"题目总索引.csv",rows)
    by_module=defaultdict(list)
    for item in rows:by_module[item["学科"]].append(item)
    for name,meta in cfg[2].items():
        save(out/"按学科"/(meta["folder"]+".csv"),by_module.get(name,[]))
    by_topic=defaultdict(list)
    for item in rows:
        if item["知识点"]!="未细分（待核验）":
            by_topic[(item["学科"],item["知识点"])].append(item)
    for lesson in cfg[0]["refresher_lessons"]:
        module=next(m for m in cfg[0]["modules"] if m["code"]==lesson["module"])
        path=out/"按知识点"/module["folder"]/(lesson["topic"]+".csv")
        save(path,by_topic.get((module["name"],lesson["label"]),[]))
    supplemental_rows=[x for x in rows if x["id"] in cfg[5]]
    for name,meta in cfg[2].items():
        save(out/"按知识点"/meta["folder"]/"补充题源.csv",
             [x for x in supplemental_rows if x["学科"]==name])
    translated=sum(bool(x["中文译稿"]) for x in rows)
    fine_pending=sum(x["知识点"]=="未细分（待核验）" for x in rows)
    report={"candidate_total":len(rows),"translated_drafts":translated,"mapped_topic_count":len(by_topic),
            "fine_classification_pending":fine_pending,
            "unclassified_total":len(by_module.get("待分类",[])),
            "by_module":dict(Counter(x["学科"] for x in rows)),
            "approved_external":0,
            "warning":"所有外部题目均未通过版权、物理答案及六轮审核。中文译稿仅初校。"}
    (out/"中文分类报告.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# 大学物理外部题源 · 中文分类导航","",f"候选记录：{len(rows)}；中英对照初校：{translated}；细分类待审：{fine_pending}。","",
           "**所有外部候选题仍不得正式组卷。** 原始英文文件保留原路径，不影响自动采集。","",
           "| 学科 | 数量 | 分类目录 |","| --- | ---: | --- |"]
    for m in cfg[0]["modules"]:
        lines.append(f'| {m["name"]} | {len(by_module[m["name"]])} | [CSV](按学科/{m["folder"]}.csv) |')
    lines.extend(["","## 按知识点检索（固定来源章节）",""])
    for lesson in cfg[0]["refresher_lessons"]:
        module=next(m for m in cfg[0]["modules"] if m["code"]==lesson["module"])
        target=f'按知识点/{module["folder"]}/{lesson["topic"]}.csv'
        lines.append(f'- {module["name"]} / {lesson["label"]}：[题目索引]({target})')
    lines.extend(["", "## 补充题源中文译稿（逐题初核）", ""])
    for name,meta in cfg[2].items():
        count=sum(x["学科"]==name for x in supplemental_rows)
        if count:
            lines.append("- " + name + "（" + str(count) +
                         "）：[补充题源索引](按知识点/" + meta["folder"] +
                         "/补充题源.csv)")
    lines+=["","[全量题目索引](题目总索引.csv) · [翻译与目录规范](../../docs/大学物理目录与翻译规范.md) · [中英术语表](../../localization/zh_CN/术语表.md)",
            "","注：知识点来源于固定章节才细分；其他候选只沿用现有学科、细分类保留待核验。译稿不代表答案已验证。",""]
    (out/"中文分类导航.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False))
    return report
if __name__=="__main__":
    generate()
