"""Independent source and byte identities for the demo-only Data chapter."""
import hashlib
import json
from pathlib import Path


def _verify_manifest(root, filename):
    root = Path(root)
    pins = json.loads((root / 'research' / filename).read_text())
    for relative, expected in pins['sha256'].items():
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Data demo source changed: {relative}')
    return pins


def verify_data_demos(root):
    return _verify_manifest(root, 'data_demos_v0_15_sources.json')


def verify_data_extra(root):
    return _verify_manifest(root, 'data_extra_v0_16_sources.json')
