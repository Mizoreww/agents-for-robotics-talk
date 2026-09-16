"""Fail-closed provenance for the official-site reset cases added in v0.19."""
import hashlib
import json

RESET_CLIPS = {'enpire_reset_pusht', 'enpire_reset_tie', 'enpire_reset_gpu'}


def verify_reset_sources(root):
    pins = json.loads((root / 'research/enpire_v0_19_sources.json').read_text())
    for file, expected in pins['sha256'].items():
        if hashlib.sha256((root / file).read_bytes()).hexdigest() != expected:
            raise ValueError(f'ENPIRE reset source drift: {file}')
    clips = json.loads((root / '.build/clip_manifest_v11.json').read_text())
    if {c['name'] for c in clips} != RESET_CLIPS:
        raise ValueError('Incomplete reset case selection')
    for clip in clips:
        if clip['start_seconds'] != 0 or clip['full_decode'] != 'passed':
            raise ValueError('Reset case must preserve a complete decoded sequence')
        if abs(clip['duration_seconds'] * 8 - clip['source_duration_seconds']) >= .4:
            raise ValueError('Reset timing or playback-rate drift')
    return pins
