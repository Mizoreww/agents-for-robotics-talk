"""Static print-engine layout check; not a browser or video-playback audit."""
from pathlib import Path
import hashlib
import html
import json
import re

from weasyprint import HTML

root = Path('/home/limx/Desktop/agent_for_robotics')
source = root / 'output/Agents_for_Robotics_Self_Contained.html'
raw = source.read_text()
deck = json.loads(re.search(r'<script type="application/json" id="deck-data">(.*?)</script>', raw, re.S).group(1))
styles = re.search(r'<style>(.*?)</style>', raw, re.S).group(1)
styles += '''
@page { size: 1280px 720px; margin: 0; }
html, body { margin: 0; padding: 0; background: white; min-height: 0; }
.canvas { position: relative; width: 1280px; height: 720px; transform: none;
          break-after: page; overflow: hidden; }
.canvas:last-child { break-after: auto; }
'''
defs = '<svg width="0" height="0" aria-hidden="true"><defs>'
for name, color in [('gray', '#646464'), ('teal', '#2ba39b')]:
    defs += f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{color}"/></marker>'
defs += '</defs></svg>'

def asset_url(key):
    asset = deck['assets'][key]
    return f'data:{asset["mime"]};base64,{asset["data"]}'

pages = []
for slide in deck['slides']:
    content = re.sub(r'data-asset="([a-f0-9]+)"', lambda match: f'src="{asset_url(match[1])}"', slide['html'])
    # The print engine renders each SVG independently; repeat the identical
    # marker definitions locally instead of relying on browser-wide SVG IDs.
    local_defs = defs.split('<defs>', 1)[1].split('</defs>', 1)[0]
    content = content.replace('viewBox="0 0 1280 720" aria-hidden="true">', 'viewBox="0 0 1280 720" aria-hidden="true"><defs>' + local_defs + '</defs>')
    for media in deck['media']:
        if media['slide'] == slide['number']:
            bbox = ';'.join(f'{css}:{media[key]}px' for css, key in [('left', 'x'), ('top', 'y'), ('width', 'w'), ('height', 'h')])
            content += f'<img class="art" style="{bbox}" src="{asset_url(media["posterKey"])}" alt="Video poster: {html.escape(media["name"])}">'
    content += f'<div class="footer">{html.escape(slide["footer"])}</div><div class="page-no">{slide["number"]}</div>'
    pages.append('<article class="canvas">' + defs + content + '</article>')
document = HTML(string='<!doctype html><html><head><meta charset="utf-8"><style>' + styles + '</style></head><body>' + ''.join(pages) + '</body></html>').render()
assert len(document.pages) == 28, len(document.pages)
destination = root / '.build/three_parts_static_preview.pdf'
document.write_pdf(destination)
report = {
    'html_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'engine': 'WeasyPrint static paged layout; videos represented by exact embedded posters',
    'page_count': len(document.pages),
    'browser_interaction_checked': False,
    'pdf': str(destination),
}
(root / '.build/three_parts_static_render_audit.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
