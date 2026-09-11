"""Subset Noto Sans CJK SC to the glyphs used by the generated script, slide text and player UI."""
from pathlib import Path
import json, re, subprocess, sys
ROOT=Path('/home/limx/Desktop/agent_for_robotics'); B=ROOT/'.build'
texts=[(ROOT/'output/Speaker_Script_Revised.md').read_text(),(B/'standalone_player.js').read_text(),(B/'script_revised.md').read_text()]
try: texts.append(json.dumps([r.get('title','') for r in json.loads((B/'slide_records_revised.json').read_text())],ensure_ascii=False))
except FileNotFoundError: pass
# Slide text can include Chinese too (e.g. 小红书 credits); include the deck html when present.
html=ROOT/'output/Agents_for_Robotics_Self_Contained.html'
if html.exists():
    m=re.search(r'<script type="application/json" id="deck-data">(.*?)</script>',html.read_text(),re.S)
    if m: texts.append(json.loads(m.group(1))['scriptMarkdown']); texts.append(''.join(s['html'] for s in json.loads(m.group(1))['slides']))
chars=sorted({c for t in texts for c in t if ord(c)>0x2E7F})
(B/'cjk_required_chars.txt').write_text(''.join(chars))
env={'PYTHONPATH':str(B/'font_deps')}
subprocess.run([sys.executable,'-m','fontTools.subset','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','--font-number=2','--text-file='+str(B/'cjk_required_chars.txt'),'--flavor=woff2','--output-file='+str(B/'assets/noto_cjk_script.woff2'),'--layout-features=*','--no-hinting','--desubroutinize'],check=True,env=env)
from fontTools.ttLib import TTFont
f=TTFont(B/'assets/noto_cjk_script.woff2'); cmap=f.getBestCmap(); missing=[c for c in chars if ord(c) not in cmap]
print(json.dumps({'required_chars':len(chars),'cjk_chars':sum(1 for c in chars if 0x4E00<=ord(c)<=0x9FFF),'missing':missing,'woff2_bytes':(B/'assets/noto_cjk_script.woff2').stat().st_size},ensure_ascii=False))
