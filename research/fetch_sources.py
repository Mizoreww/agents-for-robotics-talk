"""Internal read-only public-source capture for the survey (stdlib only)."""
import concurrent.futures
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urljoin
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent / "sources"


class Capture(HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.parts = []
        self.links = []
        self.media = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style", "noscript"}:
            self.skip += 1
        if self.skip:
            return
        if tag in {"p", "div", "section", "article", "li", "tr", "br", "figure"} or re.fullmatch(r"h[1-6]", tag):
            self.parts.append("\n")
        if attrs.get("id"):
            self.parts.append(" [#" + attrs["id"] + "] ")
        if tag == "a" and attrs.get("href"):
            self.links.append(urljoin(self.base, attrs["href"]))
        if tag in {"img", "video", "source", "iframe"}:
            self.media.append({"tag": tag, **{k: urljoin(self.base, v) if k in {"src", "poster"} else v for k, v in attrs.items() if k in {"src", "poster", "alt", "type"}}})

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"} and self.skip:
            self.skip -= 1
        elif not self.skip and (tag in {"p", "li", "tr", "section", "figure"} or re.fullmatch(r"h[1-6]", tag)):
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def capture(item):
    key, url = item
    try:
        with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=50) as response:
            raw = response.read()
            final_url = response.url
        ROOT.mkdir(parents=True, exist_ok=True)
        (ROOT / f"{key}.html").write_bytes(raw)
        parser = Capture(final_url)
        parser.feed(raw.decode("utf-8", "replace"))
        lines = [re.sub(r"\s+", " ", line).strip() for line in "".join(parser.parts).splitlines()]
        text = "\n".join(line for line in lines if line)
        (ROOT / f"{key}.txt").write_text(text)
        record = {"key": key, "url": url, "final_url": final_url, "accessed": "2026-09-10", "sha256": hashlib.sha256(raw).hexdigest(), "chars": len(text), "links": list(dict.fromkeys(parser.links)), "media": parser.media}
        (ROOT / f"{key}.metadata.json").write_text(json.dumps(record, ensure_ascii=False, indent=2))
        return {"key": key, "chars": len(text), "media": len(parser.media), "url": final_url}
    except Exception as exc:
        return {"key": key, "url": url, "error": type(exc).__name__ + ": " + str(exc)}


if __name__ == "__main__":
    jobs = json.loads(Path(sys.argv[1]).read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(capture, jobs.items()):
            print(json.dumps(result, ensure_ascii=False), flush=True)
