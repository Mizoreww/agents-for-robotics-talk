"""Fail-closed source identity tests; all output writes are intercepted in memory."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / '.build/derive_results_v09.py'
PINNED = json.loads((ROOT / 'research/results_v0_9_sources.json').read_text())['sources']


class FrozenSources(unittest.TestCase):
    def run_derivation(self):
        with contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(str(SCRIPT), run_name='__main__')

    def test_verified_sources_reproduce_authority(self):
        expected = json.loads((ROOT / 'research/results_v0_9.json').read_text())
        with patch.object(Path, 'write_text') as output:
            self.run_derivation()
        output.assert_called_once()
        self.assertEqual(json.loads(output.call_args.args[0]), expected)

    def test_every_source_rejects_byte_drift_before_publication(self):
        original_read = Path.read_bytes
        for relative in PINNED:
            target = ROOT / relative
            def mutated_read(file):
                raw = original_read(file)
                return raw + b'\n' if file == target else raw
            with self.subTest(source=relative), patch.object(Path, 'read_bytes', mutated_read):
                with patch.object(Path, 'write_text') as output:
                    with self.assertRaisesRegex(ValueError, 'Frozen source identity mismatch'):
                        self.run_derivation()
                    output.assert_not_called()

    def test_changed_hi_robot_average_is_not_reauthorized(self):
        original_read = Path.read_bytes
        target = ROOT / 'research/sources/control_results_20260914/background/hirobot_chart_values.json'
        def changed_average(file):
            raw = original_read(file)
            if file == target:
                data = json.loads(raw)
                data['values']['Average']['Instruction Accuracy']['Hi Robot'] = 77
                return json.dumps(data).encode()
            return raw
        with patch.object(Path, 'read_bytes', changed_average), patch.object(Path, 'write_text') as output:
            with self.assertRaisesRegex(ValueError, 'Frozen source identity mismatch'):
                self.run_derivation()
            output.assert_not_called()


if __name__ == '__main__':
    unittest.main()
