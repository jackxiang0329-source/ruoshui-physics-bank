#!/usr/bin/env python3
"""Hugging Face physics-question importer: staging only; never exam-ready."""
import argparse, hashlib, json, re, time, unicodedata
from urllib.error import HTTPError, URLError
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE=Path(__file__).resolve().parent.parent/"external_sources"
DATASET="yusufbaykaloglu/Physics-DPO-Dataset"
PATH=BASE/"hf_physics_dpo"
MODULES={
 "力学":("gravitation","mechanic","force","dynamics","kinematic","conservation","orbital","energy","momentum","rotation","fluid","viscous","bernoulli","friction","drag","elasticity","statics"),
 "热学":("thermo","thermal","heat","temperature","gas_","entropy","kinetic_theory","phase_transition"),
 "电磁学":("electromagnet","electric","magnet","circuit","capacitor","capacitance","electrostatics","gauss_law","maxwell","kirchhoff","current_and_resistance"),
 "光学":("optics","diffraction","refraction","interference","laser","polarization"),
 "振动与波动":("wave","oscillation","oscillatory","acoustic","vibration","sound"),
 "近代物理":("quantum","atomic","nuclear","relativity","particle","solid_state","superconductivity","semiconductor"),
}
def checksum(s):
    t=re.sub(r"\s+"," ",unicodedata.normalize("NFKC",s).casefold()).strip()
    return hashlib.sha256(t.encode("utf-8")).hexdigest()
def category(s):
    s=str(s).casefold().replace("-","_")
    return next((label for label,hints in MODULES.items() if any(x in s for x in hints)),"待分类")
def api(url,timeout=20):
    req=Request(url,headers={"Accept":"application/json","User-Agent":"Ruoshui-Physics-OER/2.2"})
    for attempt in range(3):
        try:
            with urlopen(req,timeout=timeout) as resp:
                raw=resp.read(6000001)
            if len(raw)>6000000:raise ValueError("json_response_too_large")
            return json.loads(raw.decode("utf-8"))
        except HTTPError as exc:
            if attempt==2 or exc.code not in (429,500,502,503,504):
                raise
        except (URLError,TimeoutError):
            if attempt==2:
                raise
        time.sleep(1.5*(attempt+1))
def verified_revision(timeout):
    m=api("https://huggingface.co/api/datasets/"+DATASET,timeout)
    license_signal=(m.get("cardData") or {}).get("license")
    if license_signal!="apache-2.0" and "license:apache-2.0" not in m.get("tags",[]):
        raise ValueError("license_not_explicit_apache_2_0")
    if m.get("private") or m.get("gated") not in (False,None):
        raise ValueError("dataset_is_private_or_gated")
    revision=m.get("sha")
    if not re.fullmatch(r"[0-9a-f]{40}",str(revision)):
        raise ValueError("invalid_upstream_commit")
    return revision
def eligible(x):
    q=x.get("prompt")
    if not isinstance(q,str) or not 60<=len(q)<=3500:return None
    if re.search(r"(?i)<img|!\[[^]]*\]\(|\{numref\}|(?:figure|diagram)\s*\d|see the diagram|shown in the figure|https?://\S+\.(?:png|jpg|svg)|ignore previous instructions",q):
        return None
    return q.strip()
def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def read(path,fallback):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else fallback

