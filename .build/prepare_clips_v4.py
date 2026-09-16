"""Download cited public media for the approved offline talk and prepare bounded clips.

Source originals are kept intact; only separate presentation clips are encoded.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import subprocess
import urllib.request

B = Path('/home/limx/Desktop/agent_for_robotics/.build')
A = B / 'assets/v0_8'
FF = '/home/limx/miniconda3/envs/RoboTwin/bin/ffmpeg'
FP = '/home/limx/miniconda3/envs/RoboTwin/bin/ffprobe'
JOBS = [
    ('office_newton', 'https://video.twimg.com/amplify_video/2098439638574870528/vid/avc1/1280x720/jtX8iCLebZux4cuq.mp4?tag=29', 'https://x.com/Jiarui_X/status/2098439950991806804', 0, 25, 'Source speed unspecified; scene-output excerpt'),
    ('quad_rl', 'https://video.twimg.com/amplify_video/2098297480752607232/vid/avc1/1440x1200/fDFQ9O6Z9JvGebZx.mp4?tag=29', 'https://x.com/gclue_akira/status/2098300921658868185', 0, 14, 'Source labels 50 fps real time; Wave/Sit partial cycles CUT'),
    ('keyboard', 'https://video.twimg.com/amplify_video/2098821014465519616/vid/avc1/1920x1080/IP4sVHPj3QwCbR61.mp4?tag=29', 'https://x.com/kaiwynd/status/2098823484474348008', 55, 26, '20× source playback; selected feedback/correction excerpt'),
    ('asim_delta', 'https://asimfish.github.io/astra-control-dashboard/media/Square__delta__proprio__codex-gpt-6-astra__s0__20260908T131857Z/ep00.mp4', 'https://asimfish.github.io/astra-control-dashboard/#sec4', 0, 10.2, 'Simulation replay; model waiting omitted'),
    ('asim_waypoint', 'https://asimfish.github.io/astra-control-dashboard/media/Square__waypoint__proprio__codex-gpt-6-astra__s0__20260908T132052Z/ep00.mp4', 'https://asimfish.github.io/astra-control-dashboard/#sec4', 0, 17.3, 'Simulation replay; model waiting omitted'),
]


def prepare(job):
    name, url, source, start, length, speed = job
    src = A / f'{name}_source.mp4'
    if not src.exists():
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request, timeout=120) as response:
            data = response.read()
        assert b'ftyp' in data[:64], name
        temporary = src.with_suffix('.part')
        temporary.write_bytes(data)
        temporary.replace(src)
    dest, poster = B / 'clips' / f'{name}.mp4', A / f'{name}.jpg'
    subprocess.run([FF, '-y', '-v', 'error', '-ss', str(start), '-i', str(src), '-t', str(length), '-vf', "scale=w='min(1280,iw)':h='min(720,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2", '-c:v', 'libx264', '-crf', '20', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-an', '-movflags', '+faststart', '-threads', '2', str(dest)], check=True)
    subprocess.run([FF, '-v', 'error', '-i', str(dest), '-f', 'null', '-'], check=True)
    info = json.loads(subprocess.check_output([FP, '-v', 'error', '-show_entries', 'format=duration:stream=width,height,codec_name,pix_fmt', '-of', 'json', str(dest)]))
    stream = info['streams'][0]
    subprocess.run([FF, '-y', '-v', 'error', '-ss', '1', '-i', str(dest), '-frames:v', '1', str(poster)], check=True)
    return dict(name=name, source_url=source, download_url=url, source_file=str(src), source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(), source_playback=speed, file=str(dest), poster=str(poster), start_seconds=start, duration_seconds=float(info['format']['duration']), speed_multiplier=1, audio='removed for narrated talk', width=stream['width'], height=stream['height'], codec=stream['codec_name'], pixel_format=stream['pix_fmt'], sha256=hashlib.sha256(dest.read_bytes()).hexdigest(), full_decode='passed')


if __name__ == '__main__':
    A.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(prepare, JOBS))
    (B / 'clip_manifest_v4.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
    print([(r['name'], r['duration_seconds']) for r in records])
