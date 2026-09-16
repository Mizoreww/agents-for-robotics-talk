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

    def test_chapter_is_demo_only(self):
        deck = load_deck(ROOT / 'output/Agents_for_Robotics_Self_Contained.html')
        self.assertEqual(len(deck['slides']), 37)
        self.assertEqual([s['new_slide_key'] or s['old_slide'] for s in deck['slides'][17:22]],
                         ['world', 'data_scenes', 'data_hands', 'data_motion', 'world_summary'])
        self.assertEqual({m['name'] for m in deck['media'] if 18 <= m['slide'] <= 22},
                         {'office_newton', 'kitchen', 'hand', 'rope_hand','astra_real2sim', 'dexgpt'})
        self.assertFalse(any('S13' in s['ids'] for s in deck['slides']))

    def test_pair_media_and_source_boundaries(self):
        deck = load_deck(ROOT / 'output/Agents_for_Robotics_Self_Contained.html')
        self.assertEqual({n: {m['name'] for m in deck['media'] if m['slide'] == n}
                          for n in [19, 20, 21]},
                         {19: {'office_newton', 'kitchen'}, 20: {'hand', 'rope_hand'},
                          21: {'astra_real2sim', 'dexgpt'}})
        self.assertNotIn('Source image', deck['slides'][18]['html'])
        self.assertIn('adding simulation', deck['slides'][18]['script'])
        self.assertIn('可编辑的3D场景资产', deck['slides'][18]['script'])
        self.assertNotIn('这两个案例都把现实空间变成 simulator', deck['slides'][18]['script'])
        self.assertIn('Not a validated physical hand', deck['slides'][19]['html'])
        self.assertIn('illustrative cable deformation', deck['slides'][19]['html'])
        self.assertIn('physical validation not met', deck['slides'][20]['html'])
        before = load_deck(ROOT / '.build/revision_0_17_baseline/output/Agents_for_Robotics_Self_Contained.html')
        self.assertEqual({m['name']: m['sha256'] for m in before['media'] if m['slide']<=24},
                         {m['name']: m['sha256'] for m in deck['media'] if m['slide']<=22 and m['name'] not in {'kitchen','cube','claw'}})


if __name__ == '__main__':
    unittest.main()
