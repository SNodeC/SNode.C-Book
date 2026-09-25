"""Content drift must name modified, added and missing files, independent of a SHA."""
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('alignment', Path(__file__).with_name('check-source-alignment.py'))
alignment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alignment)

class Drift(unittest.TestCase):
    def test_checkout_must_identify_the_edition_tag(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.run(['git', '-C', str(root), '-c', 'user.name=Test',
                                       '-c', 'user.email=test@example.invalid', *args],
                                      check=True, capture_output=True)
            git('init', '-q')
            git('commit', '-q', '--allow-empty', '-m', 'Edition source')
            git('tag', 'Book-1.0')
            self.assertEqual(alignment.checkout_tag(root, 'Book-1.0'), 'Book-1.0')
            git('commit', '-q', '--allow-empty', '-m', 'Later source')
            with self.assertRaises(subprocess.CalledProcessError):
                alignment.checkout_tag(root, 'Book-1.0')

    def test_content_set_and_untracked_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            for name in ('stable', 'changed', 'removed'):
                (root / name).write_text(name)
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            manifest = {'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in root.iterdir() if p.is_file()}}
            self.assertEqual(alignment.content_drift(root, manifest), [])
            (root / 'changed').write_text('different')
            (root / 'removed').unlink()
            (root / 'untracked').write_text('new')
            self.assertEqual(alignment.content_drift(root, manifest), ['changed', 'removed', 'untracked'])

if __name__ == '__main__':
    unittest.main()
