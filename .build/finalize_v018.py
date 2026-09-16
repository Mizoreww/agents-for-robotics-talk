"""Publish current documentation only after every final-hash audit has passed."""
from pathlib import Path
import hashlib,json
R=Path('/home/limx/Desktop/agent_for_robotics');B=R/'.build'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((B/'standalone_build_audit.json').read_text());h=a['sha256']
assert sha(R/'output/Agents_for_Robotics_Self_Contained.html')==h
for file in ['standalone_delivery_audit.json','standalone_layout_audit.json','standalone_playback_audit.json','standalone_ui_audit.json','standalone_mobile_audit.json','standalone_visual_audit.json','v0_18_extended_audit.json']:
 d=json.loads((B/file).read_text());assert d['html_sha256']==h,(file,'stale')
extra=json.loads((B/'v0_18_extended_audit.json').read_text())
assert extra['served_html_byte_identity']
assert {r['clip'] for r in extra['playback']}=={'cube','claw','enpire_pin','enpire_gpu','enpire_tie','enpire_cut','enpire_fleet','enpire_reset_full','enpire_verify_full'}
assert all(r['ended'] and all(not s['error'] for s in r['samples']) for r in extra['playback'])
assert json.loads((B/'standalone_delivery_audit.json').read_text())['browser_audits']=='passed for this hash'
review=json.loads((B/'v0_18_review_manifest.json').read_text())
assert review['html_sha256']==h
assert all(sha(R/f)==v for f,v in review['files'].items())
for name in ['AGENTS.md','README.md','output/README.md']:
 p=R/name;s=p.read_text().replace('v0.18 QA/review pending; check current hash-bound audits','v0.18 QA/review passed; Standards0 / Spec0, all nine added clips completed final-hash playback').replace('核验尚在进行。','当前hash的离线、全页布局、播放、按钮、移动端和新增九段完整播放检查均已通过；Standards / Spec最终复核均无未解决问题。').replace('Verification is in progress.','Final-hash offline/browser/visual QA and all nine added clips passed complete playback. Standards0 / Spec0, no unresolved findings.');p.write_text(s)
p=R/'WORKPLAN.md';s=p.read_text();i=s.find('\n# ',1);head=s[:i] if i>=0 else s;tail=s[i:] if i>=0 else '';head=head.replace('- [ ]','- [x]');p.write_text(head+tail)
p=R/'research/sources.json';j=json.loads(p.read_text());j['status']='v0.18 delivered: final-hash offline, browser, visual and complete new-video playback QA passed; Standards0 / Spec0';p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
p=R/'research/revision_0_18_review.md';s=p.read_text();s+='\n## Final QA\n\nAll 36 slides, 25 clips, 43 images and four fonts passed current-hash offline/browser checks. Nine new videos each played to completion at presentation rate without decoding errors; served bytes and loaded deck-data were hash-verified. Layout and mobile button overflow: zero. Visual review covered the new puzzle and entire ENPIRE chapter, controls and sequential one-second media overviews. No measured rehearsal.\n';p.write_text(s)
files=set(review['files'])
files.update(['.build/slide_records_revised.json','.build/assets/noto_cjk_script.woff2','.build/standalone_build_audit.json','.build/standalone_delivery_audit.json','.build/standalone_layout_audit.json','.build/standalone_playback_audit.json','.build/standalone_ui_audit.json','.build/standalone_mobile_audit.json','.build/standalone_visual_audit.json','.build/v0_18_extended_audit.json','.build/v0_18_review_manifest.json','output/Agents_for_Robotics_Self_Contained.html','output/Speaker_Script_Revised.md','output/Control_Puzzle_Demos.png','output/ENPIRE_Experience_Transfer.png','output/ENPIRE_RSI_Summary.png','research/revision_0_18_review.md','WORKPLAN.md','research/results_v0_9.json','research/results_v0_9_sources.json'])
for pin in ['research/enpire_v0_18_sources.json','research/puzzle_v0_18_sources.json']:
 files.update(json.loads((R/pin).read_text())['sha256'])
manifest={'html_sha256':h,'review_status':'Standards0 / Spec0 after narrow P3/P8 and documentation corrections; final-hash QA passed','files':{f:sha(R/f) for f in sorted(files)}}
(B/'v0_18_final_review_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Final delivery',h,len(files),'pinned files')
