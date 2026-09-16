from pathlib import Path
import urllib.request, concurrent.futures, hashlib, json
ROOT=Path('/home/limx/Desktop/agent_for_robotics'); dest=ROOT/'.build/assets/v0_18'; base='https://research.nvidia.com/labs/gear/enpire/'
files=['videos/pin-success.mp4','videos/gpu-success.mp4','videos/ziptie-success.mp4','videos/cut-ziptie-success.mp4','videos/pin-fleet.mp4','videos/pin-reset-only-1.mp4','videos/ziptie-reward-bbox.mp4','sam.min.jpg','curobo.min.jpg','control.min.jpg','robot_farm.min.jpg','gpu_insertion.min.jpg','pin_insertion_2.min.jpg','push_t.min.jpg','zip_tie.min.jpg']
def fetch(f):
 target=dest/Path(f).name
 if not target.exists():
  with urllib.request.urlopen(base+f,timeout=180) as r, target.with_suffix(target.suffix+'.part').open('wb') as out:
   while block:=r.read(1024*1024):out.write(block)
  target.with_suffix(target.suffix+'.part').rename(target)
 data=target.read_bytes(); print(f,len(data),flush=True)
 return {'url':base+f,'file':str(target.relative_to(ROOT)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
rows=list(concurrent.futures.ThreadPoolExecutor(5).map(fetch,files))
(ROOT/'research/sources/enpire_20260916/downloaded_media.json').write_text(json.dumps(rows,indent=2))
