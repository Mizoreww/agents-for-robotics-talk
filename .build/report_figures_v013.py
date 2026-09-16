"""Load hash-pinned original report captures and verify their quantitative lineage."""
from pathlib import Path
import hashlib
import json

CAPTURES = ['panel-score-ranking.png', 'panel-sr-ranking.png',
            'robolab-success-ranking.png', 'task-score-table-complete.png']


def load_report_figures(root):
    root = Path(root)
    manifest = json.loads((root / 'research/report_figures_v0_13_sources.json').read_text())
    for relative, digest in manifest['sha256'].items():
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != digest:
            raise ValueError(f'Report capture identity mismatch: {relative}')
    directory = root / '.build/assets/v0_13'
    payloads = json.loads((directory / 'source_query_rows.json').read_text())
    assert len({p['contextVersion'] for p in payloads.values()}) == 1
    assert all(not p['hasMore'] and len(p['rows']) == p['totalRows'] for p in payloads.values())
    models = {r['name']: r for r in payloads['models']['rows']}
    tasks = payloads['tasks']['rows']
    lab = {r['id']: r for r in payloads['robolab_models']['rows']}
    legacy = json.loads((root / 'research/results_v0_9.json').read_text())
    assert models['gpt']['sr'] == 26 and models['mix']['sr'] == 48
    assert abs(models['gpt']['score'] - 37.8125) < 1e-6
    assert abs(models['mix']['score'] - 62.6) < 1e-6
    assert models['gpt']['score_n'] == 48 and models['mix']['score_n'] == 50
    assert sum(t['gpt_score_n'] for t in tasks) == 48
    assert {k: v['successes'] for k, v in lab.items()} == {
        'pure_astra': 49, 'astra_pi05': 46, 'pi05_only': 18,
        'cosmos_nano_policy': 18, 'dreamzero': 17}
    assert all(r['episodes'] == 50 for r in lab.values())
    assert len(tasks) == len(legacy['robodojo']['rows']) == 10
    for current, previous in zip(tasks, legacy['robodojo']['rows']):
        assert current['id'] == previous['task']
        assert current['rates']['gpt'] == previous['gpt'] * 20
        assert current['rates']['mix'] == previous['mix'] * 20
    dom = json.loads((directory / 'heatmap_dom.json').read_text())
    audit = json.loads((directory / 'heatmap_render_audit.json').read_text())
    cells = [e['text'] for e in dom['styles'] if e['text'] is not None]
    assert cells == audit['cells'] and audit['rows'] == 12 and len(cells) == 96
    columns = ['DM0.5', 'GalaxeaVLA (G0.5)', 'Xiaomi-Robotics-1', 'OpenWAM-α', 'Pi-05', 'mix', 'gpt']
    for i, task in enumerate(tasks, 1):
        assert [float(c) for c in cells[i*8+1:i*8+8]] == [round(task['scores'][c], 2) for c in columns]
    assert [float(c) for c in cells[89:96]] == [round(models[c]['score'], 2) for c in columns]
    return {name: directory / name for name in CAPTURES}
