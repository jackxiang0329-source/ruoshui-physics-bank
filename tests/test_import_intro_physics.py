import sys, unittest, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import import_intro_physics as importer
class TestExtract(unittest.TestCase):
    def test_standalone(self):
        body='### **Example Problem**: Uniform acceleration\n'+chr(96)*4+'{exercise}\n**The Problem**\n\n> A ball is moving along a straight path with a fixed acceleration for ten seconds. Find the final speed given its initial velocity.\n\n---\n\n**The Model**\nThe answer'
        cell={'cell_type':'markdown','source':body}
        found=list(importer.extract(json.dumps({'cells':[cell]})))
        self.assertEqual(len(found),1)
        self.assertIn('Find the final speed',found[0][2])
        self.assertNotIn('The answer',found[0][2])
    def test_figure_skip(self):
        body='### **Example Problem**: With Figure\n'+chr(96)*3+'{exercise}\n**The Problem**\n\nA beam in the figure is loaded as Figure {numref}x with a certain force. Find the reaction at support A.\n---'
        self.assertEqual(list(importer.extract(json.dumps({'cells':[{'cell_type':'markdown','source':body}]}))),[])
    def test_normalized_hash(self):
        self.assertEqual(importer.canonical('One    Force'),importer.canonical('one force'))

if __name__=='__main__':unittest.main()
