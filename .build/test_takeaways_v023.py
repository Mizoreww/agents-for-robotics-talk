"""P36-only native SVG redesign: content, size consistency, and unchanged player."""
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

B = Path(__file__).resolve().parent
NS = {'s': 'http://www.w3.org/2000/svg'}


class SvgTakeawaysTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = json.loads((B / 'v0_23_baseline/deck.json').read_text())
        raw = (B.parent / 'output/Agents_for_Robotics_Self_Contained.html').read_text()
        cls.after = json.loads(re.search(r'<script type="application/json" id="deck-data">(.*?)</script>', raw, re.S)[1])

    def test_exact_scope(self):
        self.assertEqual(len(self.after['slides']), 37)
        for n, (old, new) in enumerate(zip(self.before['slides'], self.after['slides']), 1):
            expected = dict(old)
            if n == 36:
                for field in ['html', 'script', 'notesHtml', 'footer']:
                    expected[field] = new[field]
            self.assertEqual(expected, new, n)
        self.assertEqual(self.before['media'], self.after['media'])
        thumbnails = {c['sha256'] for c in json.loads((B / 'assets/v0_22/manifest.json').read_text())['captures']}
        self.assertEqual(set(self.after['assets']), set(self.before['asset_keys']) - thumbnails)
        for name in ['standalone_player.js', 'standalone_player.css', 'standalone_shell.html']:
            self.assertEqual((B / name).read_bytes(), (B / 'v0_23_baseline' / name).read_bytes())

    def test_svg_and_uniform_font(self):
        markup = (B / 'takeaways_v023.svg').read_text().strip()
        self.assertIn(markup, self.after['slides'][35]['html'])
        self.assertNotIn('Thumbnail of', self.after['slides'][35]['html'])
        root = ET.fromstring(markup)
        self.assertFalse(root.findall('.//s:image', NS))
        self.assertFalse(root.findall('.//s:foreignObject', NS))
        self.assertFalse(root.findall('.//s:script', NS))
        # Exactly one inherited body size; no local overrides hide inconsistencies.
        self.assertEqual([e.attrib['font-size'] for e in root.iter() if 'font-size' in e.attrib], ['24'])
        labels = [e.text for e in root.findall('.//s:text', NS)]
        for label in ['Agent', 'Control', 'Data', 'Improvement', 'System 2', 'Primitives',
                      'Semantic / spatial', 'Fast / contact-rich', 'Latency?',
                      'Better interface?', 'Sim2Real?', 'Efficiency?']:
            self.assertIn(label, labels)

    def test_narration_and_deletions(self):
        slide = self.after['slides'][35]
        self.assertIn('Agent', slide['script'])
        self.assertNotIn('点击放大', slide['script'])
        self.assertNotIn('click thumbnails', slide['footer'])
        self.assertNotIn('Different artifacts', slide['html'])
        self.assertNotIn('Open test: held-out tasks', self.after['slides'][34]['html'])


if __name__ == '__main__':
    unittest.main()
