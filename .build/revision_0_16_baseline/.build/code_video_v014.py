"""Verify the separately pinned Square code/proprio replay before embedding it."""
from pathlib import Path
import hashlib
import json

EXPECTED_RUN = 'Square__code__proprio__codex-gpt-6-astra__s0__20260908T142029Z'
EXPECTED_SHA = 'beff2d66b6b6454652c19e9229c35183eff75e026671b06749bdbaaf57d981ef'


def verify_code_video(root):
    root = Path(root)
    pins = json.loads((root / 'research/code_video_v0_14_sources.json').read_text())
    for relative, expected in pins['sha256'].items():
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Code replay source identity mismatch: {relative}')
    capture = json.loads((root / '.build/assets/v0_13_code/capture.json').read_text())
    assert capture['source']['run'] == EXPECTED_RUN
    assert capture['source']['episode'] == 'ep00.mp4'
    assert capture['source']['url'].endswith('/' + EXPECTED_RUN + '/ep00.mp4')
    assert capture['sha256'] == EXPECTED_SHA
    assert capture['group_successes'] == 16 and capture['group_episodes'] == 20
    assert float(capture['ffprobe']['format']['duration']) == 6.4
    assert capture['query_seconds'] == 41.339
    assert capture['full_decode_passed'] is True
    html = (root / 'research/sources/control_action_interfaces_20260914/asim_index_pinned.html').read_text()
    assert EXPECTED_RUN in html and 'plan(scene)' in html
    assert capture['pinned_html_sha256'] == hashlib.sha256(html.encode()).hexdigest()
    return capture
