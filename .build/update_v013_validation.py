from pathlib import Path
import ast,json,re
B=Path('.build');base=B/'revision_0_13_baseline';p=B/'validate_standalone.py';s=(base/p).read_text()
info=json.loads((B/'v0_13_page_map.json').read_text());mapping={int(k):v for k,v in info['old_to_new'].items()}
# Remove the exact table contracts for pages that no longer exist as native tables.
tree=ast.parse(s);lines=s.splitlines(True)
for node in reversed(tree.body):
 if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='table_cells' and isinstance(node.value.args[0],ast.Constant) and node.value.args[0].value in {8,10,16,17}:
  del lines[node.lineno-1:node.end_lineno]
s=''.join(lines)
s='\n'.join(l for l in s.splitlines() if not any(x in l for x in ["for n in [7,8]:", "slide(7)", "slide(8)","dojo_names=", "lab_methods="]))+'\n'
s=s.replace("assert slide(9)['ids']==['RPENT'] and slide(15)['ids']==['ANON']","assert slide(15)['ids']==['ANON']")
s=s.replace(",'6%到32%'",'')
s=re.sub(r'slide\((\d+)\)',lambda m:f'slide({mapping[int(m[1])]})',s)
s=re.sub(r'table_cells\((\d+),',lambda m:f'table_cells({mapping[int(m[1])]},',s)
for old in ['[21,22,23]','[28,29,30,31,32]','[12,25,35]']:
 s=s.replace(old,repr([mapping[n] for n in ast.literal_eval(old)]))
s=s.replace('N=38;V=18','N=35;V=18').replace('opening_slides==[4,20,28]','opening_slides==[4,17,25]').replace("['1 · Agent Controls Robot']*16","['1 · Agent Controls Robot']*13")
s=re.sub(r'^expected_keys=.+$',f"expected_keys={info['new_order']!r}",s,flags=re.M)
old_titles=ast.literal_eval(re.search(r'^expected_titles=(.+)$',s,re.M)[1]);new_titles=['']*35
for old,new in mapping.items():new_titles[new-1]=old_titles[old-1]
new_titles[11]='RoboDojo: Overall Results';new_titles[12]='RoboLab: Overall Results';new_titles[13]='RoboDojo: Task-Level Patterns'
s=re.sub(r'^expected_titles=.+$',f'expected_titles={new_titles!r}',s,flags=re.M)
for name in ['expected_bold','expected_media']:
 old=ast.literal_eval(re.search(r'^'+name+r'=(.+)$',s,re.M)[1]);new={mapping[k]:v for k,v in old.items() if k not in ({8,10,16,17} if name=='expected_bold' else set())}
 s=re.sub(r'^'+name+r'=.+$',f'{name}={new!r}',s,flags=re.M)
m=re.search(r'for number,terms in (\{.+?\})\.items\(\):',s);old=ast.literal_eval(m[1]);new={mapping[k]:v for k,v in old.items() if k not in {10,16,17}}
s=s[:m.start(1)]+repr(new)+s[m.end(1):]
s=s.replace("==60\n","==55\n").replace("==[15,22,27,29,31]","==[11,12,13,14,19,24,26,28]")
a=s.index("baseline=json.loads");b=s.index('\n# v0.9:',a)
s=s[:a]+'''baseline=json.loads((B/'revision_0_13_baseline/.build/standalone_build_audit.json').read_text())
assert {r['name']:r['sha256'] for r in baseline['media']}=={r['name']:r['sha256'] for r in deck['media']}
removed_alts={
 'Original Direct LIBERO-40 success-rate panel; uncertainty and all model labels retained',
 'Original supervised LIBERO-40 panel; VLA-alone baseline and uncertainty retained',
 'RPent original framework',
}
removed_figures={r['sha256'] for r in baseline['images'] if r.get('alt') in removed_alts}
assert len(removed_figures)==3
from report_figures_v013 import load_report_figures
captures=load_report_figures(ROOT)
new_image_keys={name:hashlib.sha256(file.read_bytes()).hexdigest() for name,file in captures.items()}
assert set(deck['assets'])==({r['sha256'] for r in baseline['images']}-removed_figures)|set(new_image_keys.values())
for n,names in {12:['panel-score-ranking.png','panel-sr-ranking.png'],13:['robolab-success-ranking.png'],14:['task-score-table-complete.png']}.items():
 assert 'data-table-cell' not in slide(n)['html']
 assert slide(n)['ids']==['ANON']
 for name in names:assert new_image_keys[name] in slide(n)['html']
assert all(t in slide(12)['html'] for t in ['24/50','13/50','not paired reruns'])
assert all(t in slide(12)['script'] for t in ['48个scored episodes','分母都保持50','执行段长'])
assert all(t in slide(13)['script'] for t in ['authorized retries','180提高到500','June cohort','49/50','46/50'])
assert all(t in slide(14)['script'] for t in ['不是success rate','64与12','十个任务','七种方法'])
assert slide(7)['new_slide_key']=='astra_direct'
for r in deck['slides'][:16]:
 assert 'S09' not in r['ids'] and 'RPENT' not in r['ids']
 assert 'Claude' not in r['script'] and 'RPent' not in r['script']
''' + s[b:]
p.write_text(s)
# The figure-dialog tests follow the new ordering; the player itself is unchanged.
p=B/'browser_audit.mjs';s=(base/p).read_text().replace('[15, 22, 27, 29, 31]','[11, 12, 13, 14, 19, 24, 26, 28]');p.write_text(s)
p=B/'extended_visual_audit.mjs';s=(base/p).read_text().replace('v0.12','v0.13').replace('v0_12','v0_13')
s=s.replace('[[5,0],[5,1],[5,2],[15,0],[22,0],[27,0],[29,0],[31,0],[33,0],[34,0]]','[[5,0],[5,1],[5,2],[11,0],[12,0],[12,1],[13,0],[14,0],[19,0],[24,0],[26,0],[28,0],[30,0],[31,0]]')
s=s.replace("[[12,'keyboard'],[25,'office_newton'],[35,'quad_rl'],[13,'asim_delta'],[13,'asim_waypoint']]","[[8,'keyboard'],[22,'office_newton'],[32,'quad_rl'],[9,'asim_delta'],[9,'asim_waypoint']]").replace('await go(12);await page.keyboard','await go(8);await page.keyboard');p.write_text(s)
