"""Official-site chapter order, retained content, and reset-source contracts."""
import json
from pathlib import Path
import re
import tempfile
import shutil
import unittest

from enpire_order_v019 import RESET_CLIPS, verify_reset_sources

ROOT = Path(__file__).resolve().parent.parent


def deck(file):
    return json.loads(re.search(r'<script type="application/json" id="deck-data">(.*?)</script>', file.read_text(), re.S)[1])


class OfficialOrderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = deck(ROOT / '.build/revision_0_19_baseline/output/Agents_for_Robotics_Self_Contained.html')
        cls.after = deck(ROOT / 'output/Agents_for_Robotics_Self_Contained.html')

    def test_unchanged_chapters_and_deletions(self):
        self.assertEqual(self.before['slides'][:22], self.after['slides'][:22])
        expected = self.before['slides'][22] | {'footer': self.after['slides'][22]['footer']}
        self.assertEqual(expected, self.after['slides'][22])
        for old, new in zip(self.before['slides'][-2:], self.after['slides'][-2:]):
            if new['new_slide_key'] == 'end':
                continue  # P36 is superseded and constrained by test_takeaways_v022.py.
            for field in ('title', 'html', 'script'):
                expected = old[field]
                if old['new_slide_key'] == 'thanks' and field == 'html':
                    expected = expected.replace('>Thank you</div>', '>Thanks for listening!</div>')
                self.assertEqual(expected, new[field])

    def test_exact_site_order(self):
        self.assertEqual([s['new_slide_key'] or s['old_slide'] for s in self.after['slides'][23:35]],
                         [15, 'enpire_env', 'enpire_resets', 'enpire_methods',
                          'idea_tree', 'enpire_results', 'enpire_fleet_page', 18, 'enpire_robocasa', 'enpire_demos', 'enpire_limits', 'rsi_summary'])
        self.assertIn('Markdown summary', self.after['slides'][34]['script'])
        self.assertIn('Idle robots &amp; compute', self.after['slides'][33]['html'])
        self.assertIn('More agents, more tokens', self.after['slides'][33]['html'])

    def test_all_original_clips_retained(self):
        old = {m['name']: m for m in self.before['media']}
        new = {m['name']: m for m in self.after['media']}
        self.assertEqual(set(new) - set(old), RESET_CLIPS)
        self.assertTrue(set(old) <= set(new))
        for name, clip in old.items():
            for key in ('sha256', 'duration_seconds', 'sourceUrl', 'start_seconds', 'speed_multiplier'):
                self.assertEqual(clip[key], new[name][key], (name, key))
        self.assertEqual({m['name'] for m in new.values() if m['slide'] == 33},
                         {'enpire_pin', 'enpire_gpu', 'enpire_tie', 'enpire_cut'})
        self.assertEqual({m['name'] for m in new.values() if m['slide'] == 26},
                         RESET_CLIPS | {'enpire_reset_full'})

    def test_reset_sources_and_full_sequence(self):
        verify_reset_sources(ROOT)
        clips = json.loads((ROOT / '.build/clip_manifest_v11.json').read_text())
        self.assertEqual(len(clips), 3)
        self.assertTrue(all(c['presentation_speed'] == 8 for c in clips))

    def test_source_drift_rejected(self):
        pins = json.loads((ROOT / 'research/enpire_v0_19_sources.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            mirror = Path(directory)
            for file in ['research/enpire_v0_19_sources.json', *pins['sha256']]:
                target = mirror / file
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / file, target)
            (mirror / '.build/clips/enpire_reset_gpu.mp4').write_bytes(b'corrupt')
            with self.assertRaises(ValueError):
                verify_reset_sources(mirror)


if __name__ == '__main__':
    unittest.main()
