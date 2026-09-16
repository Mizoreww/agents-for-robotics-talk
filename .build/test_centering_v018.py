"""P3/P23 remove requested text and adjust only vertical positions."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent


class TextNodes(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.nodes = []
        self.active = None
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div' and attrs.get('class') == 'text':
            self.active = {'text': '', 'style': attrs['style']}
            self.nodes.append(self.active)

    def handle_data(self, data):
        if self.active is not None:
            self.active['text'] += data

    def handle_endtag(self, tag):
        if tag == 'div':
            self.active = None


class CenteringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = json.loads((ROOT / '.build/v0_18_centering_baseline/deck.json').read_text())
        raw = (ROOT / 'output/Agents_for_Robotics_Self_Contained.html').read_text()
        cls.after = json.loads(re.search(r'<script type="application/json" id="deck-data">(.*?)</script>', raw, re.S)[1])

    def test_subtitle_followup_changes_nothing_else(self):
        previous = json.loads((ROOT / '.build/v0_18_p23_subtitle_before.json').read_text())
        expected, count = re.subn(
            r'<div class="text"[^>]*>Chapter overview · ENPIRE: improve the next policy, not just the next action</div>',
            '', previous['slides'][22]['html'])
        self.assertEqual(count, 1)
        previous['slides'][22]['html'] = expected
        # Approved academic citation follow-up changes only the footer.
        previous['slides'][22]['footer'] = self.after['slides'][22]['footer']
        for i in range(23):
            self.assertEqual(previous['slides'][i], self.after['slides'][i], i + 1)

    def test_only_requested_slides_change(self):
        for a, b in zip(self.before['slides'][:23], self.after['slides'][:23], strict=True):
            if 24 <= a['number'] <= 34:
                continue  # v0.19 explicitly resequences the ENPIRE chapter.
            for key in a:
                if (a['number'] in (3, 23) and key == 'html') or (a['number'] == 23 and key == 'footer'):
                    continue
                self.assertEqual(a[key], b[key], (a['number'], key))
        self.assertEqual([m for m in self.before['media'] if m['slide'] < 23],
                         [m for m in self.after['media'] if m['slide'] < 23])

    def test_exact_requested_text_removed(self):
        removed = {
            3: {'Established experiments explain mechanisms; new demos reopen the boundaries.'},
            23: {'Evidence', 'Policy / code changes that persist into later trials.',
                 'Still open', 'Can real experiments drive reusable improvement?',
                 'Chapter overview · ENPIRE: improve the next policy, not just the next action'},
        }
        for n, drop in removed.items():
            old = TextNodes(self.before['slides'][n - 1]['html']).nodes
            new = TextNodes(self.after['slides'][n - 1]['html']).nodes
            expected = ' '.join(e['text'] for e in old if e['text'] not in drop).split()
            self.assertEqual(expected, ' '.join(e['text'] for e in new).split())
            self.assertTrue(drop.isdisjoint(e['text'] for e in new))

    def test_only_vertical_positions_change(self):
        for n in (3, 23):
            nodes = TextNodes(self.after['slides'][n - 1]['html']).nodes
            original = {node['text']: node for node in TextNodes(self.before['slides'][n - 1]['html']).nodes}
            body = []
            for node in nodes:
                style = dict(part.split(':', 1) for part in node['style'].split(';') if ':' in part)
                old_style = dict(part.split(':', 1) for part in original[node['text']]['style'].split(';') if ':' in part)
                y = float(style['top'].removesuffix('px'))
                for key in old_style:
                    if key != 'top':
                        self.assertEqual(style[key], old_style[key], (n, node['text'], key))
                if float(old_style['top'].removesuffix('px')) < 140:
                    self.assertEqual(style, old_style, (n, 'title or chapter marker moved'))
                if y >= 140:
                    body.append((y, y + float(style['height'].removesuffix('px'))))
            center = (min(y for y, _ in body) + max(y for _, y in body)) / 2
            # P23's subsequent subtitle deletion explicitly preserves all remaining positions.
            self.assertLess(abs(center - (400 if n == 3 else 444)), 15, (n, center))


if __name__ == '__main__':
    unittest.main()
