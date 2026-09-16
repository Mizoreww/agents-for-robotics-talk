"""Independent HTMLParser audit; no model, robot, or external code execution."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import math
import re
import statistics

ROOT = Path(__file__).resolve().parent
SOURCE_SHA256 = "50af836616bef6dfaed22e142702d37da7e5884c85954e9cb9ae3e7d685d4851"


class Episodes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.rows = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div":
            if self.depth:
                self.depth += 1
            elif "ep" in attrs.get("class", "").split():
                self.depth = 1
                self.parts = []
                self.media = []
        if self.depth and tag == "video":
            self.media.append(attrs["src"])

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "div" and self.depth:
            self.depth -= 1
            if not self.depth:
                assert len(self.media) == 1
                self.rows.append((self.media[0], " ".join(self.parts)))


def verify():
    source = (ROOT / "asim_index.html").read_bytes()
    assert hashlib.sha256(source).hexdigest() == SOURCE_SHA256
    assert source == (ROOT / "asim_index_pinned.html").read_bytes()
    parser = Episodes()
    parser.feed(source.decode())
    assert len(parser.rows) == 370
    derived = json.loads((ROOT / "asim_query_times_derived.json").read_text())
    actual = {}
    for media, body in parser.rows:
        _, run, episode = media.split("/")
        task, interface, state, model, seed, stamp = run.split("__")
        if not (stamp.startswith("20260908T") and state == "proprio"
                and model == "codex-gpt-6-astra"):
            continue
        pairs = re.findall(r"查询\s+(\d+)\s*（第\s+\d+\s+步，([\d.]+)\s+s，", body)
        declared = int(re.search(r"模型的推理轨迹（(\d+) 次查询）", body)[1])
        assert [int(pair[0]) for pair in pairs] == list(range(1, declared + 1))
        times = [float(pair[1]) for pair in pairs]
        assert all(math.isfinite(value) and value > 0 for value in times)
        key = (run, episode)
        assert key not in actual
        actual[key] = times
    assert len(actual) == 180
    assert set(Counter(run for run, _ in actual).values()) == {20}
    expected = {(row["run"], row["episode"]): row["query_seconds"]
                for row in derived["episodes"]}
    assert actual == expected
    assert derived["source_sha256"] == SOURCE_SHA256
    assert derived["source_commit"] == "1e7952c26e0a8783e4eca48514b3a1cc03e2c5df"
    for row in derived["summary"]:
        matches = [times for (run, _), times in actual.items()
                   if run.split("__")[1] == row["interface"]
                   and (row["task"] == "ALL" or run.split("__")[0] == row["task"])]
        times = [value for values in matches for value in values]
        assert row["episodes"] == len(matches)
        assert row["queries"] == len(times)
        for key, value in {"mean_s": statistics.mean(times),
                           "median_s": statistics.median(times),
                           "min_s": min(times), "max_s": max(times),
                           "sum_s": sum(times),
                           "inverse_mean_s": 1 / statistics.mean(times)}.items():
            assert math.isclose(row[key], value, rel_tol=1e-12, abs_tol=1e-9)
    assert sum(len(values) for values in actual.values()) == 731
    print("PASS: pinned source; 370 visible episodes; exact 180 selected episodes; 731 queries; 12 summaries")


if __name__ == "__main__":
    verify()
