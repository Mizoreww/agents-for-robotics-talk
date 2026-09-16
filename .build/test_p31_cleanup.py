"""P31 removes only its native table and takeaway band, preserving the plots."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
OLD = '下表来自官网 Figure 7 的精确绘图数据，保留 mean 和 std。'
NEW = '左、中两图来自官网 Figure 7 的精确绘图数据，保留 mean 和 std。'


class P31CleanupTests(unittest.TestCase):
    def test_exact_deletion_and_preservation(self):
        before = json.loads((ROOT / '.build/v0_19_p31_before.json').read_text())
        raw = (ROOT / 'output/Agents_for_Robotics_Self_Contained.html').read_text()
        after = json.loads(re.search(
            r'<script type="application/json" id="deck-data">(.*?)</script>', raw, re.S)[1])
        expected = json.loads(json.dumps(before['slides']))
        removed = []

        def remove_requested(match):
            y = re.search(r'top:([0-9.]+)px;', match[0])
            if y and 467 <= float(y[1]) <= 612:
                removed.append(match[0])
                return ''
            return match[0]

        expected[30]['html'] = re.sub(
            r'<div\b[^>]*>.*?</div>', remove_requested, expected[30]['html'], flags=re.S)
        self.assertEqual(len(removed), 22)  # Table: 20 elements; takeaway band: 2.
        self.assertTrue(any('More parallel experiments' in x for x in removed))
        self.assertTrue(any('Agent–robot pairs' in x for x in removed))
        for name in ('script', 'notesHtml'):
            self.assertEqual(expected[30][name].count(OLD), 1)
            expected[30][name] = expected[30][name].replace(OLD, NEW)
        expected[30]['html'] = expected[30]['html'].replace('left:126px;top:135px;width:1027px;height:320px;', 'left:126px;top:238px;width:1027px;height:320px;')
        self.assertEqual(expected[:33], after['slides'][:33])
        self.assertEqual(before['media'], after['media'])
        self.assertEqual(before['asset_keys'], sorted(set(after['assets']) - {r['sha256'] for r in json.loads((ROOT / '.build/assets/v0_22/manifest.json').read_text())['captures']}))
        # Later chapter split is independently constrained by test_v020.py.
        self.assertEqual(after['slides'][30]['html'].count('class="art original"'), 1)


if __name__ == '__main__':
    unittest.main()
