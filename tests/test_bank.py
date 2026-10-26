"""Unittest checks source isolation; not a substitute for independent physical review."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
from build import TOPICS, check, load_bank, render
from assemble_exam import assemble

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

    def test_generated_subfolder_relative_paths(self):
        source=render([self.items[0]],False,ROOT/'generated',ROOT)
        self.assertIn('../bank/',source)
        self.assertNotIn('data/problems.json',source)

if __name__=='__main__':
    unittest.main()
