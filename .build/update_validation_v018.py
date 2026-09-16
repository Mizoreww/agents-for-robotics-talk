from pathlib import Path
import re,ast
B=Path('.build');p=B/'validate_standalone.py';s=(B/'revision_0_18_baseline/.build/validate_standalone.py').read_text()
# Map each retained/replaced semantic position to its reviewed new page.
mp={**{n:n for n in range(1,9)},**{n:n+1 for n in range(9,24)},24:25,25:27,26:29,27:28,28:30,29:31,30:33,31:35,32:36}
s=re.sub(r'slide\((\d+)\)',lambda m:f'slide({mp[int(m[1])]})',s)
s=re.sub(r'table_cells\((\d+),',lambda m:f'table_cells({mp[int(m[1])]},',s)
s=s.replace('N=32;V=20','N=36;V=25').replace('opening_slides==[4,17,22]','opening_slides==[4,18,23]')
order=None
for n in ast.parse((B/'build_selfcontained.py').read_text()).body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='order' for t in n.targets):order=ast.literal_eval(n.value)
s=re.sub(r'^expected_keys=.*$', 'expected_keys='+repr(order),s,flags=re.M)
# Titles remain an independently checked exact list.
titles=['Agents for Robotics','Demo: Painting with Feedback','Three Roles for Robotics Agents','Agent Controls Robot','Hierarchical Robot Control','Where Does Generalization Live?','Astra: Stronger Real-Robot Performance','Astra: More Real-Robot Demos','Robot Puzzle Demos in Simulation','One Model, Different Control Interfaces','Astra Interfaces: Three Tasks','Astra: Introducing a Hybrid Architecture','RoboDojo: Overall Results','RoboLab: Overall Results','RoboDojo: Task-Level Patterns','High Latency Limits Real-Time Control','Control: Strengths and Open Gaps','Agent Creates Data','Astra: Scene Reconstruction','Astra: Hand Assets','Astra: Replay and Data Rollout','Data: From Demos to Useful Data','Agent Improves Policy','ENPIRE: Environment and Improvement','ENPIRE: Reset and Verification','ENPIRE: Two Ways to Improve Policy','ENPIRE: What Did the Agent Change?','ENPIRE: Two Physical Tasks','ENPIRE: Parallel Physical Research','ENPIRE: Autoresearch in RoboCasa','ENPIRE: Learned Manipulation Demos','ENPIRE: Experience Across Tasks','ENPIRE: Cost of Physical Research','Toward Recursive Self-Improvement','Takeaways','Thank You']
s=re.sub(r'^expected_titles=.*$','expected_titles='+repr(titles),s,flags=re.M)
s=s.replace("['1 · Agent Controls Robot']*13+['2 · Agent Creates Data']*5+['3 · Agent Improves Policy']*9", "['1 · Agent Controls Robot']*14+['2 · Agent Creates Data']*5+['3 · Agent Improves Policy']*12")
s=s.replace("for n in [22, 23, 24, 25, 26]:assert slide(n)['ids']==['S15']", "for n in [23,24,27]:assert slide(n)['ids']==['S15']")
s=s.replace("assert all(t in slide(31)['footer'] for t in ['4 experts','FULL EVAL NOT MET','8×'])", "assert '8×' in slide(31)['footer'] and 'ENPIRE' in slide(31)['title']")
a=s.index('# v0.17 pairs');b=s.index('from data_demos_v015',a)
s=s[:a]+'''# v0.18 retains every pre-existing Control/Data clip byte-for-byte.
baseline=json.loads((B/'revision_0_18_baseline/.build/standalone_build_audit.json').read_text())
expected_retained={r['name']:r['sha256'] for r in baseline['media'] if r['slide']<=21}
assert expected_retained=={r['name']:r['sha256'] for r in deck['media'] if r['name'] in expected_retained}
from enpire_v018 import verify_enpire, verify_puzzles
verify_enpire(ROOT);verify_puzzles(ROOT)
'''+s[b:]
s=s.replace("deck['slides'][16:21]", "deck['slides'][17:22]").replace("deck['slides'][:16]", "deck['slides'][:17]")
a=s.index("old_text=(B/");b=s.index('for n,names in ',a)
s=s[:a]+s[b:]
s=s.replace("{12:['panel-score-ranking.png','panel-sr-ranking.png'],13:['robolab-success-ranking.png'],14:['task-score-table-complete.png']}","{13:['panel-score-ranking.png','panel-sr-ranking.png'],14:['robolab-success-ranking.png'],15:['task-score-table-complete.png']}")
s=s.replace('expected_bold={7:', 'expected_bold={7:').replace('}, 10:','}, 11:').replace('}, 27:','}, 28:').replace('}, 28: {(2, 2)}','}, 30: {(2, 2)}').replace('}, 30: {(0, 1)','}, 33: {(0, 1)')
s=s.replace("{27: ['4 plotted traces', 'conditional retries', 'not pooled pass@1'], 28: ['40-episode'", "{28: ['4 plotted traces', 'conditional retries', 'not pooled pass@1'], 30: ['40-episode'")
s=s.replace('for n in [8, 18, 19, 20, 29]:','for n in [8, 9, 19, 20, 21, 31]:').replace("sum(r['minutes'] for r in deck['slides'])==51","sum(r['minutes'] for r in deck['slides'])==59")
s=s.replace("'clip_manifest_v8.json']","'clip_manifest_v8.json','clip_manifest_v9.json','clip_manifest_v10.json']")
media={2:{'painting'},7:{'astra_insertion','astra_bowl'},8:{'policy_plug','keyboard'},9:{'cube','claw'},10:{'asim_delta','asim_waypoint','asim_code'},12:{'anon_hybrid_pack','anon_direct_sort'},19:{'office_newton','kitchen'},20:{'rope_hand','hand'},21:{'dexgpt','astra_real2sim'},25:{'enpire_reset_full','enpire_verify_full'},29:{'enpire_fleet'},31:{'enpire_pin','enpire_tie','enpire_cut'},32:{'enpire_gpu'}}
s=re.sub(r'^expected_media=.*$','expected_media='+repr(media),s,flags=re.M)
s=s.replace('[11,12,13,14,23,25,27,28]', '[12,13,14,15,24,26,27,28,29,30]')
p.write_text(s)
# Demo tests continue to guard the Data content while new ENPIRE tests own global scope.
p=B/'test_data_demos_v015.py';s=(B/'revision_0_18_baseline/.build/test_data_demos_v015.py').read_text()
a=s.index('    def test_non_data_pages_unchanged');b=s.index('    def test_chapter_is_demo_only',a)
s=s[:a]+s[b:]
s=s.replace("len(deck['slides']), 32", "len(deck['slides']), 36").replace("deck['slides'][16:21]", "deck['slides'][17:22]").replace('17 <= m[\'slide\'] <= 21','18 <= m[\'slide\'] <= 22')
s=s.replace('for n in [18, 19, 20]', 'for n in [19, 20, 21]').replace("{18: {'office_newton', 'kitchen'}, 19: {'hand', 'rope_hand'},\n                          20: {'astra_real2sim', 'dexgpt'}}", "{19: {'office_newton', 'kitchen'}, 20: {'hand', 'rope_hand'},\n                          21: {'astra_real2sim', 'dexgpt'}}")
s=re.sub(r"deck\['slides'\]\[(17|18|19)\]",lambda m:f"deck['slides'][{int(m[1])+1}]",s)
s=s.replace("for m in before['media']}", "for m in before['media'] if m['slide']<=24}").replace("for m in deck['media'] if m['name'] != 'kitchen'}", "for m in deck['media'] if m['slide']<=22 and m['name'] not in {'kitchen','cube','claw'}}")
p.write_text(s)
