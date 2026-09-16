"""Official ENPIRE media and the scoped RSI discussion for chapter three."""
import hashlib
import json

SITE = 'https://research.nvidia.com/labs/gear/enpire/'
PAPER = 'https://arxiv.org/html/2606.19980v1'
NEW_CLIPS = {'enpire_pin', 'enpire_gpu', 'enpire_tie', 'enpire_cut',
             'enpire_fleet', 'enpire_reset_full', 'enpire_verify_full'}


def verify_enpire(root):
    pins = json.loads((root / 'research/enpire_v0_18_sources.json').read_text())
    for relative, expected in pins['sha256'].items():
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != expected:
            raise ValueError(f'ENPIRE source drift: {relative}')
    clips = json.loads((root / '.build/clip_manifest_v9.json').read_text())
    if {c['name'] for c in clips} != NEW_CLIPS:
        raise ValueError('Incomplete ENPIRE clip set')
    for c in clips:
        if abs(c['duration_seconds'] * c['presentation_speed'] - c['source_duration_seconds']) > .4:
            raise ValueError(f'Full-sequence duration mismatch: {c["name"]}')
        if c['start_seconds'] != 0 or c['full_decode'] != 'passed':
            raise ValueError('ENPIRE clips must preserve complete source sequences')
    return pins


def verify_puzzles(root):
    pins = json.loads((root / 'research/puzzle_v0_18_sources.json').read_text())
    for relative, expected in pins['sha256'].items():
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Puzzle source drift: {relative}')
    clips = json.loads((root / '.build/clip_manifest_v10.json').read_text())
    if {c['name'] for c in clips} != {'cube', 'claw'}:
        raise ValueError('Incomplete puzzle clip set')
    claw = next(c for c in clips if c['name'] == 'claw')
    if abs(claw['duration_seconds'] - pins['claw_boundary_seconds']) > .05:
        raise ValueError('Claw clip must end at the documented source scene boundary')
    return pins


