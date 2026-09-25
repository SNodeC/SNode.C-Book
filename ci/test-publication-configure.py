#!/usr/bin/env python3
"""Exercise CMake tool selection without network access or a TeX installation."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublicationConfigure(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.build = self.root/'build'
        self.pandoc = self.root/'pandoc/bin/pandoc'
        self.crossref = self.root/'crossref/pandoc-crossref'
        self.system = self.root/'system/pandoc'
        for path, version in (
            (self.pandoc, 'pandoc 3.9.0.2'),
            (self.crossref, 'pandoc-crossref built with Pandoc v3.9.0.2'),
            (self.system, 'pandoc 3.11'),
        ):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('#!/bin/sh\necho "'+version+'"\n')
            path.chmod(0o755)

    def configure(self, *options):
        return subprocess.run([
            'cmake', '-S', str(ROOT), '-B', str(self.build),
            '-DFETCHCONTENT_SOURCE_DIR_BOOK_PANDOC='+str(self.pandoc.parent.parent),
            '-DFETCHCONTENT_SOURCE_DIR_BOOK_CROSSREF='+str(self.crossref.parent),
            *options,
        ], env={**os.environ, 'PATH': str(self.system.parent)+os.pathsep+os.environ['PATH']},
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def test_fresh_defaults_ignore_incompatible_path_and_reconfigure_offline(self):
        result = self.configure()
        self.assertEqual(result.returncode, 0, result.stdout)
        cache = (self.build/'CMakeCache.txt').read_text()
        self.assertIn('PANDOC:FILEPATH='+str(self.pandoc), cache)
        self.assertIn('PANDOC_CROSSREF_FILTER:FILEPATH='+str(self.crossref), cache)
        result = self.configure('-DFETCHCONTENT_FULLY_DISCONNECTED=ON')
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_legacy_bare_defaults_select_managed_pair(self):
        result = self.configure('-DPANDOC=pandoc', '-DPANDOC_CROSSREF_FILTER=pandoc-crossref')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('PANDOC:FILEPATH='+str(self.pandoc), (self.build/'CMakeCache.txt').read_text())

    def test_explicit_executables_are_preserved_and_mismatch_is_rejected(self):
        result = self.configure('-DPANDOC='+str(self.pandoc),
                                '-DPANDOC_CROSSREF_FILTER='+str(self.crossref))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertFalse((self.build/'_deps').exists())
        result = self.configure('-DPANDOC='+str(self.system))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('active Pandoc 3.11, crossref built with Pandoc 3.9.0.2', result.stdout)

    def test_pdfs_disabled_does_not_require_publication_tools(self):
        result = self.configure('-DSNODEC_BOOK_BUILD_PDFS=OFF', '-DPANDOC=/missing',
                                '-DPANDOC_CROSSREF_FILTER=/missing')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertFalse((self.build/'_deps').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
