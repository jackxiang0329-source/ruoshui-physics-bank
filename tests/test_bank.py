"""Unittest checks source isolation; not a substitute for independent physical review."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
from build import TOPICS, check, load_bank, render
from assemble_exam import assemble, assign_points
from check_review import validate as validate_reviews, digest_for
from audit_milestone import audit, verify_index_metadata, verify_master_metadata

class BankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items=load_bank(ROOT)

    def test_unique_metadata_and_fragments(self):
        errs,counts=check(self.items,ROOT)
        self.assertEqual([],errs)
        self.assertEqual(len(self.items),sum(counts.values()))
        self.assertGreaterEqual(len(self.items),36)

    def test_question_book_inputs_no_embedded_answer(self):
        source=render(self.items,False,ROOT/'tex',ROOT)
        self.assertIn(r'\input{../bank/M001/question.tex}',source)
        self.assertNotIn('/solution.tex',source)
        self.assertIn(r'\documentclass[lang=cn,color=blue,11pt]{elegantbook}',source)

    def test_solutions_book_inputs(self):
        source=render(self.items,True,ROOT/'tex',ROOT)
        self.assertIn(r'\input{../bank/M001/solution.tex}',source)

    def test_pending_default_gate(self):
        verified=[p for p in self.items if p['quality_status']=='质检通过']
        if not verified:
            with self.assertRaises(ValueError):
                assemble(self.items,1,12,[],1,5,False)
        else:
            errors, _, approved=validate_reviews(ROOT)
            self.assertEqual([],errors)
            self.assertEqual(approved,len(verified))
            selected=assemble(self.items,1,12,[],1,5,False)
            self.assertTrue(all(p['quality_status']=='质检通过' for p in selected))
        draft=assemble(self.items,6,12,[],1,5,True)
        self.assertEqual(6,len(draft))
        self.assertEqual(6,len(set(x['topic'] for x in draft)))

    def test_single_choice_options_are_structured_and_displayed(self):
        choices=[p for p in self.items if p['kind']=='选择题']
        self.assertGreaterEqual(len(choices),14)
        self.assertTrue(all(p['correct_option'] in ('A','B','C','D') for p in choices))
        for item in choices:
            tex=(ROOT/'bank'/item['id']/'question.tex').read_text(encoding='utf-8')
            self.assertEqual(4,len(item['choices']))
            for label,value in item['choices']:
                self.assertIn('\\textbf{'+label+'.} '+value,tex)
            self.assertEqual('\\mathrm{'+item['correct_option']+'}',item['answer'])

    def test_approval_requires_six_review_records(self):
        errors,total,approved=validate_reviews(ROOT)
        self.assertEqual([],errors)
        self.assertGreaterEqual(total,100)
        self.assertEqual(approved,sum(p['quality_status']=='质检通过' for p in self.items))
        self.assertEqual(64,len(digest_for(ROOT,'M007')))

    def test_exact_topic_quotas(self):
        selected=assemble(self.items,8,42,[],1,5,True,
                          quotas={'力学':2,'电磁学':2})
        self.assertEqual(8,len(selected))
        self.assertEqual(2,sum(p['topic']=='力学' for p in selected))
        self.assertEqual(2,sum(p['topic']=='电磁学' for p in selected))
        self.assertEqual(4,sum(p['topic'] not in ('力学','电磁学') for p in selected))

    def test_exam_duration_and_reproducibility(self):
        a=assemble(self.items,6,123,[],1,5,True,max_minutes=120)
        b=assemble(self.items,6,123,[],1,5,True,max_minutes=120)
        self.assertEqual([p['id'] for p in a],[p['id'] for p in b])
        self.assertLessEqual(sum(p['estimated_minutes'] for p in a),120)
        with self.assertRaises(ValueError):
            assemble(self.items,6,123,[],1,5,True,max_minutes=1)

    def test_difficulty_weighted_scores(self):
        selected=assemble(self.items,10,42,[],1,5,True)
        scores=assign_points(selected,100)
        self.assertEqual(len(selected),len(scores))
        self.assertTrue(all(isinstance(s,int) and s>0 for s in scores))
        self.assertEqual(100,sum(scores))
        with self.assertRaises(ValueError):
            assign_points(selected,9)

    def test_topic_quota_impossible_is_rejected(self):
        with self.assertRaises(ValueError):
            assemble(self.items,5,1,[],1,5,True,quotas={'力学':6})

    def test_new_integrated_items_have_independent_fragments(self):
        ids=('M013','M014','E013','E014','T013','T014',
             'W013','W014','O013','O014','Q013','Q014')
        for pid in ids:
            folder=ROOT/'bank'/pid
            self.assertTrue((folder/'meta.json').is_file())
            self.assertTrue((folder/'question.tex').is_file())
            self.assertTrue((folder/'solution.tex').is_file())

    def test_first_100_milestone_structural_coverage(self):
        errors, summary=audit(ROOT,minimum=100)
        self.assertEqual([],errors)
        self.assertGreaterEqual(summary['written_questions'],100)
        self.assertEqual(summary['defined_formula_checks'],summary['written_questions'])
        self.assertEqual(summary['qa_pending']+summary['qa_approved_declared'],
                         summary['written_questions'])

    def test_csv_field_drift_is_detected_before_publication(self):
        p=self.items[0]
        good={
            'id':p['id'],'topic':p['topic'],'kind':p['kind'],
            'level':str(p['level']),'estimated_minutes':str(p['estimated_minutes']),
            'title':p['title'],'tags':';'.join(p['tags']),
            'quality_status':p['quality_status'],
        }
        self.assertEqual([],verify_index_metadata([good],[p]))
        for changed in ('title','kind','level','estimated_minutes',
                        'tags','quality_status'):
            altered=good.copy()
            altered[changed]='DELIBERATELY_INVALID'
            errors=verify_index_metadata([altered],[p])
            self.assertTrue(errors,msg='Audit missed '+changed)

    def test_master_metadata_and_answer_drift_is_detected(self):
        qbook=(ROOT/'tex'/'questions.tex').read_text(encoding='utf-8')
        sbook=(ROOT/'tex'/'solutions.tex').read_text(encoding='utf-8')
        self.assertEqual([], verify_master_metadata(self.items,qbook,sbook))
        item=self.items[0]
        broken_question=qbook.replace(item['title'],'题名意外改动',1)
        self.assertTrue(verify_master_metadata(self.items,broken_question,sbook))
        original=r'\displaystyle '+item['answer']
        self.assertIn(original,sbook)
        broken_solution=sbook.replace(original,r'\displaystyle 123456',1)
        self.assertTrue(verify_master_metadata(self.items,qbook,broken_solution))

    def test_generated_subfolder_relative_paths(self):
        source=render([self.items[0]],False,ROOT/'generated',ROOT)
        self.assertIn('../bank/',source)
        self.assertNotIn('data/problems.json',source)

if __name__=='__main__':
    unittest.main()
