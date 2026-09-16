from pathlib import Path
import subprocess,json,hashlib
ROOT=Path('/home/limx/Desktop/agent_for_robotics');A=ROOT/'.build/assets/v0_18_control';F='/home/limx/miniconda3/envs/RoboTwin/bin/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[];urls=json.loads((ROOT/'research/sources/control_extra_20260916/download_urls.json').read_text())
for name,duration,source_url in [('cube',None,'https://x.com/ZeYanjie/status/2098118164626501669'),('claw',20.566667,'https://qinengwang-aiden.github.io/demos/constraint_demos/?demo=claw')]:
 src=A/f'{name}_source.mp4';out=ROOT/'.build/clips'/f'{name}.mp4';poster=A/f'{name}.jpg'
 cmd=[F+'ffmpeg','-v','error','-y','-i',str(src)]+(['-t',str(duration)] if duration else [])+['-an','-vf','scale=1280:-2,fps=30','-c:v','libx264','-threads','2','-preset','fast','-crf','25','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
 subprocess.run(cmd,check=True);subprocess.run([F+'ffmpeg','-v','error','-y','-ss','0.5','-i',str(out),'-frames:v','1',str(poster)],check=True);subprocess.run([F+'ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
 p=json.loads(subprocess.check_output([F+'ffprobe','-v','error','-show_format','-show_streams','-of','json',str(out)]));v=next(s for s in p['streams'] if s['codec_type']=='video')
 rows.append({'name':name,'source_url':source_url,'download_url':urls[src.name],'source_file':str(src),'source_sha256':sha(src),'file':str(out),'poster':str(poster),'start_seconds':0,'duration_seconds':float(p['format']['duration']),'speed_multiplier':1,'audio':'removed for narrated talk','width':v['width'],'height':v['height'],'codec':v['codec_name'],'pixel_format':v['pix_fmt'],'sha256':sha(out),'full_decode':'passed','source_playback':'Complete X-posted video, original playback retained; no added speedup.' if name=='cube' else 'Entire Claw segment [0,20.566667) from official two-demo export; source overlay 8x retained. Cut is the title/scene change to Three-ring Threading, after final withdrawal.'})
(ROOT/'.build/clip_manifest_v10.json').write_text(json.dumps(rows,indent=2))
files=[str(p.relative_to(ROOT)) for p in A.iterdir() if p.suffix in ['.mp4','.jpg']]+[str(Path(r['file']).relative_to(ROOT)) for r in rows]+['.build/clip_manifest_v10.json']+[str(p.relative_to(ROOT)) for p in (ROOT/'research/sources/control_extra_20260916').iterdir() if p.is_file()]
(ROOT/'research/puzzle_v0_18_sources.json').write_text(json.dumps({'retrieved':'2026-09-16','cube_site_status':'403 Forbidden; no bypass attempted. Original public post/video used; action interface not disclosed.','claw_boundary_seconds':20.566667,'sha256':{f:sha(ROOT/f) for f in files}},indent=2))
