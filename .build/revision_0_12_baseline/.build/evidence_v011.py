"""Read the separately frozen v0.11 evidence; normal builds never refresh it."""
import hashlib
import json
import statistics
from pathlib import Path


def load_evidence(root: Path):
    authority = json.loads((root / 'research/evidence_v0_11_sources.json').read_text())
    for relative, expected in authority['sources'].items():
        actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'v0.11 source identity changed: {relative}')
    source_dir = root / 'research/sources/astra_interfaces_frequency_20260915'
    timing = json.loads((source_dir / 'asim_query_times_derived.json').read_text())
    if timing['source_sha256'] != hashlib.sha256((source_dir / 'asim_index.html').read_bytes()).hexdigest():
        raise ValueError('Asim timing source does not match frozen HTML')
    episodes = timing['episodes']
    identities = {(r['run'], r['episode']) for r in episodes}
    if len(episodes) != 180 or len(identities) != 180:
        raise ValueError('Asim timing needs 180 unique episodes')
    for interface in ('delta', 'waypoint', 'code'):
        for task in ('Lift', 'Can', 'Square'):
            rows = [r for r in episodes if r['interface'] == interface and r['task'] == task]
            if len(rows) != 20 or any(r['state'] != 'proprio' for r in rows):
                raise ValueError('Asim timing selection drift')
    aggregate = {}
    for row in timing['summary']:
        selected = [r for r in episodes if r['interface'] == row['interface'] and (row['task'] == 'ALL' or r['task'] == row['task'])]
        times = [t for r in selected for t in r['query_seconds']]
        expected = {'episodes': len(selected), 'queries': len(times),
                    'mean_s': statistics.mean(times), 'median_s': statistics.median(times),
                    'min_s': min(times), 'max_s': max(times), 'sum_s': sum(times),
                    'inverse_mean_s': 1 / statistics.mean(times)}
        if any(row[key] != value for key, value in expected.items()):
            raise ValueError('Asim timing aggregate does not match selected queries')
        if row['task'] == 'ALL':
            aggregate[row['interface']] = row
    if set(aggregate) != {'delta', 'waypoint', 'code'}:
        raise ValueError('Asim timing interface missing')
    return aggregate
