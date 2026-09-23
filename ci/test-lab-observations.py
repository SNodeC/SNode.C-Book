#!/usr/bin/env python3
"""Async output is evidence only once its complete record has been delivered."""
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

EXERCISES = Path(__file__).resolve().parents[1] / 'companion/exercises'
sys.path.insert(0, str(EXERCISES))
import lab_support

RECOVERY = runpy.run_path(str(EXERCISES / 'ch15/recovery.py'))


class AsyncObservations(unittest.TestCase):
    def test_waits_for_complete_matching_record(self):
        path = Mock()
        path.read_text.side_effect = ['old\n', 'old\nexpected', 'old\nexpected\n']
        with patch.object(lab_support.time, 'sleep'):
            lab_support.wait_log(path, 'expected')
        self.assertEqual(path.read_text.call_count, 3)

    def test_missing_record_still_fails(self):
        path = Mock()
        path.read_text.return_value = 'unrelated\n'
        with patch.object(lab_support.time, 'monotonic', side_effect=[0, 1, 6]), \
             patch.object(lab_support.time, 'sleep'):
            with self.assertRaisesRegex(AssertionError, 'Missing'):
                lab_support.wait_log(path, 'expected')

    def test_live_json_ignores_partial_tail_but_rejects_complete_bad_record(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'records.jsonl'
            path.write_text('{"message":"first"}\n{"message":')
            self.assertEqual(RECOVERY['records'](path), [{'message': 'first'}])
            with path.open('a') as output:
                output.write('"second"}\n')
            self.assertEqual(RECOVERY['records'](path),
                             [{'message': 'first'}, {'message': 'second'}])
            path.write_text('{broken}\n')
            with self.assertRaises(json.JSONDecodeError):
                RECOVERY['records'](path)


if __name__ == '__main__':
    unittest.main()
