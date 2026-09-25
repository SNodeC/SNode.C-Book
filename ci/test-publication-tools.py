import importlib.util
from pathlib import Path
import unittest
spec = importlib.util.spec_from_file_location('tools', Path(__file__).with_name('check-publication-tools.py'))
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)

class Versions(unittest.TestCase):
    def test_surrounding_version_text_is_irrelevant(self):
        self.assertEqual(tools.versions('pandoc 3.9.0.2\nFeatures: +lua',
            'pandoc-crossref v0.3.24 git commit UNKNOWN built with Pandoc v3.9.0.2, and extra data'), '3.9.0.2')
    def test_mismatch_fails(self):
        with self.assertRaisesRegex(ValueError, 'mismatch'):
            tools.versions('pandoc 3.10.1', 'crossref built with Pandoc v3.9.0.2')
    def test_missing_build_version_fails(self):
        with self.assertRaisesRegex(ValueError, 'Cannot identify'):
            tools.versions('pandoc 3.9.0.2', 'pandoc-crossref 3.9.0.2')

if __name__ == '__main__': unittest.main()
