"""Academic footer and late-demo follow-up: no slide-body or media changes."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent


def key(slide):
    return slide['new_slide_key'] or slide['old_slide']


class EnpirePolishTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = json.loads((ROOT / '.build/v0_19_polish_baseline/deck.json').read_text())
        raw = (ROOT / 'output/Agents_for_Robotics_Self_Contained.html').read_text()
        cls.after = json.loads(re.search(
            r'<script type="application/json" id="deck-data">(.*?)</script>', raw, re.S)[1])

    def test_order_and_academic_citations(self):
        slides = self.after['slides']
        self.assertEqual([key(s) for s in slides[23:35]], [
            15, 'enpire_env', 'enpire_resets', 'enpire_methods', 'idea_tree',
            'enpire_results', 'enpire_fleet_page', 18, 'enpire_robocasa',
            'enpire_demos', 'enpire_limits', 'rsi_summary'])
        reference = ('W. Xiao et al., “ENPIRE: Agentic Robot Policy Self-Improvement '
                     'in the Real World,” arXiv:2606.19980, 2026. ')
        suffixes = [
            'Adapted schematic.', 'Fig. 2.',
            'Project website, Auto Evaluation. Adapted schematic.',
            'Project website, Auto Reset, Cases 1–4.',
            'Secs. 2, 3.1–3.2; App. B.5. Images: project website.',
            'Fig. 12; App. B.6.',
            'Fig. 3; project website, interactive plot data.',
            'Sec. 3.3; Fig. 3. Video: project website.',
            'Fig. 7; project website, interactive plot data.',
            'Fig. 6; App. D.2.',
            'Videos: project website, Learned Policy.',
            'Project website, Limitations.',
            'Sec. 3.4; App. B.1. RSI discussion: this talk.',
        ]
        self.assertEqual([s['footer'] for s in slides[22:35]],
                         [reference + suffix for suffix in suffixes])

    def test_only_requested_content_changes(self):
        before = {key(s): s for s in self.before['slides']}
        self.assertEqual(set(before) | {'enpire_limits'}, {key(s) for s in self.after['slides']})
        for slide in self.after['slides']:
            if key(slide) == 'enpire_limits':
                continue  # Exact split scope is checked in test_v020.py.
            original = before[key(slide)]
            expected = dict(original)
            allowed = ['number', 'startMinutes']
            if 23 <= slide['number'] <= 35:
                allowed.append('footer')
            if key(slide) in ['enpire_demos', 'enpire_robocasa']:
                allowed.extend(['script', 'notesHtml'])
            if key(slide) == 18:
                # The later P31 deletion is checked exactly by test_p31_cleanup.py.
                allowed.extend(['html', 'script', 'notesHtml'])
            if key(slide) == 'end':
                # New closing scope is checked exactly in test_takeaways_v022.py.
                allowed.extend(['html', 'script', 'notesHtml', 'footer'])
            if key(slide) == 'rsi_summary':
                allowed.extend(['title', 'html', 'script', 'notesHtml'])
            if key(slide) == 'thanks':
                expected['html'] = expected['html'].replace('>Thank you</div>', '>Thanks for listening!</div>')
            expected.update({name: slide[name] for name in allowed})
            self.assertEqual(expected, slide, key(slide))
        demos = self.after['slides'][32]['script']
        self.assertNotIn('先看 ENPIRE 最后得到了什么', demos)
        self.assertNotIn('再回头解释', demos)
        self.assertIn('看过系统、策略改进机制和定量结果以后', demos)

    def test_all_media_unchanged(self):
        before = {m['name']: m for m in self.before['media']}
        after = {m['name']: m for m in self.after['media']}
        self.assertEqual(set(before), set(after))
        for name, media in after.items():
            self.assertEqual(before[name] | {'slide': media['slide']}, media, name)
        self.assertEqual(self.before['asset_keys'], sorted(set(self.after['assets']) - {r['sha256'] for r in json.loads((ROOT / '.build/assets/v0_22/manifest.json').read_text())['captures']}))
        self.assertEqual({m['name'] for m in after.values() if m['slide'] == 33},
                         {'enpire_pin', 'enpire_gpu', 'enpire_tie', 'enpire_cut'})


if __name__ == '__main__':
    unittest.main()
