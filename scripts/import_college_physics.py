#!/usr/bin/env python3
"""Copy independent College Physics exercises from a pinned CC BY 3.0 source.

Copied markup is a raw MathML/HTML excerpt, not an exam-ready LaTeX question.
Skip figures, broken cross-references and non-standalone problems.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent.parent / "external_sources"
REPO = "philschatz/physics-book"
REV = "a7efaa7e221fab1694022d8bb98b83a73ee31d3d"
LIC_SHA = "83863a52718b273acbf27c1a0dc91a28f9c94ea5"
SOURCE = "college_physics"
MAX_SIZE = 210_000
TAG = re.compile(r"</?div\b[^>]*>", re.I)
EX_START = re.compile(r'<div\s+data-type="exercise"[^>]*>', re.I)
PROBLEM_START = re.compile(r'<div\s+data-type="problem"[^>]*>', re.I)
SKIP = re.compile(
    r'(?i)\[\[link\]\]|\]\(#|<img\b|!\[[^]]*\]\(|'
    r'(?:figure|diagram|graph|photo|image|chart)\s+\d|'
    r'(?:(?:refer|see)\s+to\s+)(?:figure|fig|diagram|graph)|'
    r'<!--|(?:https?://[^\s"<>]*\.(?:png|jpg|svg))|'
    r'copyright\s+\d|©|all rights reserved'
)
MODULES = [
    ("物理基础", ("unit", "measure", "problem-solving", "significant figure", "scope and scale",
                 "physics: an introduction", "approximation")),
    ("热学", ("thermodynam", "temperature", "heat", "gas", "entropy")),
    ("光学", ("optics", "lens", "refraction", "diffraction", "interference", "light")),
    ("电磁学", ("electric", "magnet", "capacit", "circuit", "current", "charge", "induct")),
    ("振动与波动", ("wave", "oscill", "sound", "vibrat", "resonan")),
    ("近代物理", ("quantum", "nuclear", "atomic", "relativ", "particle", "radiation")),
    ("力学", ("motion", "velocity", "acceleration", "kinemat", "force", "momentum",
             "rotat", "gravity", "gravitat", "energy", "fluid", "pressure", "mechanic", "work",
             "displace", "velocit", "elast", "stress", "strain", "newton", "friction",
             "equilibrium", "torque", "collision", "falling object", "impulse", "power",
             "vector", "satellite", "kepler", "archimedes", "cohesion", "adhesion",
             "surface tension", "capillary", "bernoulli", "rocket propulsion",
             "density", "pascal", "viscosity", "laminar", "poiseuille",
             "simple machine", "stability")),
]
def source_url(path):
    return "https://raw.githubusercontent.com/" + REPO + "/" + REV + "/" + "/".join(quote(x,safe="") for x in path.split("/"))
def get(url,limit,timeout):
    with urlopen(Request(url, headers={"User-Agent":"RuoshuiPhysicsOER/2.4"}),timeout=timeout) as r:
        data = r.read(limit+1)
    if len(data)>limit:
        raise ValueError("source_exceeds_size_limit")
    return data
def sha_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def norm(s):
    return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",s).casefold()).strip()
def group(title):
    name=title.casefold()
    return next((label for label,keys in MODULES if any(k in name for k in keys)),"待分类")
def block(html,start):
    """Slice one balanced <div> element including any nested <div>s."""
    stack=0
    for match in TAG.finditer(html,start):
        if match.group(0).lower().startswith("</div"):
            stack-=1
            if stack==0:
                return html[start:match.end()]
        else:
            stack+=1
    return None
def parse(html):
    title_match=re.search(r'(?m)^title:\s*"([^"]+)"',html)
    title=title_match.group(1) if title_match else "Unknown chapter"
    result=[]
    for i,match in enumerate(EX_START.finditer(html)):
        exercise=block(html,match.start())
        if not exercise:
            continue
        if not ('data-element-type="problems-exercises"' in match.group(0)
                or 'data-element-type="conceptual-questions"' in match.group(0)):
            continue
        problem=PROBLEM_START.search(exercise)
        if not problem:
            continue
        body=block(exercise,problem.start())
        if not body:
            continue
        content=body[problem.end()-problem.start():]
        content=re.sub(r"</div>\s*$","",content).strip()
        if not 30<=len(content)<=9500 or SKIP.search(content):
            continue
        if "<div" in content or re.search(r"\.\./resources/|<media|<figure",content,re.I):
            continue
        normalized=norm(content)
        if not 25<=len(normalized)<=3500:
            continue
        digest=hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        result.append({"ordinal":i,"section":title,"content":content,
                       "digest":digest,"class":"calculation" if
                       'data-element-type="problems-exercises"' in match.group(0)
                       else "conceptual"})
    return result
def load(path,default):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default
def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def license_check(timeout):
    raw=get(source_url("LICENSE.txt"),2000,timeout)
    if sha_blob(raw)!=LIC_SHA or b"Creative Commons Attribution 3.0 Unported License" not in raw:
        raise ValueError("college_physics_license_evidence_mismatch")
def build_manifest(timeout):
    tree=json.loads(get(
        "https://api.github.com/repos/"+REPO+"/git/trees/"+REV+"?recursive=1",1200000,timeout
    ).decode("utf-8"))
    if tree.get("truncated"):
        raise ValueError("source_tree_truncated")
    files=[{"path":x["path"],"sha":x["sha"],"bytes":x["size"],"processed":False}
           for x in tree.get("tree",[]) if x.get("type")=="blob" and
           re.fullmatch(r"contents/m[0-9]+\.md",x.get("path","")) and
           x.get("size",MAX_SIZE+1)<=MAX_SIZE]
    if len(files)<150:
        raise ValueError("source_manifest_expected_modules_missing")
    return {"repository":REPO,"revision":REV,"license":"CC BY 3.0 Unported",
            "imported":0,"modules":files}
def run(limit=250,max_files=40,timeout=15,base=BASE):
    root=base/SOURCE
    mp,ip=root/"source_manifest.json",root/"index.json"
    index=load(ip,{"records":[],"count":0,"exam_eligible_count":0})
    manifest=load(mp,None)
    license_check(timeout)
    if manifest is None:
        manifest=build_manifest(timeout)
    if manifest.get("repository")!=REPO or manifest.get("revision")!=REV:
        raise ValueError("source_manifest_revision_or_repository_invalid")
    seen={v["question_sha256"] for v in index["records"]}
    serial=max((int(x["id"].split("-")[-1]) for x in index["records"]),default=0)
    targets=[v for v in manifest["modules"] if not v.get("processed")][:max_files]
    added,failures=[],[]
    reasons=Counter()
    with ThreadPoolExecutor(max_workers=8) as pool:
        tasks={v["path"]:pool.submit(get,source_url(v["path"]),MAX_SIZE,timeout) for v in targets}
        for module in targets:
            path=module["path"]
            try:
                original=tasks[path].result()
                if sha_blob(original)!=module["sha"]:
                    raise ValueError("source_blob_sha_mismatch")
                examples=parse(original.decode("utf-8"))
                for item in examples:
                    if item["digest"] in seen:
                        reasons["normalized_duplicate"]+=1
                        continue
                    if len(added)>=limit:
                        break
                    serial+=1
                    pid="CP-"+str(serial).zfill(5)
                    dst=root/"raw"/(pid+".md")
                    if dst.exists():
                        raise ValueError("output_id_collision")
                    dst.parent.mkdir(parents=True,exist_ok=True)
                    url="https://github.com/"+REPO+"/blob/"+REV+"/"+path
                    dst.write_text("# "+item["section"]+" — "+pid+"\n\n"+item["content"]
                        +"\n\n---\n"
                        +"Attribution: OpenStax College, *College Physics* (2014); CC BY 3.0 Unported.\n"
                        +"Upstream: "+url+"\nGit source blob SHA: "+module["sha"]
                        +"\nRaw HTML/MathML source excerpt, not exam-approved.\n",
                        encoding="utf-8")
                    index["records"].append({
                        "id":pid,"title":item["section"],"module":group(item["section"]),
                        "question_type":item["class"],"license":"CC BY 3.0 Unported",
                        "author":"OpenStax College","source_url":url,"source_path":path,
                        "source_revision":REV,"source_sha":module["sha"],
                        "exercise_index":item["ordinal"],"question_sha256":item["digest"],
                        "requires_markup_conversion":True,"license_review":"pending",
                        "semantic_dedup":"pending","answer_verified":False,
                        "exam_ready":False,"status":"raw_candidate_requires_review"
                    })
                    seen.add(item["digest"]);added.append(pid)
                if len(added)>=limit:
                    break
                module["processed"]=True
                module["extracted_candidates"]=len(examples)
            except Exception as e:
                failures.append({"path":path,"reason":str(e)[:190]})
    manifest["imported"]=len(index["records"])
    index["count"]=len(index["records"])
    save(mp,manifest);save(ip,index)
    report={"timestamp_utc":datetime.now(timezone.utc).isoformat(),
            "source":REPO,"revision":REV,"added_count":len(added),
            "added_ids":added,"candidate_files_checked":len(targets),
            "modules_pending":sum(not x.get("processed") for x in manifest["modules"]),
            "skipped_reasons":dict(reasons),"failures":failures,"exam_ready_added":0}
    save(base/"logs"/"college_physics_latest.json",report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--limit",type=int,default=250)
    p.add_argument("--max-files",type=int,default=40)
    p.add_argument("--timeout",type=int,default=15)
    a=p.parse_args()
    if not 1<=a.limit<=250 or not 1<=a.max_files<=50:
        p.error("limit must be <=250; max-files <=50")
    run(a.limit,a.max_files,a.timeout)
