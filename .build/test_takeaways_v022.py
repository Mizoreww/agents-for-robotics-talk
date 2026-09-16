"""Exact P35 deletion, P36 recap, thumbnail identity and preserved player/media."""
import hashlib
import json
from pathlib import Path
import re
import unittest

B = Path(__file__).resolve().parent


class TakeawaysTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = json.loads((B / 'v0_22_baseline/deck.json').read_text())
        raw = (B.parent / 'output/Agents_for_Robotics_Self_Contained.html').read_text()
        cls.after = json.loads(re.search(r'<script type="application/json" id="deck-data">(.*?)</script>', raw, re.S)[1])

    def test_exact_slide_scope(self):
        self.assertEqual(len(self.after['slides']), 37)
        for n, (old, new) in enumerate(zip(self.before['slides'], self.after['slides']), 1):
            expected = dict(old)
            if n == 35:
                expected['html'], count = re.subn(
                    r'<div class="text"[^>]*>Open test: held-out tasks, matched budgets, no regression</div>',
                    '', expected['html'])
                self.assertEqual(count, 1)
            if n == 36:
                for field in ['html', 'script', 'notesHtml', 'footer']:
                    expected[field] = new[field]
            self.assertEqual(expected, new, n)

    def test_questions_preserved(self):
        slide = self.after['slides'][35]
        for label in ['Control', 'Data', 'Improvement', 'Latency?', 'Better interface?', 'Sim2Real?', 'Efficiency?', 'Open problems']:
            self.assertIn(label, slide['html'])
        for deleted in ['Different artifacts', 'Different tests', 'Re-test the division', 'Reliable execution', 'Held-out gain + cost']:
            self.assertNotIn(deleted, slide['html'] + slide['footer'])
        self.assertLess(len(' '.join(re.findall(r'<text\b[^>]*>(.*?)</text>', slide['html'])).split()), 50)
        # Raster thumbnails are superseded by test_takeaways_v023.py's exact SVG checks.
        self.assertIn('takeaways-diagram', slide['html'])
        for term in ['Latency', 'interface', 'Sim2Real', 'Efficiency']:
            self.assertIn(term, slide['script'])

    def test_media_and_archived_thumbnail_identity(self):
        self.assertEqual(self.before['media'], self.after['media'])
        manifest = json.loads((B / 'assets/v0_22/manifest.json').read_text())
        added = set()
        for capture in manifest['captures']:
            raw = (B / 'assets/v0_22' / capture['file']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), capture['sha256'])
            source = self.after['slides'][capture['slide'] - 1]['html'].encode()
            self.assertEqual(hashlib.sha256(source).hexdigest(), capture['source_html_sha256'])
            added.add(capture['sha256'])
        self.assertEqual(set(self.after['assets']), set(self.before['asset_keys']))
        self.assertTrue(added.isdisjoint(self.after['assets']))
        self.assertEqual(len(added), 2)

    def test_player_unchanged(self):
        for name in ['standalone_shell.html', 'standalone_player.css', 'standalone_player.js']:
            self.assertEqual((B / name).read_bytes(), (B / 'v0_22_baseline' / name).read_bytes())


if __name__ == '__main__':
    unittest.main()
