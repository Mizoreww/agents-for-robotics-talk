"""Build slide-table values from frozen public sources; never scrape at build time."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent
PINNED = json.loads((ROOT / 'research/results_v0_9_sources.json').read_text())['sources']
sources = {}


def read_bytes(relative):
    raw = (ROOT / relative).read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if relative not in PINNED or actual != PINNED[relative]:
        raise ValueError(f'Frozen source identity mismatch: {relative}')
    sources[relative] = actual
    return raw


def read(relative):
    return read_bytes(relative).decode()


def load(relative):
    return json.loads(read(relative))


cases = load('research/sources/anonymous_report_421_public_results__evaluation_cases.json')['cases']
report = load('research/sources/anonymous_report_421_data.json')
tasks = report['queries']['tasks']['rows']
assert len(cases) == 100 and len(tasks) == 10
dojo = []
for task in tasks:
    row = {'task': task['id']}
    pairs = []
    for method in ['gpt', 'mix']:
        selected = [c for c in cases if c['task'] == task['id'] and c['method'] == method]
        assert len(selected) == 5
        assert len({c['case_id'] for c in selected}) == 5
        pairs.append({c['case_id']: c['seeds'] for c in selected})
        row[method] = sum(c['success'] for c in selected)
        assert row[method] * 20 == task['rates'][method]
    assert pairs[0] == pairs[1]
    dojo.append(row)
dojo_totals = {}
for method in ['gpt', 'mix']:
    selected = [c for c in cases if c['method'] == method]
    scored = [c['score'] for c in selected if c['score'] is not None]
    dojo_totals[method] = {'successes': sum(c['success'] for c in selected),
                           'n': len(selected), 'score_n': len(scored),
                           'mean_score': 100 * sum(scored) / len(scored)}
assert [dojo_totals[m]['successes'] for m in ['gpt', 'mix']] == [13, 24]

lab = load('research/sources/control_results_20260914/control/robolab.json')
baselines = load('research/sources/control_results_20260914/control/robolab-baselines.json')
assert lab['episodes_per_task'] == 5 and len(lab['tasks']) == 10
assert baselines['initial_states_paired'] is False
for method in lab['methods']:
    assert sum(r['successes'][method['id']] for r in lab['tasks']) == method['successes']
    assert method['episodes'] == 50
    if method.get('source_kind') == 'historical':
        original = next(m for m in baselines['methods'] if m['source_run'] == method['source_run'])
        for row in original['tasks']:
            assert row['episodes'] == len(row['trials']) == 5
            assert row['successes'] == sum(t['success'] for t in row['trials'])
            assert row['successes'] == next(t for t in lab['tasks'] if t['task'] == row['task'])['successes'][method['id']]

asim = load('research/sources/control_action_interfaces_20260914/asim_tables.json')[0]
assert len(asim) == 4
asim_rows = [[row[0]] + [re.match(r'(\d+/\d+)', cell)[1] for cell in row[1:]] for row in asim[1:]]

# The source supplies this results table as plain text; require its exact table schema.
robocurve = read('research/sources/control_action_interfaces_20260914/robocurve.txt')
block = robocurve.split('\nResults\n', 1)[1].split('\nAll runs\n', 1)[0]
cells = [line.strip() for line in block.splitlines() if line.strip()]
assert cells[:8] == ['Task', 'Model', 'Mean stage', 'Completions', 'Rate', 'Output tokens/run', 'Est. cost/run', 'Minutes/run']
assert len(cells[8:]) == 6 * 8
robocurve_rows = []
for i in range(8, len(cells), 8):
    task, model, stage, count, rate, tokens, cost, minutes = cells[i:i+8]
    a, n = [int(x) for x in count.split('/')]
    assert n == 20 and a * 100 / n == float(rate.strip('%'))
    robocurve_rows.append({'task': task, 'model': model, 'successes': a, 'n': n})

rpent_text = read('research/sources/control_results_20260914/background/rpent_paper_v4.txt')
rpent_block = rpent_text.split('Table 3: Aggregate LIBERO-Pro', 1)[1].split('\f', 1)[0]
rpent = []
for label in ['πRLinf', 'Harness VLA (Codex)', 'Harness VLA (CC)']:
    line = next(line for line in rpent_block.splitlines() if line.strip().startswith(label) and len(re.findall(r'\d+\.\d+', line)) == 9)
    values = [float(n) for n in re.findall(r'\d+\.\d+', line)]
    assert all(v.is_integer() for v in values[:8])
    total = sum(values[:8])
    assert abs(total / 8 - values[8]) <= .05
    rpent.append({'method': label, 'cells': values[:8], 'redirect': int(sum(values[:8:2])),
                  'swap': int(sum(values[1:8:2])), 'successes': int(total), 'n': 800})

model_data = load('research/sources/control_results_20260914/later/enpire_site_model_scaling_data.json')
resources = load('research/sources/control_results_20260914/later/enpire_site_resource_data.json')
for file in ['enpire_site_model_scaling_data.provenance.json', 'enpire_site_resource_data.provenance.json']:
    load('research/sources/control_results_20260914/later/' + file)
hirobot = load('research/sources/control_results_20260914/background/hirobot_chart_values.json')
# A transcription of the labelled original Figure 3, independently checked in the research note.
replay_image = 'research/sources/control_results_20260914/later/agentic_replay_results_original.png'
read_bytes(replay_image)
real2sim = [
    ['Gemma 4 31B', 48, 8, 44, 2.62],
    ['Qwen 3.6 35B', 45, 11, 44, 12.97],
    ['Claude Haiku 4.5', 37, 12, 51, 9.16],
    ['GPT-5.4', 43, 12, 45, 82.30],
]
assert all(sum(r[1:4]) == 100 for r in real2sim)
assert sources == PINNED, 'Every pinned source must participate in result derivation.'

authority = {'version': '0.9', 'sources': sources, 'robodojo': {'rows': dojo, 'totals': dojo_totals},
             'robolab': lab, 'asim': asim_rows, 'robocurve': robocurve_rows, 'rpent': rpent,
             'enpire_models': model_data, 'enpire_resources': resources,
             'hirobot': hirobot, 'real2sim': real2sim}
(ROOT / 'research/results_v0_9.json').write_text(json.dumps(authority, ensure_ascii=False, indent=2) + '\n')
print('Derived verified results from', len(sources), 'frozen source files')
