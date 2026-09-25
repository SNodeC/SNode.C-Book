#!/usr/bin/env python3
"""Check the live-log record boundary without running a network peer."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('recovery', ROOT/'companion/exercises/ch16/recovery.py')
recovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recovery)


class RecordBoundaryTests(unittest.TestCase):
    def test_partial_record_waits_for_newline(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory)/'client.log'
            for text, expected in [
                ('{"message":"pending', []),
                ('{"message":"ready"}\n{"message":"pending', [{'message': 'ready'}]),
                ('{"message":"ready"}\n{"message":"pending"}', [{'message': 'ready'}]),
                ('{"message":"ready"}\n{"message":"pending"}\n',
                 [{'message': 'ready'}, {'message': 'pending'}]),
            ]:
                with self.subTest(text=text):
                    log.write_text(text)
                    self.assertEqual(recovery.records(log), expected)

    def test_malformed_complete_record_still_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory)/'client.log'
            log.write_text('{bad}\n')
            with self.assertRaises(json.JSONDecodeError):
                recovery.records(log)


if __name__ == '__main__':
    unittest.main(verbosity=2)