def run(limit=500,scan_limit=1000,timeout=20,revision_provider=None,page_provider=None,base=BASE):
    directory=base/"hf_physics_dpo"
    mp,ip=directory/"manifest.json",directory/"index.json"
    m=read(mp,{"dataset":DATASET,"config":"default","split":"train","revision":None,"next_offset":0,"total_rows":None})
    idx=read(ip,{"count":0,"exam_eligible_count":0,"records":[]})
    if m["dataset"]!=DATASET or m["config"]!="default" or m["split"]!="train":
        raise ValueError("source_manifest_identity_mismatch")
    check=revision_provider or (lambda:verified_revision(timeout))
    version=check()
    if m.get("revision") and m["revision"]!=version:
        raise ValueError("upstream_revision_changed_manual_review_required")
    m["revision"]=version
    def fetch_page(offset,length):
        return api("https://datasets-server.huggingface.co/rows?"+urlencode({
            "dataset":DATASET,"config":"default","split":"train",
            "offset":offset,"length":length}),timeout)
    get_rows=page_provider or fetch_page
    offset=int(m["next_offset"])
    start=offset
    total=m.get("total_rows")
    serial=max((int(x["id"].split("-")[-1]) for x in idx["records"]),default=0)
    known={x["question_sha256"] for x in idx["records"]}
    accepted=[];checked=0;skipped={};failures=[]
    def skip(reason):skipped[reason]=skipped.get(reason,0)+1
    try:
        while checked<scan_limit and len(accepted)<limit:
            if isinstance(total,int) and offset>=total:break
            page=get_rows(offset,min(100,scan_limit-checked))
            if page.get("partial"):raise ValueError("incomplete_hf_dataset_view")
            if not {"prompt","domain"}.issubset({x.get("name") for x in page.get("features",[])}):
                raise ValueError("unexpected_hf_dataset_schema")
            total=page.get("num_rows_total")
            if not isinstance(total,int):raise ValueError("missing_total_rows")
            rows=page.get("rows",[])
            if not rows:break
            for item in rows:
                if item.get("row_idx")!=offset:raise ValueError("hf_rows_not_contiguous")
                row=item.get("row") or {}
                row_idx=offset;offset+=1;checked+=1
                q=eligible(row)
                if q is None:skip("invalid_or_media_dependent_question");continue
                subject=row.get("domain")
                if not isinstance(subject,str) or not subject.strip():
                    skip("missing_physics_domain");continue
                digest=checksum(q)
                if digest in known:skip("duplicate_normalized_question");continue
                if len(accepted)>=limit:break
                serial+=1
                qid="HFDPO-"+str(serial).zfill(5)
                dest=directory/"raw"/(qid+".md")
                if dest.exists():raise ValueError("id_collision")
                dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_text("# "+qid+"\n\n"+q+"\n\n---\n"
                    +"Source: https://huggingface.co/datasets/"+DATASET
                    +"\nRow: "+str(row_idx)+"\nUpstream revision observed: "+version
                    +"\nLicense signal: Apache-2.0; underlying rights review pending."
                    +"\nGenerated content: answer and physics correctness unverified."
                    +"\nNot exam-ready.\n",encoding="utf-8")
                idx["records"].append({
                    "id":qid,"source":DATASET,"source_url":"https://huggingface.co/datasets/"+DATASET,
                    "row_idx":row_idx,"dataset_revision_observed":version,
                    "domain":subject,"module":category(subject),
                    "difficulty_signal":row.get("difficulty"),
                    "question_sha256":digest,
                    "license":"Apache-2.0 (source metadata; rights review pending)",
                    "author":"Dataset contributors (see original dataset card)",
                    "semantic_dedup":"pending","license_review":"pending",
                    "answer_verified":False,"exam_ready":False,
                    "status":"synthetic_question_requires_academic_review",
                })
                known.add(digest);accepted.append(qid)
                if len(accepted)>=limit:break
            if len(rows)<min(100,scan_limit-checked+len(rows)):break
    except Exception as e:
        failures.append({"offset":offset,"reason":str(e)[:220]})
    # Do not commit a potentially mixed-version batch.
    if check()!=version:raise ValueError("hf_revision_drift_no_commit_allowed")
    m["next_offset"]=offset;m["total_rows"]=total
    idx["count"]=len(idx["records"])
    write(mp,m);write(ip,idx)
    report={
      "timestamp_utc":datetime.now(timezone.utc).isoformat(),
      "run_id":__import__("os").environ.get("GITHUB_RUN_ID","local"),
      "source":DATASET,"source_revision_observed":version,
      "added_count":len(accepted),"added_ids":accepted,"scanned":checked,
      "offset_before":start,"offset_after":offset,"total_rows":total,
      "skipped":skipped,"failures":failures,"exam_ready_added":0,
      "note":"Source is synthetic. Dataset viewer rows are not revision-pinned; each copied question is SHA256-hashed."
    }
    log_dir=base/"logs"
    write(log_dir/"huggingface_import_latest.json",report)
    day=log_dir/(datetime.now(timezone.utc).strftime("%Y-%m-%d")+"-huggingface.jsonl")
    with day.open("a",encoding="utf-8") as f:f.write(json.dumps(report,ensure_ascii=False)+"\n")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report
if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--limit",type=int,default=500)
    a.add_argument("--scan-limit",type=int,default=1000)
    a.add_argument("--timeout",type=int,default=20)
    opts=a.parse_args()
    if not 1<=opts.limit<=500 or not 1<=opts.scan_limit<=1000:a.error("limits exceeded")
    run(opts.limit,opts.scan_limit,opts.timeout)
