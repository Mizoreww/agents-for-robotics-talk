"""Prepare source-bound 2026-09-14 clips; preserve archived clips unchanged."""
from pathlib import Path
import subprocess, json, hashlib, shutil
B=Path('/home/limx/Desktop/agent_for_robotics/.build')
ff=shutil.which('ffmpeg') or '/home/limx/miniconda3/envs/RoboTwin/bin/ffmpeg'
fp=shutil.which('ffprobe') or '/home/limx/miniconda3/envs/RoboTwin/bin/ffprobe'
base='https://raw.githubusercontent.com/cheng-haha/GPT-Policy-Eval/43929f0ee3673da67393fcbe85d43c58eb15db59/assets/'
jobs=[
 ('policy_plug',base+'plug-insertion-top-and-right-wrist.mp4','https://github.com/cheng-haha/GPT-Policy-Eval','12× source playback'),
 ('policy_goal',base+'visual-goal.mp4','https://github.com/cheng-haha/GPT-Policy-Eval','24× source playback'),
 ('roborsi_act','https://lab.noematrix.ai/assets/roborsi/demo/act-corrective-comparison-raw-v2.mp4?v=20260904-1','https://lab.noematrix.ai/blog/2-roborsi/','source comparison; no additional speed-up')]
manifest=[]
for name,url,source,speed in jobs:
 src=B/'assets/v0_6'/f'{name}.mp4'; out=B/'clips'/f'{name}.mp4'; poster=B/'assets/v0_6'/f'{name}.jpg'
 subprocess.run([ff,'-y','-v','error','-i',str(src),'-vf',"scale=w='min(1280,iw)':h='min(720,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2",'-c:v','libx264','-crf','20','-preset','fast','-pix_fmt','yuv420p','-an','-movflags','+faststart','-threads','2',str(out)],check=True)
 subprocess.run([ff,'-v','error','-i',str(out),'-f','null','-'],check=True)
 d=json.loads(subprocess.check_output([fp,'-v','error','-show_entries','format=duration:stream=width,height,codec_name,pix_fmt','-of','json',str(out)])); s=d['streams'][0]
 subprocess.run([ff,'-y','-v','error','-ss','1','-i',str(out),'-frames:v','1',str(poster)],check=True)
 manifest.append(dict(name=name,source_file=str(src),download_url=url,source_url=source,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),source_playback=speed,start_seconds=0,duration_seconds=float(d['format']['duration']),speed_multiplier=1,audio='removed for narrated talk',file=str(out),poster=str(poster),width=s['width'],height=s['height'],codec=s['codec_name'],pixel_format=s['pix_fmt'],sha256=hashlib.sha256(out.read_bytes()).hexdigest(),full_decode='passed'))
# Anonymous report clips are prepared by the reference research task, then merged here.
anon=B/'assets/v0_6/anonymous_clip_manifest.json'
if anon.exists(): manifest += json.loads(anon.read_text())
(B/'clip_manifest_v3.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print([(c['name'],c['duration_seconds']) for c in manifest])
