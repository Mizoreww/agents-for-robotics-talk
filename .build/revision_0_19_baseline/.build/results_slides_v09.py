"""Compact native result tables for the existing 1280 × 720 talk template."""
import hashlib
import json
from table_emphasis import best_cells, column_extrema, row_maxima


def make_results(root, page, text, rect, figure, band):
    data = json.loads((root / 'research/results_v0_9.json').read_text())
    pinned = json.loads((root / 'research/results_v0_9_sources.json').read_text())['sources']
    assert data['sources'] == pinned, 'Result authority must use the reviewed source identities.'
    for relative, expected in data['sources'].items():
        assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == expected, relative
    source_root = root / 'research/sources/control_results_20260914'

    def table(headers, rows, widths, y=210, row_h=43, head_h=48, size=22, x=64,
              comparisons=(), emphasize=()):
        assert len(headers) == len(widths) and all(len(row) == len(headers) for row in rows)
        selected = best_cells(rows, comparisons) | set(emphasize)
        assert all(0 <= r < len(rows) and 0 <= c < len(headers) for r, c in selected)
        els = [rect(x, y, sum(widths), head_h, '#eaf5f3')]
        for index, row in enumerate([headers] + rows):
            top = y if index == 0 else y + head_h + (index - 1) * row_h
            height = head_h if index == 0 else row_h
            if index > 0:
                els += [rect(x, top + height - 1, sum(widths), 1, '#d8e5e2')]
            left = x
            for col, (cell, width) in enumerate(zip(row, widths)):
                element = text(str(cell), left + 10, top + 4, width - 20, height - 7,
                               size, '#1d7d76' if index == 0 else '#1a1a1a',
                               index == 0 or (index - 1, col) in selected,
                               align='left' if col == 0 else 'center')
                if index > 0:
                    element['tableCell'] = [index - 1, col]
                    element['resultEmphasis'] = (index - 1, col) in selected
                els.append(element)
                left += width
        return els

    def note(value, y=620, size=18):
        return [text(value, 74, y, 1132, max(45, len(value.splitlines()) * size * 1.25), size, '#646464')]

    slides = {}
    key = 'hirobot_results'
    title = 'Hi Robot: Instruction and Progress'
    els = page(title, 1)
    els += [figure(source_root / 'background/hirobot_figure5_pdf_crop.png',
                   'Hi Robot original Figure 5; complete axes, four panels and legend',
                   64, 145, 1152, 264, 'https://arxiv.org/html/2502.19417v2#S5.F5')]
    average = data['hirobot']['values']['Average']
    rows = [[method, average['Instruction Accuracy'][method], average['Task Progress'][method]]
            for method in ['Flat VLA', 'GPT-4o High-Level', 'Hi Robot', 'Expert Human']]
    rows[-1][0] = 'Expert human high-level (oracle)'
    els += table(['Author-displayed average', 'Instruction Accuracy (%)', 'Task Progress (%)'], rows,
                 [492, 330, 330], y=425, row_h=31, head_h=35, size=20,
                 comparisons=column_extrema(rows, [(1, 'max'), (2, 'max')], range(3)))
    els += note('3 real-world task domains × 20 trials per method. Metrics count commands / objects, not successful episodes.\nHi Robot also changes training data; this comparison alone does not isolate hierarchy.', 601, 18)
    slides[key] = (title, els, ['HIROBOT'])

    title = 'RPent: Harness VLA Results'
    rows = [[r['method'].replace('πRLinf', 'Direct frozen π0.5-SFT'), f"{r['redirect']} / 400",
             f"{r['swap']} / 400", f"{r['successes']} / 800"] for r in data['rpent']]
    els = page(title, 1, 'LIBERO-Pro · same frozen VLA checkpoint · successes / evaluation episodes')
    els += table(['Method', 'Instruction redirect', 'Position swap', 'Overall'], rows,
                 [447, 240, 240, 225], y=233, row_h=66, head_h=47, size=22,
                 comparisons=column_extrema(rows, [(1, 'max'), (2, 'max'), (3, 'max')]))
    els += [text('Few-shot memory, additional planning and analytic primitives', 74, 516, 1132, 36, 25, '#1d7d76', True)]
    els += note('8 cells × 10 tasks × 10 held-out seeds. Seed 0 builds memory; seeds 1–10 evaluate without resets.\nCounts derived from Table 3 cells. CC = Claude Code. Extra compute differs; planner labels are not Astra.', 574, 19)
    slides['rpent_results'] = (title, els, ['RPENT', 'HARNESS'])

    title = 'Astra Interfaces: Three Tasks'
    els = page(title, 1, 'Same GPT-6 Astra · prompt-v3 · medium reasoning · successes / 20 episodes')
    els += table(['Task', 'Script\nupper', 'Random\nlower', 'ΔEEF\nproprio', 'Waypoint\nnone',
                  'Waypoint\nproprio', 'Code\nproprio', 'Code\nprivileged'], data['asim'],
                 [137, 145, 145, 145, 145, 145, 145, 145], y=219, row_h=65, head_h=64, size=21,
                 comparisons=row_maxima(data['asim'], range(3, 8)),
                 emphasize={(row,5) for row in range(len(data['asim']))})
    slides['interface_results'] = (title, els, ['ASIM'])

    title = 'RoboDojo: Per-Task Results'
    names = ['Organize table', 'Sort by language', 'Imitate sorting sequence', 'Arrange largest number',
             'Pack objects into box', 'Classify objects', 'Build tower', 'Make kong', 'Fold clothes', 'Bottles into dustbin']
    rows = [[name, f"{r['gpt']} / 5", f"{r['mix']} / 5"] for name, r in zip(names, data['robodojo']['rows'])]
    totals = data['robodojo']['totals']
    rows.append(['Total success', f"{totals['gpt']['successes']} / 50 (26%)", f"{totals['mix']['successes']} / 50 (48%)"])
    els = page(title, 1, 'Simulation · 10 selected tasks × 5 aligned cases · native binary success')
    els += table(['Task', 'Astra Direct', 'Astra + π0.5 Hybrid'], rows, [592, 280, 280], y=189, row_h=32, head_h=38, size=21,
                 comparisons=row_maxima(rows, [1, 2]))
    els += note('Native Score: Direct 37.81 (48 scored episodes); Hybrid 62.60 (50). Success denominator stays 50 each.\nThe motor prior, action interface and executed horizon change together.', 603, 18)
    slides['robodojo_results'] = (title, els, ['ANON'])

    title = 'RoboLab: Selected Final Slots'
    methods = ['pi05_only', 'astra_pi05', 'pure_astra', 'cosmos_nano_policy', 'dreamzero']
    rows = [[r['label']] + [f"{r['successes'][m]} / 5" for m in methods] for r in data['robolab']['tasks']]
    rows.append(['Total / 50'] + [str(next(r['successes'] for r in data['robolab']['methods'] if r['id'] == m)) for m in methods])
    els = page(title, 1, 'Descriptive comparison · 5 final slots per task and method; no pooled RoboDojo score')
    els += table(['Task', 'π0.5¹', 'Astra\nHybrid', 'Astra\nDirect', 'Cosmos3¹', 'DreamZero¹'], rows,
                 [382, 154, 154, 154, 154, 154], y=188, row_h=30, head_h=56, size=19,
                 comparisons=row_maxima(rows, range(1, 6)))
    els += note('Astra retains historical results + authorized retries; states are not strictly paired.\nTwo Direct BlocksInBin retries raised decision budget 180→500. ¹June cohort: first 5 episodes/task, including failures.\nTask versions / control settings are not verified identical. These are not fresh, uniform-budget attempts.', 587, 17)
    slides['robolab_results'] = (title, els, ['ANON'])

    title = 'Real2Sim: All Backend Results'
    rows = [[r[0], r[1], r[2], r[3], f'${r[4]:.2f}'] for r in data['real2sim']]
    els = page(title, 2, 'DROID-100 · all 100 episodes stay in each backend’s denominator')
    els += table(['Backend', 'Accepted', 'Partial', 'Failed', 'Model-call bill'], rows,
                 [392, 180, 180, 180, 220], y=228, row_h=63, head_h=46, size=23,
                 comparisons=column_extrema(rows, [(1, 'max'), (3, 'min'), (4, 'min')]))
    els += [text('Acceptance tests a selected replay, not novel-action prediction', 74, 549, 1132, 35, 25, '#1d7d76', True)]
    els += note('≤5 eligible candidates · 3 VLM judges · any judge’s best candidate ≥8/10 passes.\nBill covers model calls for the 100-episode run; perception, simulation and preparation costs are excluded.', 602, 18)
    slides['real2sim_results'] = (title, els, ['S13'])

    title = 'ENPIRE: Two Physical Tasks'
    els = page(title, 3, 'Official plot means at the stated research time · different metrics and policy families')
    els += [figure(source_root / 'later/enpire_scaling_original.png',
                   'ENPIRE complete original Figure 3; model curves, traces and fleet scaling',
                   64, 198, 532, 391, 'https://arxiv.org/html/2606.19980v1#S1.F3')]
    models = data['enpire_models']
    rows = []
    for push in models['pushtModel']:
        pin = next(row for row in models['pinModel'] if row['label'] == push['label'])
        assert len(push['runs']) == len(pin['runs']) == 4
        assert push['highlight_xs'][-1] == 8 and pin['highlight_xs'][-1] == 4
        rows.append([push['label'], f"{push['highlight_mean'][-1]:.3f}", f"{100 * pin['highlight_mean'][-1]:.1f}%"])
    els += table(['Coding agent', 'Push-T @ 8 h\nNormalized score', 'Pin @ 4 h\nSuccess rate'], rows,
                 [180, 220, 212], y=232, row_h=65, head_h=64, size=19, x=604,
                 comparisons=column_extrema(rows, [(1, 'max'), (2, 'max')]))
    els += [text('Heuristic policy', 784, 519, 220, 30, 19, '#646464', align='center'),
            text('Gradient-based', 1004, 519, 212, 30, 19, '#646464', align='center')]
    els += note('4 plotted traces per configuration; independent seed count / held-out test size not fully disclosed.\nPhysical rollouts permit ≤8 conditional retries. These are not pooled pass@1 scores.', 604, 18)
    slides['enpire_results'] = (title, els, ['S15', 'ENPIRE_SITE'])

    title = 'ENPIRE: Autoresearch in RoboCasa'
    els = page(title, 3, 'Simulation · VLA, zero-shot tool use and iterative feedback in the same study')
    els += [figure(source_root / 'later/enpire_robocasa_original.png',
                   'ENPIRE original Figure 6; RoboCasa task examples and aggregate baseline bars',
                   64, 187, 1152, 285, 'https://arxiv.org/html/2606.19980v1#S3.F6')]
    els += table(['Method', 'What changes', 'Reported evidence'],
                 [['GR00T N1.5', 'End-to-end VLA', 'Baseline'],
                  ['CaP-X*', 'Zero-shot agentic tool use', 'No autoresearch'],
                  ['ENPIRE', 'Tool / VLA code + feedback', 'Highest aggregate bar']],
                 [270, 488, 394], y=488, row_h=29, head_h=32, size=19, emphasize={(2, 2)})
    els += note('Reported 40-episode evaluations use frozen seeds / layouts / styles, one script execution per episode.\nNo reset/retry API. Exact bar values are not published; the 8 task images are examples, not 8 numeric rows.', 616, 17)
    slides['enpire_robocasa'] = (title, els, ['S15'])

    return slides, table, note, data
