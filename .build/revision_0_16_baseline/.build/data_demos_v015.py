"""Independent source and byte identities for the demo-only Data chapter."""
import hashlib
import json
from pathlib import Path


def verify_data_demos(root):
    root = Path(root)
    pins = json.loads((root / 'research/data_demos_v0_15_sources.json').read_text())
    for relative, expected in pins['sha256'].items():
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Data demo source changed: {relative}')
    return pins
