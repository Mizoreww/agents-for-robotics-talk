"""Fail-closed source tests and regression coverage for the current demo-only chapter."""
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

from data_demos_v015 import verify_data_demos, verify_data_extra, verify_kitchen_video

ROOT = Path(__file__).resolve().parent.parent


def load_deck(file):
    return json.loads(re.search(r'<script type="application/json" id="deck-data">(.*?)</script>', file.read_text(), re.S)[1])


class DataDemoTests(unittest.TestCase):
    def test_source_identity(self):
        self.assertEqual(verify_data_extra(ROOT)['awesome_commit'], '61baafd5fc94ae2db32da8da57704310033a6210')

    def test_kitchen_source_identity(self):
        self.assertEqual(verify_kitchen_video(ROOT)['source']['x_post_id'], '2098460193319186578')

    def test_kitchen_drift_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            mirror = Path(directory)
            manifest = 'research/kitchen_v0_17_sources.json'
            pins = json.loads((ROOT / manifest).read_text())
            for relative in [manifest, *pins['sha256']]:
                target = mirror / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
            video = mirror / '.build/clips/kitchen.mp4'
            video.write_bytes(video.read_bytes() + b'drift')
            with self.assertRaises(ValueError):
                verify_kitchen_video(mirror)

    def test_modified_source_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            mirror = Path(directory)
            manifest = 'research/data_extra_v0_16_sources.json'
            pins = json.loads((ROOT / manifest).read_text())
            for relative in [manifest, *pins['sha256']]:
                target = mirror / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
            video = mirror / '.build/clips/rope_hand.mp4'
            video.write_bytes(video.read_bytes() + b'drift')
            with self.assertRaises(ValueError):
                verify_data_extra(mirror)

    def test_non_data_pages_unchanged(self):
        before = load_deck(ROOT / '.build/revision_0_17_baseline/output/Agents_for_Robotics_Self_Contained.html')
        after = load_deck(ROOT / 'output/Agents_for_Robotics_Self_Contained.html')
        pairs = list(zip(before['slides'][:16], after['slides'][:16]))
        pairs += list(zip(before['slides'][24:], after['slides'][21:]))
        self.assertEqual(len(pairs), 27)
        for old, new in pairs:
            self.assertEqual(old['html'], new['html'], new['title'])
            self.assertEqual(old['title'], new['title'])
            if new['number'] != 3:
                self.assertEqual(old['script'], new['script'], new['title'])
            else:
                self.assertIn('Data 只看 Awesome-Astra 收录的六个 demo', new['script'])

    def test_chapter_is_demo_only(self):
        deck = load_deck(ROOT / 'output/Agents_for_Robotics_Self_Contained.html')
        self.assertEqual(len(deck['slides']), 32)
        self.assertEqual([s['new_slide_key'] or s['old_slide'] for s in deck['slides'][16:21]],
                         ['world', 'data_scenes', 'data_hands', 'data_motion', 'world_summary'])
        self.assertEqual({m['name'] for m in deck['media'] if 17 <= m['slide'] <= 21},
                         {'office_newton', 'kitchen', 'hand', 'rope_hand','astra_real2sim', 'dexgpt'})
        self.assertFalse(any('S13' in s['ids'] for s in deck['slides']))

    def test_pair_media_and_source_boundaries(self):
        deck = load_deck(ROOT / 'output/Agents_for_Robotics_Self_Contained.html')
        self.assertEqual({n: {m['name'] for m in deck['media'] if m['slide'] == n}
                          for n in [18, 19, 20]},
                         {18: {'office_newton', 'kitchen'}, 19: {'hand', 'rope_hand'},
                          20: {'astra_real2sim', 'dexgpt'}})
        self.assertNotIn('Source image', deck['slides'][17]['html'])
        self.assertIn('adding simulation', deck['slides'][17]['script'])
        self.assertIn('可编辑的3D场景资产', deck['slides'][17]['script'])
        self.assertNotIn('这两个案例都把现实空间变成 simulator', deck['slides'][17]['script'])
        self.assertIn('Not a validated physical hand', deck['slides'][18]['html'])
        self.assertIn('illustrative cable deformation', deck['slides'][18]['html'])
        self.assertIn('physical validation not met', deck['slides'][19]['html'])
        before = load_deck(ROOT / '.build/revision_0_17_baseline/output/Agents_for_Robotics_Self_Contained.html')
        self.assertEqual({m['name']: m['sha256'] for m in before['media']},
                         {m['name']: m['sha256'] for m in deck['media'] if m['name'] != 'kitchen'})


if __name__ == '__main__':
    unittest.main()
