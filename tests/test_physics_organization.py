import unittest
from pathlib import Path

class OrganizationTests(unittest.TestCase):
    def test_taxonomy_file_exists(self):
        root=Path(__file__).resolve().parents[1]
        self.assertTrue((root/'taxonomy/physics_taxonomy.json').is_file())

if __name__=='__main__':
    unittest.main()
