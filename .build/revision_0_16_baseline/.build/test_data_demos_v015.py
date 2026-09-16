"""Fail-closed source tests and regression coverage for the demo-only chapter."""
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

from data_demos_v015 import verify_data_demos

ROOT = Path(__file__).resolve().parent.parent


def load_deck(file):
    return json.loads(re.search(r'<script type="application/json" id="deck-data">(.*?)</script>', file.read_text(), re.S)[1])


class DataDemoTests(unittest.TestCase):
    def test_source_identity(self):
        self.assertEqual(verify_data_demos(ROOT)['awesome_commit'], '61baafd5fc94ae2db32da8da57704310033a6210')

    def test_modified_source_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            mirror = Path(directory)
            manifest = 'research/data_demos_v0_15_sources.json'
            pins = json.loads((ROOT / manifest).read_text())
            for relative in [manifest, *pins['sha256']]:
                target = mirror / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
            video = mirror / '.build/clips/dexgpt.mp4'
            video.write_bytes(video.read_bytes() + b'drift')
            with self.assertRaises(ValueError):
                verify_data_demos(mirror)

    def test_non_data_pages_unchanged(self):
        before = load_deck(ROOT / '.build/revision_0_15_baseline/output/Agents_for_Robotics_Self_Contained.html')
        after = load_deck(ROOT / 'output/Agents_for_Robotics_Self_Contained.html')
        pairs = list(zip(before['slides'][:16], after['slides'][:16]))
        pairs += list(zip(before['slides'][24:], after['slides'][22:]))
        self.assertEqual(len(pairs), 27)
        for old, new in pairs:
            self.assertEqual(old['html'], new['html'], new['title'])
            self.assertEqual(old['title'], new['title'])
            if new['number'] != 3:
                self.assertEqual(old['script'], new['script'], new['title'])
            else:
                self.assertIn('Data 只看 Awesome-Astra 收录的四个 demo', new['script'])

    def test_chapter_is_demo_only(self):
        deck = load_deck(ROOT / 'output/Agents_for_Robotics_Self_Contained.html')
        self.assertEqual([s['new_slide_key'] or s['old_slide'] for s in deck['slides'][16:22]],
                         ['world', 'data_scene', 19, 'data_replay', 'data_rollout', 'world_summary'])
        self.assertEqual({m['name'] for m in deck['media'] if 17 <= m['slide'] <= 22},
                         {'office_newton', 'hand', 'astra_real2sim', 'dexgpt'})
        self.assertFalse(any('S13' in s['ids'] for s in deck['slides']))


if __name__ == '__main__':
    unittest.main()
