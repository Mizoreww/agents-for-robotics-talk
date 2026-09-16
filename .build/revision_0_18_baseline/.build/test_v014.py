"""Focused source identity and explicitly labelled interface highlighting checks."""
from pathlib import Path
import json
import shutil
import tempfile
import unittest

from code_video_v014 import verify_code_video
from table_emphasis import best_cells, row_maxima

ROOT = Path(__file__).resolve().parent.parent


class RevisionTests(unittest.TestCase):
    def test_code_replay_authority(self):
        self.assertEqual(verify_code_video(ROOT)['source']['episode'], 'ep00.mp4')

    def test_modified_video_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            mirror = Path(directory)
            manifest = 'research/code_video_v0_14_sources.json'
            pins = json.loads((ROOT / manifest).read_text())
            for relative in [manifest, *pins['sha256']]:
                target = mirror / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
            video = mirror / '.build/assets/v0_13_code/asim_square_code_proprio_ep00.mp4'
            video.write_bytes(video.read_bytes() + b'drift')
            with self.assertRaises(ValueError):
                verify_code_video(mirror)

    def test_waypoint_column_is_highlight_not_universal_winner(self):
        rows = json.loads((ROOT / 'research/results_v0_9.json').read_text())['asim']
        nonprivileged_best = best_cells(rows, row_maxima(rows, range(3, 7)))
        self.assertIn((2, 5), nonprivileged_best)  # Square waypoint
        self.assertIn((1, 3), nonprivileged_best)  # Can delta
        self.assertNotIn((1, 5), nonprivileged_best)
        marked = best_cells(rows, row_maxima(rows, range(3, 8))) | {(r, 5) for r in range(3)}
        self.assertEqual(marked, {(0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 7), (2, 7), (1, 5), (2, 5)})


if __name__ == '__main__':
    unittest.main()
