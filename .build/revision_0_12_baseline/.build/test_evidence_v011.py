"""Fail-closed v0.11 timing/source regressions, without changing disk files."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from evidence_v011 import load_evidence

ROOT = Path(__file__).resolve().parent.parent
PINNED = json.loads((ROOT / 'research/evidence_v0_11_sources.json').read_text())['sources']


class EvidenceV011(unittest.TestCase):
    def test_original_query_counts_and_means(self):
        rows = load_evidence(ROOT)
        self.assertEqual([rows[k]['queries'] for k in ('delta', 'waypoint', 'code')], [414, 241, 76])
        self.assertEqual([round(rows[k]['mean_s'], 2) for k in ('delta', 'waypoint', 'code')], [30.75, 26.08, 41.98])

    def test_every_source_rejects_byte_drift(self):
        original = Path.read_bytes
        for relative in PINNED:
            target = ROOT / relative
            def read(file):
                raw = original(file)
                return raw + b'\n' if file == target else raw
            with self.subTest(source=relative), patch.object(Path, 'read_bytes', read):
                with self.assertRaisesRegex(ValueError, 'source identity changed'):
                    load_evidence(ROOT)

    def check_semantic_mutation(self, mutate, message):
        original = Path.read_text
        def read(file, *args, **kwargs):
            value = original(file, *args, **kwargs)
            if file.name == 'asim_query_times_derived.json':
                data = json.loads(value)
                mutate(data)
                return json.dumps(data)
            return value
        with patch.object(Path, 'read_text', read):
            with self.assertRaisesRegex(ValueError, message):
                load_evidence(ROOT)

    def test_changed_mean_cannot_pass_aggregation(self):
        self.check_semantic_mutation(lambda d: d['summary'][0].update(mean_s=1), 'aggregate')

    def test_duplicate_episode_is_rejected(self):
        self.check_semantic_mutation(lambda d: d['episodes'].__setitem__(0, d['episodes'][1]), 'unique episodes')

    def test_observation_selection_is_rejected(self):
        self.check_semantic_mutation(lambda d: d['episodes'][0].update(state='privileged'), 'selection drift')

    def test_source_identity_is_bound_to_query_records(self):
        self.check_semantic_mutation(lambda d: d.update(source_sha256='0' * 64), 'does not match')


if __name__ == '__main__':
    unittest.main()
