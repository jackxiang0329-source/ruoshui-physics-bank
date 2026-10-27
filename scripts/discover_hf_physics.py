#!/usr/bin/env python3
"""Find Hugging Face physics datasets without automatically copying unreviewed content."""
import json
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parent.parent
CAT=ROOT/"external_sources"/"catalog"/"huggingface_datasets.json"
SEARCHES=["physics","physics problems","university physics","physics qa"]
def scan(provider=None,path=CAT):
    old=json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"schema":1,"records":[]}
    known={x["dataset_id"].casefold():x for x in old["records"]}
    when=datetime.now(timezone.utc).isoformat()
    added=[];failed=[]
    for search in SEARCHES:
        try:
            if provider:found=provider(search)
            else:
                url="https://huggingface.co/api/datasets?"+urlencode({"search":search,"limit":50})
                with urlopen(Request(url,headers={"User-Agent":"Ruoshui-Physics-OER/2.2"}),timeout=18) as f:raw=f.read(4000001)
                if len(raw)>4000000:raise ValueError("discovery_response_too_large")
                found=json.loads(raw)
            if not isinstance(found,list):raise ValueError("invalid_results")
            for x in found:
                key=x.get("id")
                if not isinstance(key,str) or "/" not in key or x.get("private") or x.get("gated"):continue
                if not any(w in key.casefold() for w in ("phys","mechanic","optics","quantum")):continue
                lic=(x.get("cardData") or {}).get("license") or x.get("license") or next(
                    (v.split(":",1)[1] for v in x.get("tags",[]) if v.startswith("license:")),None)
                if key.casefold() in known:
                    known[key.casefold()]["last_seen_utc"]=when;continue
                known[key.casefold()]={
                    "dataset_id":key,"url":"https://huggingface.co/datasets/"+key,
                    "license_signal":lic,"revision_seen":x.get("sha"),
                    "first_seen_utc":when,"last_seen_utc":when,
                    "status":"NC_restricted_review" if lic and "-nc" in str(lic) else "license_and_source_review_pending",
                    "license_verified":False,"auto_import_enabled":False,
                }
                added.append(key)
        except Exception as exc:failed.append({"query":search,"reason":str(exc)[:180]})
    old.update({"records":sorted(known.values(),key=lambda x:x["dataset_id"].casefold()),
      "last_checked_utc":when,"new_count":len(added),"new_names":added,"errors":failed})
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(old,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"new":len(added),"total":len(known),"failures":failed},ensure_ascii=False))
    return old
if __name__=="__main__":scan()
