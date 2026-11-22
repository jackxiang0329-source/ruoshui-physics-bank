#!/usr/bin/env python3
"""Cross-check chapter, IDs, provisional review gates for all 238 thought-question candidates.
This is structural/provenance QC ONLY, not 238 validated physical arguments.
"""
import json
import re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent
P=re.compile(r"\\paragraph\{思考题\s+(\d+\.\d+)\}")
def require(ok,desc):
 if not ok: raise AssertionError(desc)
def validate_register(register_name,root,expected,chapterfield,numberfield,registry_title):
 reg=json.loads((ROOT/register_name).read_text(encoding="utf-8"))
 entries=reg["entries"]
 require(len(entries)==expected,f"{registry_title} count mismatch {len(entries)}")
 require(len(set(e["canonical_id"] for e in entries))==expected, f"{registry_title} duplicate canonical_id")
 ids=[str(e[numberfield]) for e in entries]
 require(len(set(ids))==expected,f"{registry_title} duplicate question ID")
 bychapter=Counter(int(s.split(".")[0]) for s in ids)
 require(len(ids)==sum(bychapter.values()),"count mismatch")
 for item in reg["chapters"]:
  chap=int(item["chapter"])
  count=item["source_thought_count"] if root=="thought_questions" else item["count"]
  require(bychapter[chap]==count,f"Chapter {chap} register count {count} != {bychapter[chap]}")
  qpath=ROOT/root/f"{chap:02d}"/"questions.tex"
  spath=ROOT/root/f"{chap:02d}"/"solutions.tex"
  qids=P.findall(qpath.read_text(encoding="utf-8"))
  sids=P.findall(spath.read_text(encoding="utf-8"))
  required=set(str(e[numberfield]) for e in entries if int(str(e[numberfield]).split(".")[0])==chap)
  require(len(qids)==len(set(qids))==count,f"chapter {chap} duplicate/missing questions")
  require(len(sids)==len(set(sids))==count,f"chapter {chap} duplicate/missing solutions")
  require(set(qids)==required and set(sids)==required,f"chapter {chap} register-vs-files mismatch")
 for e in entries:
  chapter=int(str(e[numberfield]).split(".")[0])
  require(str(e[numberfield]).startswith(f"{chapter}."),"number mismatch")
  require(e["academic_review"]=="pending_independent_verification" and e["exam_ready"] is False,f"premature approval in {registry_title}: {e[numberfield]}")
  require(e["question_file"]==f"{root}/{chapter:02d}/questions.tex" and e["solution_file"]==f"{root}/{chapter:02d}/solutions.tex",f"mismatched file mapping {e[numberfield]}")
 if root=="thought_questions":
  require(reg["thought_question_count"]==207 and reg["thought_solution_count"]==207,"V2 count")
  require(reg["publication_rights_status"]=="not_checked", "V2 copyright gate")
 else:
  require(reg["companion_selected_thought_count"]==31 and reg["companion_selected_solution_count"]==31, "S count")
  require(reg["do_not_duplicate_with_future_V1_full_intake"] is True,"V1 duplicate-prevention gate")
  require(all(e["main_book_original_thought_status"]=="not_checked_unavailable_V1_scan" for e in entries),"V1 source scope changed without recheck")
  require(all(e["source_rights_status"]=="not_checked" for e in entries),"S copyright gate")
 print(f"PASS {registry_title}: {expected} existing candidates ID mapping, chapter counts, Q/S presence, academic and copyright gates; zero new originals")
 return set((registry_title,e[numberfield]) for e in entries)
def main():
 v2=validate_register("thought_register.json","thought_questions",207,"chapter","source_thought_number","V2")
 s=validate_register("supplement_selected_thought_register.json","supplement_selected_thought",31,"chapter","source_thought_number","S")
 require(len(v2 | s)==238,"mixed-namespace collision")
 print("PASS 238 thought-candidate provenance/structure records; NOT 238 proof checks, source originals still unverified")
if __name__=="__main__": main()
