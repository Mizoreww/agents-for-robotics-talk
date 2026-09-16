"""Archive three official reset cases; preserve complete sequences at site playback speed."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / '.build/assets/v0_19'
SITE = 'https://research.nvidia.com/labs/gear/enpire/'
ASSETS.mkdir(parents=True, exist_ok=True)


def sha(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()


def probe(file):
    return json.loads(subprocess.check_output([
        '/home/limx/miniconda3/envs/RoboTwin/bin/ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(file)]))


def prepare(item):
    name, filename = item
    source = ASSETS / filename
    url = SITE + 'videos/' + filename
    # Require each exact URL to occur in the already-pinned official inventory.
    inventory = json.loads((ROOT / 'research/sources/enpire_20260916/media_inventory.json').read_text())
    assert url in {row['url'] for row in inventory}
    if not source.exists():
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=120) as response, source.open('wb') as out:
            while chunk := response.read(1048576):
                out.write(chunk)
    source_seconds = float(probe(source)['format']['duration'])
    clip = ROOT / '.build/clips' / (name + '.mp4')
    poster = ASSETS / (name + '.jpg')
    subprocess.run(['/home/limx/miniconda3/envs/RoboTwin/bin/ffmpeg', '-v', 'error', '-y', '-i', str(source), '-an',
                    '-vf', 'setpts=PTS/8,scale=960:-2,fps=30', '-c:v', 'libx264',
                    '-threads', '2', '-preset', 'medium', '-crf', '25', '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart', str(clip)], check=True)
    subprocess.run(['/home/limx/miniconda3/envs/RoboTwin/bin/ffmpeg', '-v', 'error', '-i', str(clip), '-f', 'null', '-'], check=True)
    subprocess.run(['/home/limx/miniconda3/envs/RoboTwin/bin/ffmpeg', '-v', 'error', '-y', '-i', str(clip), '-frames:v', '1', str(poster)], check=True)
    info = probe(clip)
    stream = next(s for s in info['streams'] if s['codec_type'] == 'video')
    seconds = float(info['format']['duration'])
    assert abs(seconds * 8 - source_seconds) < .4
    return {'name': name, 'source_url': SITE, 'download_url': url,
            'source_file': str(source), 'source_sha256': sha(source), 'file': str(clip),
            'poster': str(poster), 'start_seconds': 0, 'duration_seconds': seconds,
            'source_duration_seconds': source_seconds, 'presentation_speed': 8,
            'speed_multiplier': 1, 'audio': 'removed for narrated talk',
            'width': stream['width'], 'height': stream['height'], 'codec': stream['codec_name'],
            'pixel_format': stream['pix_fmt'], 'sha256': sha(clip), 'full_decode': 'passed',
            'source_playback': 'Complete original reset, encoded at 8x source time; player 1x.'}


with ThreadPoolExecutor(max_workers=3) as pool:
    clips = list(pool.map(prepare, [
        ('enpire_reset_pusht', 'pusht-reset-only-1.mp4'),
        ('enpire_reset_tie', 'ziptie-reset-1.mp4'),
        ('enpire_reset_gpu', 'gpu-reset-1.mp4')]))
manifest = ROOT / '.build/clip_manifest_v11.json'
manifest.write_text(json.dumps(clips, indent=2) + '\n')
files = [manifest, ROOT / 'research/sources/enpire_order_20260916/website.html',
         ROOT / 'research/sources/enpire_order_20260916/user_toc.png']
for clip in clips:
    files.extend(Path(clip[key]) for key in ('source_file', 'file', 'poster'))
pins = {'source': SITE, 'selection': 'First official reset case per task; entire original sequence.',
        'sha256': {str(f.relative_to(ROOT)): sha(f) for f in files}}
(ROOT / 'research/enpire_v0_19_sources.json').write_text(json.dumps(pins, indent=2) + '\n')
print(json.dumps([{'name': c['name'], 'seconds': c['duration_seconds']} for c in clips]))
