"""Regression guards for reviewed content replacements (not academic approvals)."""
import json
import sys
import unittest
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from build import load_bank, check


class ReplacementRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {m['id']: m for m in load_bank(ROOT)}

    def test_all_six_replacements_stay_independently_addressable(self):
        errors, _ = check(list(self.data.values()), ROOT)
        self.assertEqual([], errors)
        for pid in ('T011', 'O016', 'O011', 'O012', 'W017', 'Q016'):
            self.assertEqual('待独立复核', self.data[pid]['quality_status'])
            for part in ('meta.json', 'question.tex', 'solution.tex'):
                self.assertTrue((ROOT / 'bank' / pid / part).is_file())

    def test_previous_near_duplicate_topics_are_separated(self):
        cases = {
            ('T004', 'T011'): '两块不同温度金属块接触',
            ('O008', 'O016'): '牛顿环',
            ('O002', 'O012'): '全反射临界角',
            ('O003', 'O011'): '视深',
            ('W007', 'W017'): '介质质点',
            ('Q003', 'Q016'): '不确定度',
        }
        for (original, changed), marker in cases.items():
            a = self.data[original]
            b = self.data[changed]
            self.assertNotEqual(a['title'], b['title'])
            self.assertIn(marker, b['title'] + ' ' +
                          (ROOT / 'bank' / changed / 'question.tex').read_text(encoding='utf-8'))
            self.assertTrue(set(a['tags']).isdisjoint(set(b['tags'])),
                            msg=changed + ': knowledge tags should now distinguish models')

    def test_replaced_multiple_choice_items_have_consistent_answer_keys(self):
        for pid in ('T011', 'O011', 'W017', 'Q016'):
            p = self.data[pid]
            self.assertEqual('选择题', p['kind'])
            self.assertEqual(['A','B','C','D'], [x[0] for x in p['choices']])
            self.assertEqual(r'\mathrm{' + p['correct_option'] + '}', p['answer'])
            tex = (ROOT / 'bank' / pid / 'question.tex').read_text(encoding='utf-8')
            for label, content in p['choices']:
                self.assertIn(r'\textbf{' + label + '.} ' + content, tex)

    def test_selected_independent_equation_relations(self):
        self.assertEqual(sp.Rational(300,400)*sp.Rational(300,200), sp.Rational(9,8))
        self.assertEqual(sp.Rational(1,1)/sp.Rational(4,3), sp.Rational(3,4))
        self.assertEqual(sp.Rational(1,1)/sp.Rational(625,1000), sp.Rational(8,5))
        self.assertEqual(
            (sp.Rational(9,10**6)-sp.Rational(3,10**6))/
            (10*sp.Rational(600,10**9)), 1)
        self.assertEqual((sp.Rational(1,4))/(sp.Rational(1,2)), sp.Rational(1,2))

    def test_answer_master_and_index_include_revised_titles(self):
        qbook = (ROOT / 'tex' / 'questions.tex').read_text(encoding='utf-8')
        sbook = (ROOT / 'tex' / 'solutions.tex').read_text(encoding='utf-8')
        import csv
        with (ROOT / 'data' / 'index.csv').open(encoding='utf-8-sig', newline='') as f:
            index = {r['id']: r for r in csv.DictReader(f)}
        for pid in ('T011', 'O016', 'O011', 'O012', 'W017', 'Q016'):
            p = self.data[pid]
            self.assertIn('【' + pid + '】 ' + p['title'], qbook)
            self.assertIn('【' + pid + '】 ' + p['title'], sbook)
            self.assertEqual(p['title'], index[pid]['title'])
            self.assertIn(r'\input{../bank/' + pid + '/solution.tex}', sbook)
            self.assertNotIn(r'\input{../bank/' + pid + '/solution.tex}', qbook)


if __name__ == '__main__':
    unittest.main()
