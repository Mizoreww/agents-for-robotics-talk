from pathlib import Path
import subprocess,json,hashlib,concurrent.futures
ROOT=Path('/home/limx/Desktop/agent_for_robotics');A=ROOT/'.build/assets/v0_18';F='/home/limx/miniconda3/envs/RoboTwin/bin/'
def probe(p):return json.loads(subprocess.check_output([F+'ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
jobs=[('enpire_pin','pin-success.mp4',8),('enpire_gpu','gpu-success.mp4',8),('enpire_tie','ziptie-success.mp4',8),('enpire_cut','cut-ziptie-success.mp4',8),('enpire_fleet','pin-fleet.mp4',8),('enpire_reset_full','pin-reset-only-1.mp4',8),('enpire_verify_full','ziptie-reward-bbox.mp4',1)]
def run(job):
 name,file,speed=job;source=A/file;out=ROOT/'.build/clips'/f'{name}.mp4';poster=A/f'{name}.jpg'
 subprocess.run([F+'ffmpeg','-v','error','-y','-i',str(source),'-an','-vf',f'setpts=PTS/{speed},scale=960:-2,fps=30','-c:v','libx264','-threads','2','-preset','fast','-crf','27','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
 subprocess.run([F+'ffmpeg','-v','error','-y','-ss','0.5','-i',str(out),'-frames:v','1',str(poster)],check=True)
 subprocess.run([F+'ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
 p=probe(out);v=next(s for s in p['streams'] if s['codec_type']=='video');duration=float(p['format']['duration']);srcdur=float(probe(source)['format']['duration'])
 print(name,srcdur,duration,flush=True)
 return {'name':name,'source_url':'https://research.nvidia.com/labs/gear/enpire/','download_url':'https://research.nvidia.com/labs/gear/enpire/videos/'+file,'source_file':str(source),'source_sha256':sha(source),'file':str(out),'poster':str(poster),'start_seconds':0,'duration_seconds':duration,'source_duration_seconds':srcdur,'presentation_speed':speed,'speed_multiplier':1,'audio':'removed for narrated talk','width':v['width'],'height':v['height'],'codec':v['codec_name'],'pixel_format':v['pix_fmt'],'sha256':sha(out),'full_decode':'passed','source_playback':f'Complete original file; encoded at {speed}x source time, without temporal cuts. Player rate 1x.'}
clips=list(concurrent.futures.ThreadPoolExecutor(3).map(run,jobs));(ROOT/'.build/clip_manifest_v9.json').write_text(json.dumps(clips,indent=2))
files=[str(p.relative_to(ROOT)) for p in A.iterdir() if p.is_file()]+[str(Path(c['file']).relative_to(ROOT)) for c in clips]+['.build/clip_manifest_v9.json']
files += [str(p.relative_to(ROOT)) for p in (ROOT/'research/sources/enpire_20260916').iterdir() if p.is_file()]
pins={'retrieved':'2026-09-16','commit':'99ee90acf65b5b18957c8382ad580db999528be3','sha256':{f:sha(ROOT/f) for f in files}}
(ROOT/'research/enpire_v0_18_sources.json').write_text(json.dumps(pins,indent=2))
