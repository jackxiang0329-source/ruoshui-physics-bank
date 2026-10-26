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
        with self.assertRaises(ValueError):
            assemble(self.items,1,12,[],1,5,False)
        selected=assemble(self.items,6,12,[],1,5,True)
        self.assertEqual(6,len(selected))
        self.assertEqual(6,len(set(x['topic'] for x in selected)))

    def test_approval_requires_six_review_records(self):
        errors,total,approved=validate_reviews(ROOT)
        self.assertEqual([],errors)
        self.assertEqual(60,total)
        self.assertEqual(0,approved)
        self.assertEqual(64,len(digest_for(ROOT,'M007')))

    def test_exact_topic_quotas(self):
        selected=assemble(self.items,8,42,[],1,5,True,
                          quotas={'力学':2,'电磁学':2})
        self.assertEqual(8,len(selected))
        self.assertEqual(2,sum(p['topic']=='力学' for p in selected))
        self.assertEqual(2,sum(p['topic']=='电磁学' for p in selected))
        self.assertTrue(all(p['topic'] not in ('力学','电磁学')
                            for p in selected if p['id'] not in
                            {x['id'] for x in selected if x['topic'] in ('力学','电磁学')}))

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

    def test_generated_subfolder_relative_paths(self):
        source=render([self.items[0]],False,ROOT/'generated',ROOT)
        self.assertIn('../bank/',source)
        self.assertNotIn('data/problems.json',source)

if __name__=='__main__':
    unittest.main()