def build_slides(root, page, text, rect, connector, figure, video_el, band, layouts, placements):
    """Use the existing deck's typography, diagrams and player placement contract."""
    assets = root / '.build/assets/v0_18'

    def video(key, name, x, y, w, h, caption):
        els, box = video_el(name, x, y, w, h, caption)
        placements.setdefault(key, []).append((name, box))
        return els

    env = page('ENPIRE: Reset and Verification', 3)
    env += [text('Automatic reset', 64, 151, 560, 36, 26, '#1d7d76', True),
            text('Two-view verification', 656, 151, 560, 36, 26, '#1d7d76', True)]
    env += video('enpire_env', 'enpire_reset_full', 64, 210, 560, 327, 'Pin reset · complete sequence · 8×')
    env += video('enpire_env', 'enpire_verify_full', 656, 210, 560, 327, 'Zip-tie detector views · complete sequence · 1×')
    env += band('Reset and verifier stay fixed during policy improvement.')

    methods = page('ENPIRE: Two Ways to Improve Policy', 3)
    for x, title, file, equation, detail in [
        (64, 'Push-T: heuristic code', 'push_t.min.jpg', 'a = f(o)', 'Revise geometry and feedback logic'),
        (656, 'Pin insertion: learned policy', 'pin_insertion_2.min.jpg', 'πθ(a | o)', 'Revise BC / RL recipes and train θ')]:
        methods += [text(title, x, 151, 560, 38, 26, '#1d7d76', True),
                    figure(assets / file, 'ENPIRE official task photograph: ' + title, x, 211, 560, 245, SITE),
                    text(equation, x, 478, 560, 43, 31, '#1d7d76', True, align='center'),
                    text(detail, x, 539, 560, 40, 23, align='center')]
    methods += band('The Agent chooses and revises the algorithm; the policy executes the motion.')

    fleet = page('ENPIRE: Parallel Physical Research', 3)
    fleet += video('enpire_fleet_page', 'enpire_fleet', 64, 177, 560, 328, 'Official fleet recording · complete sequence · 8×')
    original = next(e.copy() for e in layouts[17] if e.get('alt', '').startswith('Original ENPIRE pin'))
    x, y, w, h = original['bbox']
    scale = min(560 / w, 328 / h)
    original['bbox'] = [656 + (560-w*scale)/2, 177 + (328-h*scale)/2, w*scale, h*scale]
    fleet += [original, text('1 pair: >1.5 h', 100, 551, 490, 42, 30, '#646464', True, align='center'),
              text('8 pairs: ~40 min', 690, 551, 490, 42, 30, '#1d7d76', True, align='center'),
              text('Time to near-perfect pin performance · conditional retries allowed', 64, 615, 1152, 35, 21, '#646464', align='center')]

    demos = page('ENPIRE: Learned Manipulation Demos', 3)
    for x, name, label in [(64, 'enpire_pin', 'Pin insertion'), (460, 'enpire_tie', 'Tie zip-tie'), (856, 'enpire_cut', 'Cut zip-tie')]:
        demos += [text(label, x, 155, 360, 37, 26, '#1d7d76', True)]
        demos += video('enpire_demos', name, x, 222, 360, 312, 'Complete official sequence · 8×')
    demos += band('Observe recovery across attempts; physical pass@8 includes conditional retries.')

    transfer = page('ENPIRE: Experience Across Tasks', 3)
    for i, (label, sub) in enumerate([('Pin autoresearch', 'Experiments + reflection'), ('Written recipes', 'Persistent experience'), ('GPU autoresearch', 'New task instructions')]):
        x = 64 + 404*i
        transfer += [rect(x, 158, 344, 100, '#eaf5f3' if i == 1 else '#f4f6f5', '#c6d9d6'),
                     text(label, x+10, 177, 324, 32, 24, '#1d7d76', True, align='center'),
                     text(sub, x+10, 216, 324, 28, 19, '#646464', align='center')]
        if i < 2:
            transfer += [connector(x+344, 208, x+404, 208)]
    transfer += video('enpire_transfer', 'enpire_gpu', 64, 298, 650, 307, 'GPU insertion · complete official sequence · 8×')
    transfer += [text('What carries over?', 764, 339, 444, 40, 28, '#1d7d76', True),
                 text('A written summary\nof training experience', 764, 397, 444, 87, 27),
                 text('No prior checkpoints or raw trajectories', 764, 511, 444, 71, 21, '#646464')]

    rsi = page('Toward Recursive Self-Improvement', 3)
    rsi += [text('RSI: can experience improve the improver?', 64, 151, 1152, 44, 29, '#1d7d76', True)]
    for x, w, label, sub, accent in [(64, 260, 'Agent', 'Hypothesis + edits', True),
                                    (438, 330, 'Policy / training code', 'New version', False),
                                    (884, 332, 'Physical experiments', 'Fixed tests + logs', False)]:
        rsi += [rect(x, 259, w, 107, '#2ba39b' if accent else '#f4f6f5', '#c6d9d6'),
                text(label, x+10, 277, w-20, 34, 25, '#ffffff' if accent else '#1a1a1a', True, align='center'),
                text(sub, x+10, 321, w-20, 28, 19, '#e2f3ef' if accent else '#646464', align='center')]
    rsi += [connector(324, 312, 438, 312), connector(768, 312, 884, 312),
            connector(1050, 366, 1050, 428, '#2ba39b', False), connector(1050, 428, 194, 428, '#2ba39b', False),
            connector(194, 428, 194, 366, '#2ba39b'), text('ENPIRE: feedback improves the next policy', 362, 385, 622, 32, 22, '#1d7d76', align='center'),
            text('Retained recipes / memory', 64, 481, 465, 42, 27, '#1d7d76', True),
            connector(532, 504, 625, 504), text('Better future research?', 658, 481, 558, 44, 29, '#aa514a', True),
            text('Open test: held-out tasks, matched budgets, no regression', 64, 575, 1152, 45, 27, '#646464', align='center')]
    return {
        'enpire_env': ('ENPIRE: Reset and Verification', env, ['S15', 'ENPIRE_SITE']),
        'enpire_methods': ('ENPIRE: Two Ways to Improve Policy', methods, ['S15', 'ENPIRE_SITE', 'ENPIRE_CODE']),
        'enpire_fleet_page': ('ENPIRE: Parallel Physical Research', fleet, ['S15', 'ENPIRE_SITE']),
        'enpire_demos': ('ENPIRE: Learned Manipulation Demos', demos, ['S15', 'ENPIRE_SITE']),
        'enpire_transfer': ('ENPIRE: Experience Across Tasks', transfer, ['ENPIRE_TRANSFER', 'ENPIRE_SITE']),
        'rsi_summary': ('Toward Recursive Self-Improvement', rsi, ['ENPIRE_TRANSFER', 'ROBORSI', 'DGM']),
    }
