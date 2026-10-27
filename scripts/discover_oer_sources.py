#!/usr/bin/env python3
"""Discover public university physics exercise repositories without copying their content.

License metadata is only a discovery signal: every source must be independently
reviewed before enabling an importer or using a question in exams.
"""
import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUTPUT=ROOT/"external_sources"/"catalog"/"discovered_repositories.json"
QUERIES=[
    "physics problem bank in:name,description",
    "university physics exercises in:name,description",
    "physics open educational resources in:name,description",
]
LIMIT=30
UA="Ruoshui-Physics-OER-Discovery/1.0"


def collect():
    existing=json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {"schema":"physics-github-oer-discovery/v1","records":[]}
    known={r["full_name"].lower():r for r in existing["records"]}
    now=datetime.now(timezone.utc).isoformat()
    failures=[]
    added=[]
    for phrase in QUERIES:
        url="https://api.github.com/search/repositories?"+urllib.parse.urlencode({"q":phrase,"per_page":LIMIT,"sort":"updated","order":"desc"})
        headers={"User-Agent":UA,"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28"}
        token=os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"]="Bearer "+token
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=25) as response:
                result=json.load(response)
        except Exception as error:
            failures.append({"query":phrase,"reason":str(error)[:160]})
            continue
        for x in result.get("items",[]):
            if x.get("archived") or x.get("fork") or x.get("private"):
                continue
            fullname=x.get("full_name","")
            description=x.get("description") or ""
            combined=(fullname+" "+description).lower()
            if not re.search(r"(physics|mechanics|electromagnet|thermodynamic|optics|quantum)",combined):
                continue
            if not re.search(r"(problem|question|exercise|homework|course|educat|textbook|open)",combined):
                continue
            if fullname.lower() in known:
                known[fullname.lower()]["last_seen_utc"]=now
                known[fullname.lower()]["updated_at"]=x.get("updated_at")
                continue
            row={
                "full_name":fullname,"html_url":x.get("html_url"),
                "description":description[:350],"default_branch":x.get("default_branch"),
                "license_spdx_signal":(x.get("license") or {}).get("spdx_id"),
                "updated_at":x.get("updated_at"),
                "first_seen_utc":now,"last_seen_utc":now,
                "license_review":"pending",
                "reuse_permission_verified":False,
                "auto_import_enabled":False,
                "status":"discovered_only_not_a_question",
            }
            known[fullname.lower()]=row
            added.append(fullname)
    existing["records"]=sorted(known.values(),key=lambda x:x["full_name"].lower())
    existing["last_check_utc"]=now
    existing["last_new_repositories"]=len(added)
    existing["last_new_names"]=added[:60]
    existing["last_failures"]=failures
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(existing,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"new_repositories":len(added),"all_discovered":len(known),"failures":failures},ensure_ascii=False))
    return existing

if __name__=="__main__":
    collect()
