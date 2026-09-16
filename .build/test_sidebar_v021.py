"""UI contract and unchanged content against the delivered v0.20 snapshot."""
import hashlib
import json
import re
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent


class SidebarContract(unittest.TestCase):
    def test_accessible_controls(self):
        shell = (B / 'standalone_shell.html').read_text()
        self.assertIn('aria-controls="notes"', shell)
        self.assertIn('id="notes-close"', shell)
        self.assertIn('id="notes-scroll"', shell)

    def test_media_and_player_unchanged(self):
        html = (B.parent / 'output/Agents_for_Robotics_Self_Contained.html').read_text()
        sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
        identity = json.loads((B / 'v0_21_baseline/identity.json').read_text())
        payloads = re.findall(r'<script[^>]*id="(video-[^"]+)"[^>]*>(.*?)</script>', html, re.S)
        self.assertEqual({k: sha(v) for k, v in payloads}, identity['video_payloads'])
        self.assertEqual(len(payloads), 28)
        # Subsequent P35/P36 content changes have their own exact-scope regression.
        for name in ['standalone_shell.html', 'standalone_player.css', 'standalone_player.js']:
            self.assertEqual((B / name).read_bytes(), (B / 'v0_22_baseline' / name).read_bytes())


if __name__ == '__main__':
    unittest.main()
