"""Prepare the community clips added on 2026-09-11 (three-part revision)."""
from pathlib import Path
import subprocess, json, hashlib, concurrent.futures
b=Path('/home/limx/Desktop/agent_for_robotics/.build'); out=b/'clips'; out.mkdir(exist_ok=True)
import shutil
ff=shutil.which('ffmpeg') or '/home/limx/miniconda3/envs/RoboTwin/bin/ffmpeg'
fp=shutil.which('ffprobe') or '/home/limx/miniconda3/envs/RoboTwin/bin/ffprobe'
assert ff and fp, 'ffmpeg/ffprobe not found on PATH'
downloads={d['name']:d for d in json.loads((b/'community_downloads.json').read_text())}
# name, source, start, duration, source post
jobs=[('ze_rubik','ze_rubik_source',0,None),('wenli_icl','wenli_icl_source',0,None),('arx_knob','arx_knob_source',0,None),
      ('show_harness','show_harness_source',39,33),('juggle','juggle_source',0,None),('xhs_piper','xhs_piper_source',0,None)]
def do(j):
    name,src,start,dur=j; f=out/(name+'.mp4')
    cmd=[ff,'-y','-v','error','-ss',str(start),'-i',str(b/'assets'/(src+'.mp4'))]
    if dur: cmd+=['-t',str(dur)]
    cmd+=['-vf',"scale=w='min(1280,iw)':h='min(720,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2",'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-an','-movflags','+faststart','-threads','2',str(f)]
    subprocess.run(cmd,check=True)
    subprocess.run([ff,'-v','error','-i',str(f),'-f','null','-'],check=True)  # full decode check
    d=json.loads(subprocess.check_output([fp,'-v','error','-show_entries','format=duration:stream=width,height,codec_name,pix_fmt','-of','json',str(f)])); duration=float(d['format']['duration'])
    poster=b/'assets'/(name+'.jpg'); t=min(1,duration/3)
    subprocess.run([ff,'-y','-v','error','-ss',str(t),'-i',str(f),'-frames:v','1',str(poster)],check=True)
    rec=downloads[src+'.mp4']
    return {'name':name,'source_file':src+'.mp4','source_url':rec['post_url'],'author':rec['author'],'posted':rec.get('posted'),'start_seconds':start,'duration_seconds':duration,'speed_multiplier':1,'audio':'removed for narrated talk','file':str(f),'poster':str(poster),'width':d['streams'][0]['width'],'height':d['streams'][0]['height'],'codec':d['streams'][0]['codec_name'],'pixel_format':d['streams'][0]['pix_fmt'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'full_decode':'passed'}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as p: r=list(p.map(do,jobs))
(b/'clip_manifest_v2.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)); print('Prepared',len(r),'clips;',round(sum(x['duration_seconds'] for x in r),2),'seconds')
for x in r: print(x['name'],x['width'],x['height'],round(x['duration_seconds'],2),x['sha256'][:12])
