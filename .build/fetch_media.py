"""Capture only explicitly selected public source media."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'


def fetch(item):
    name, url = item
    dest = ASSETS / name
    record = {'name': name, 'url': url, 'accessed': '2026-09-10'}
    try:
        if not dest.exists():
            temp = dest.with_suffix(dest.suffix + '.partial')
            started = time.monotonic()
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=75) as response:
                with temp.open('wb') as out:
                    while chunk := response.read(1024 * 1024):
                        out.write(chunk)
                        if out.tell() > 400 * 1024 * 1024 or time.monotonic() - started > 240:
                            raise RuntimeError('Asset exceeds bounded download budget')
            temp.replace(dest)
        record.update(status='downloaded', bytes=dest.stat().st_size,
                      sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
    except Exception as exc:
        record.update(status='unavailable', error=f'{type(exc).__name__}: {exc}')
    print(json.dumps(record), flush=True)
    return record


if __name__ == '__main__':
    jobs = json.loads((ROOT / 'asset_requests.json').read_text())
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(fetch, jobs.items()))
    (ROOT / 'media_downloads.json').write_text(json.dumps(results, indent=2))
