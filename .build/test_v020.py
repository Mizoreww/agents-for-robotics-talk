"""Constrain P31 vertical-only centering, the chapter split and closing copy."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent


def key(slide):
    return slide['new_slide_key'] or slide['old_slide']


class V020Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = json.loads((ROOT / '.build/v0_20_baseline/deck.json').read_text())
        raw = (ROOT / 'output/Agents_for_Robotics_Self_Contained.html').read_text()
        cls.after = json.loads(re.search(
            r'<script type="application/json" id="deck-data">(.*?)</script>', raw, re.S)[1])

    def test_exact_unchanged_scope(self):
        old = {key(s): s for s in self.before['slides']}
        self.assertEqual(len(self.after['slides']), 37)
        self.assertEqual(set(old) | {'enpire_limits'}, {key(s) for s in self.after['slides']})
        for slide in self.after['slides']:
            identity = key(slide)
            if identity == 'enpire_limits':
                continue
            expected = dict(old[identity])
            expected.update(number=slide['number'], startMinutes=slide['startMinutes'])
            if identity == 18:
                anchor = 'left:126px;top:135px;width:1027px;height:320px;'
                self.assertEqual(expected['html'].count(anchor), 1)
                expected['html'] = expected['html'].replace(anchor, anchor.replace('135', '238'))
            if identity == 'thanks':
                expected['html'] = expected['html'].replace('>Thank you</div>', '>Thanks for listening!</div>')
            if identity == 'end':
                # P36 is independently constrained by test_takeaways_v022.py.
                for field in ('html', 'script', 'notesHtml', 'footer'):
                    expected[field] = slide[field]
            if identity == 'rsi_summary':
                for field in ('title', 'html', 'script', 'notesHtml'):
                    expected[field] = slide[field]
            self.assertEqual(expected, slide, identity)

    def test_split_content_and_timing(self):
        slides = self.after['slides']
        self.assertEqual([key(s) for s in slides[33:]],
                         ['enpire_limits', 'rsi_summary', 'end', 'thanks'])
        limits, recursive = slides[33:35]
        self.assertEqual(limits['title'], 'ENPIRE: Limitations')
        self.assertEqual(recursive['title'], 'Toward Recursive Self-Improvement')
        for phrase in ['Idle robots &amp; compute', 'More agents, more tokens']:
            self.assertIn(phrase, limits['html'])
            self.assertNotIn(phrase, recursive['html'])
        for phrase in ['Retained recipes / memory', 'Better future research?', 'Physical experiments']:
            self.assertNotIn(phrase, limits['html'])
            self.assertIn(phrase, recursive['html'])
        self.assertIn('Markdown summary', recursive['script'])
        self.assertIn('held-out tasks', recursive['script'])
        self.assertEqual(sum(s['minutes'] for s in slides), 60)

    def test_media_and_closing(self):
        self.assertEqual(self.before['media'], self.after['media'])
        self.assertEqual(self.before['asset_keys'], sorted(set(self.after['assets']) - {r['sha256'] for r in json.loads((ROOT / '.build/assets/v0_22/manifest.json').read_text())['captures']}))
        self.assertIn('Thanks for listening!', self.after['slides'][36]['html'])
        self.assertNotIn('>Thank you</div>', self.after['slides'][36]['html'])


if __name__ == '__main__':
    unittest.main()
