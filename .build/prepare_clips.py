from pathlib import Path
import subprocess,json,hashlib,concurrent.futures
from PIL import Image
b=Path('/home/limx/Desktop/agent_for_robotics/.build');out=b/'clips';out.mkdir(exist_ok=True)
import shutil
ff=shutil.which('ffmpeg') or '/home/limx/miniconda3/envs/RoboTwin/bin/ffmpeg'
fp=shutil.which('ffprobe') or '/home/limx/miniconda3/envs/RoboTwin/bin/ffprobe'
assert ff and fp, 'ffmpeg/ffprobe not found on PATH'
jobs=[('astra_bowl','astra_bowl',0,None),('ar2s_teaser','ar2s_teaser',0,None),('enpire_verify','enpire_verify',0,None),('astra_insertion','astra_insertion',0,None),('painting','painting_source',0,None),('astra_real2sim','astra_real2sim_source',0,None),('astra_microphone','astra_microphone_source',35,25),('aspire_trace','aspire_trace',0,30)]
def do(j):
 name,src,start,dur=j;f=out/(name+'.mp4');cmd=[ff,'-y','-v','error','-ss',str(start),'-i',str(b/'assets'/(src+'.mp4'))]
 if dur:cmd+=['-t',str(dur)]
 cmd+=['-vf',"scale=w='min(1280,iw)':h='min(720,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2",'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-an','-movflags','+faststart','-threads','2',str(f)]
 subprocess.run(cmd,check=True)
 # Decode every delivered frame; unlike a metadata read this checks the whole stream.
 subprocess.run([ff,'-v','error','-i',str(f),'-f','null','-'],check=True)
 d=json.loads(subprocess.check_output([fp,'-v','error','-show_entries','format=duration:stream=width,height,codec_name,pix_fmt','-of','json',str(f)]));duration=float(d['format']['duration'])
 poster=b/'assets'/(name+'.jpg');t=8 if name=='painting' else min(1,duration/3)
 subprocess.run([ff,'-y','-v','error','-ss',str(t),'-i',str(f),'-frames:v','1',str(poster)],check=True)
 return {'name':name,'source_file':src+'.mp4','start_seconds':start,'duration_seconds':duration,'speed_multiplier':1,'audio':'removed for narrated talk','file':str(f),'poster':str(poster),'width':d['streams'][0]['width'],'height':d['streams'][0]['height'],'codec':d['streams'][0]['codec_name'],'pixel_format':d['streams'][0]['pix_fmt'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'full_decode':'passed'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as p:r=list(p.map(do,jobs))
(b/'clip_manifest.json').write_text(json.dumps(r,indent=2));print('Prepared',len(r),'clips;',round(sum(x['duration_seconds'] for x in r),2),'seconds')
