"""Revision-specific evidence and scope gates, independent of slide construction."""
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

from enpire_v018 import NEW_CLIPS, verify_enpire, verify_puzzles

ROOT = Path(__file__).resolve().parent.parent


def deck(file):
    return json.loads(re.search(r'<script type="application/json" id="deck-data">(.*?)</script>', file.read_text(), re.S)[1])


class EnpireTests(unittest.TestCase):
    def test_source_pins(self):
        self.assertEqual(verify_enpire(ROOT)['commit'], '99ee90acf65b5b18957c8382ad580db999528be3')
        self.assertEqual(verify_puzzles(ROOT)['claw_boundary_seconds'], 20.566667)

    def test_media_drift_fails_closed(self):
        for manifest, media, verify in [
            ('research/enpire_v0_18_sources.json', '.build/clips/enpire_pin.mp4', verify_enpire),
            ('research/puzzle_v0_18_sources.json', '.build/clips/claw.mp4', verify_puzzles)]:
            with self.subTest(manifest=manifest), tempfile.TemporaryDirectory() as directory:
                mirror = Path(directory)
                pins = json.loads((ROOT / manifest).read_text())
                for relative in [manifest, *pins['sha256']]:
                    target = mirror / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / relative, target)
                (mirror / media).write_bytes(b'not-the-pinned-video')
                with self.assertRaises(ValueError):
                    verify(mirror)

    def test_baseline_control_data_and_closing_preserved(self):
        before = deck(ROOT / '.build/revision_0_18_baseline/output/Agents_for_Robotics_Self_Contained.html')
        after = deck(ROOT / 'output/Agents_for_Robotics_Self_Contained.html')
        current = after['slides'][:8] + after['slides'][9:22] + after['slides'][-2:]
        original = before['slides'][:21] + before['slides'][-2:]
        self.assertEqual(len(current), len(original))
        for old, new in zip(original, current):
            for field in ('title', 'html', 'script'):
                expected = old[field]
                if old['number'] == 3 and field == 'html':
                    expected = expected.replace('ENPIRE + training and in-context adaptation', 'ENPIRE + reusable research experience')
                if old['number'] == 8 and field == 'script':
                    expected = expected.replace('下一页就固定为同一个 Astra，看不同 action 输出的公开比较。', '下一页先看两个 simulation puzzle，再回到同一 Astra 的不同 action interface 比较。')
                self.assertEqual(expected, new[field], (old['number'], field))
        base_media = {m['name']: m['sha256'] for m in before['media'] if m['slide'] <= 21}
        self.assertEqual(base_media, {m['name']: m['sha256'] for m in after['media'] if m['name'] in base_media})

    def test_chapter_and_rsi_boundaries(self):
        d = deck(ROOT / 'output/Agents_for_Robotics_Self_Contained.html')
        self.assertEqual(len(d['slides']), 36)
        self.assertEqual({m['name'] for m in d['media'] if m['slide'] >= 23}, NEW_CLIPS)
        text = d['scriptMarkdown']
        for term in ['Markdown summary', 'held-out tasks', 'Recursive Self-Improvement', '不是 coding foundation model', 'conditional retries']:
            self.assertIn(term, text)
        self.assertNotIn('Astra: Training and Context', text)
        self.assertEqual(d['slides'][8]['new_slide_key'], 'puzzle_demos')
        self.assertIn('ideal grasps', d['slides'][8]['html'])
        self.assertIn('action interface not disclosed', d['slides'][8]['html'])
        self.assertIn('How can we use it for downstream training?', d['slides'][21]['html'])


if __name__ == '__main__':
    unittest.main()
