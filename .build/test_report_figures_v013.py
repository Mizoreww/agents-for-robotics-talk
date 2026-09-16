import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from report_figures_v013 import load_report_figures

ROOT = Path(__file__).resolve().parent.parent


class ReportFiguresTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest_file = 'research/report_figures_v0_13_sources.json'
        self.manifest = json.loads((ROOT / self.manifest_file).read_text())
        files = list(self.manifest['sha256']) + [self.manifest_file, 'research/results_v0_9.json']
        for name in files:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)

    def repin_fixture(self, name, data):
        target = self.root / name
        target.write_text(json.dumps(data))
        self.manifest['sha256'][name] = hashlib.sha256(target.read_bytes()).hexdigest()
        (self.root / self.manifest_file).write_text(json.dumps(self.manifest))

    def test_complete_capture(self):
        self.assertEqual(len(load_report_figures(self.root)), 4)

    def test_modified_image_fails_closed(self):
        name = '.build/assets/v0_13/panel-score-ranking.png'
        (self.root / name).write_bytes(b'changed')
        with self.assertRaises(ValueError):
            load_report_figures(self.root)

    def test_mixed_live_versions_rejected(self):
        name = '.build/assets/v0_13/source_query_rows.json'
        data = json.loads((self.root / name).read_text())
        data['models']['contextVersion'] = 'different'
        self.repin_fixture(name, data)
        with self.assertRaises(AssertionError):
            load_report_figures(self.root)

    def test_task_order_cannot_silently_change(self):
        name = '.build/assets/v0_13/source_query_rows.json'
        data = json.loads((self.root / name).read_text())
        data['tasks']['rows'].reverse()
        self.repin_fixture(name, data)
        with self.assertRaises(AssertionError):
            load_report_figures(self.root)

    def test_missing_heatmap_cell_rejected(self):
        name = '.build/assets/v0_13/heatmap_render_audit.json'
        data = json.loads((self.root / name).read_text())
        data['cells'].pop()
        self.repin_fixture(name, data)
        with self.assertRaises(AssertionError):
            load_report_figures(self.root)

    def test_incomplete_query_rejected(self):
        name = '.build/assets/v0_13/source_query_rows.json'
        data = json.loads((self.root / name).read_text())
        data['models']['hasMore'] = True
        self.repin_fixture(name, data)
        with self.assertRaises(AssertionError):
            load_report_figures(self.root)


if __name__ == '__main__':
    unittest.main()
