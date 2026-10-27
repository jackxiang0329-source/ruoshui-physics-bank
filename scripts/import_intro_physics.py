#!/usr/bin/env python3
"""Import pinned CC BY 4.0 undergraduate physics question excerpts for review only."""
import argparse, hashlib, json, re, unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote

BASE=Path(__file__).resolve().parent.parent/"external_sources"
REPO="saturnaxis/IntroPhysics"
REV="cd3ed19ede4206f68e6ea7c1e28c5961a872f3cb"
SIZE=1800000

def sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def canonical(s):
    return re.sub(r"\s+"," ",unicodedata.normalize("NFKC",s).casefold()).strip()

def fetch(path,cap=SIZE,timeout=15):
    url="https://raw.githubusercontent.com/"+REPO+"/"+REV+"/"+"/".join(quote(x,safe="") for x in path.split("/"))
    request=Request(url,headers={"User-Agent":"Ruoshui-Physics-OER/2.0"})
    with urlopen(request,timeout=timeout) as result:
        data=result.read(cap+1)
    if len(data)>cap: raise ValueError("source_too_large")
    return data

def verify_license(timeout):
    for path,expected,marker in [
        ("README.md","344a0d9f7de8f8cbe56923407b4a859fbc72959f","Creative Commons Attribution 4.0 International"),
        ("LICENSE.md","2f244ac814036ecd9ba9f69782e89ce6b1dca9eb","Attribution 4.0 International")
    ]:
        data=fetch(path,40000,timeout)
        if sha(data)!=expected or marker not in data.decode("utf-8"):
            raise ValueError("license_evidence_changed:"+path)

def extract(text):
    for index,cell in enumerate(json.loads(text)["cells"]):
        if cell.get("cell_type")!="markdown":continue
        source=cell.get("source","")
        body="".join(source) if isinstance(source,list) else source
        heading=re.search(r"(?im)^#{2,6}\s+\*\*Example Problem\*\*\s*:\s*(.+)$",body)
        start=re.search(r"(?i)\*\*The Problem\*\*\s*\n",body)
        if not heading or not start or "{exercise}" not in body:continue
        q=re.split(r"(?m)^\s*---\s*$|^\s*\*\*The Model\*\*|^\s*\x60{3,}\{(?:figure-md|dropdown|admonition)\}",body[start.end():],maxsplit=1)[0]
        q=re.sub(r"(?m)^\s*>\s?","",q).strip()
        if not 35<=len(q)<=5000:continue
        if re.search(r"(?i)<img|!\[[^]]*\]\(|\{numref\}|\{ref\}|\{figure|data:image|\\includegraphics|https?://[^\s)]*\.(?:png|jpg|svg)|from openstax|adapted from|taken from|©|all rights reserved|figure\s+\d|shown in (?:the|a) figure",q):continue
        yield index,heading.group(1).strip().strip("*"),q,hashlib.sha256(canonical(q).encode()).hexdigest()

def run(limit=100,timeout=15):
    directory=BASE/"intro_physics"
    mp=directory/"source_manifest.json"
    ip=directory/"index.json"
    manifest=json.loads(mp.read_text(encoding="utf-8"))
    index=json.loads(ip.read_text(encoding="utf-8"))
    if manifest["repository"]!=REPO or manifest["revision"]!=REV:raise ValueError("source_pin_mismatch")
    verify_license(timeout)
    seen={(x["source_path"],x["cell_index"],x["question_sha256"]) for x in index["records"]}
    hashes={x["question_sha256"] for x in index["records"]}
    next_id=max((int(x["id"].split("-")[-1]) for x in index["records"]),default=0)
    pending=[x for x in manifest["notebooks"] if not x.get("processed")]
    added=[];failed=[];inspected=0
    with ThreadPoolExecutor(max_workers=5) as pool:
        tasks={x["path"]:pool.submit(fetch,x["path"],SIZE,timeout) for x in pending}
        for item in pending:
            path=item["path"]
            try:
                raw=tasks[path].result()
                if sha(raw)!=item["sha"]:raise ValueError("upstream_git_sha_mismatch")
                questions=list(extract(raw.decode("utf-8")))
                inspected+=len(questions)
                for cell,title,question,h in questions:
                    key=(path,cell,h)
                    if key in seen or h in hashes:continue
                    if len(added)>=limit:break
                    next_id+=1;pid="IP-"+str(next_id).zfill(4)
                    dest=directory/"raw"/(pid+".md")
                    if dest.exists():raise ValueError("destination_collision")
                    dest.parent.mkdir(parents=True,exist_ok=True)
                    link="https://github.com/"+REPO+"/blob/"+REV+"/"+path
                    dest.write_text("# "+title+"\n\n"+question+"\n\n---\n"+"Attribution: Billy Quarles, Introductory Physics, East Texas A&M University, CC BY 4.0. Rights review pending.\nOriginal: "+link+"\nUpstream Git blob SHA: "+item["sha"]+"\nNot exam-ready.\n",encoding="utf-8")
                    index["records"].append({"id":pid,"title":title,"module":"物理基础" if path.startswith("Chapter01/") else "力学","source":"Billy Quarles — PHYS 2425 University Physics I","source_repository":REPO,"source_revision":REV,"source_path":path,"source_sha":item["sha"],"source_url":link,"cell_index":cell,"question_sha256":h,"license":"CC BY 4.0 (repository-level; rights review pending)","license_review":"pending","semantic_dedup":"pending","answer_verified":False,"exam_eligible":False,"status":"raw_candidate_requires_review"})
                    seen.add(key);hashes.add(h);added.append(pid)
                if len(added)>=limit:break
                item["processed"]=True
                item["extracted_count"]=len(questions)
            except Exception as exc:failed.append({"path":path,"reason":str(exc)[:200]})
    index["count"]=len(index["records"]);manifest["imported"]=len(index["records"])
    for path,obj in ((mp,manifest),(ip,index)):
        path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"source":REPO,"revision":REV,"added_count":len(added),"added":added,"extracted_candidates":inspected,"notebooks_pending":sum(not x.get("processed") for x in manifest["notebooks"]),"failures":failed,"exam_ready_added":0}
    logs=BASE/"logs";logs.mkdir(parents=True,exist_ok=True)
    (logs/"intro_physics_latest.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--limit",type=int,default=100)
    p.add_argument("--timeout",type=int,default=15)
    args=p.parse_args()
    if not 1<=args.limit<=100:p.error("limit must be 1..100")
    run(args.limit,args.timeout)
