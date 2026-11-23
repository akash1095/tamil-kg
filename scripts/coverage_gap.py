"""Run coverage_gap.sparql against Wikidata and write one JSONL line per relation.

Usage:
    python scripts/coverage_gap.py
    python scripts/coverage_gap.py --out results/coverage/coverage_gap.jsonl

In:  scripts/coverage_gap.sparql
Out: results/coverage/coverage_gap.jsonl  (one line per relation + one summary line)
     data/cache/coverage_raw_<date>.json  (raw SPARQL responses)
Copy the query date it prints into run_log.md.
"""
import argparse
import datetime as dt
import json
import re
import time
from pathlib import Path

import requests

ENDPOINT = "https://query.wikidata.org/sparql"
# Wikimedia asks for a descriptive User-Agent. Keep it anonymous for review.
HEADERS = {
    "User-Agent": "spelll2027-tamil-kg/0.1 (academic research; anonymous submission)",
    "Accept": "application/sparql-results+json",
}
RELATIONS = {
    "P19": "place of birth", "P20": "place of death",
    "P569": "date of birth", "P570": "date of death",
    "P106": "occupation", "P69": "educated at",
    "P166": "award received", "P102": "political party",
}
LITERAL = {"P569", "P570"}  # year-valued: label counts not meaningful

ROOT = Path(__file__).resolve().parent.parent


def load_queries(path):
    blocks, name = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"#---\s*query:\s*(\w+)", line)
        if m:
            name = m.group(1)
            blocks[name] = []
        elif name:
            blocks[name].append(line)
    return {k: "\n".join(v).strip() for k, v in blocks.items()}


def run(query, retries=3):
    for attempt in range(retries):
        r = requests.get(ENDPOINT, params={"query": query}, headers=HEADERS, timeout=90)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(10 * (attempt + 1))
            continue
        r.raise_for_status()
    raise RuntimeError(f"query failed after {retries} tries (last status {r.status_code})")


def value(binding, key):
    return int(binding[key]["value"]) if key in binding else 0


def pct(a, b):
    return round(100.0 * a / b, 1) if b else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sparql", default=str(ROOT / "scripts" / "coverage_gap.sparql"))
    ap.add_argument("--out", default=str(ROOT / "results" / "coverage" / "coverage_gap.jsonl"))
    args = ap.parse_args()

    queries = load_queries(Path(args.sparql))
    today = dt.date.today().isoformat()
    raw = {}

    people_res = run(queries["people"])
    raw["people"] = people_res
    n_people = value(people_res["results"]["bindings"][0], "people")
    print(f"Humans with a Tamil Wikipedia article: {n_people}")

    rows = []
    for pid, name in RELATIONS.items():
        q = re.sub(r"VALUES \?prop \{[^}]*\}", f"VALUES ?prop {{ wdt:{pid} }}", queries["relation"])
        res = run(q)
        raw[pid] = res
        b = res["results"]["bindings"][0] if res["results"]["bindings"] else {}
        with_prop, vals = value(b, "people_with_prop"), value(b, "values")
        ta, en = value(b, "values_with_ta_label"), value(b, "values_with_en_label")
        row = {
            "relation": pid, "name": name, "query_date": today,
            "people_total": n_people,
            "people_with_prop": with_prop,
            "pct_people_with_prop": pct(with_prop, n_people),
            "values": vals,
        }
        if pid not in LITERAL:
            row.update({
                "values_with_ta_label": ta, "pct_values_ta_label": pct(ta, vals),
                "values_with_en_label": en, "pct_values_en_label": pct(en, vals),
            })
        rows.append(row)
        print(json.dumps(row, ensure_ascii=False))
        time.sleep(2)  # be polite to WDQS

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.write(json.dumps({"summary": True, "query_date": today, "people_total": n_people},
                           ensure_ascii=False) + "\n")

    cache = ROOT / "data" / "cache" / f"coverage_raw_{today}.json"
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out}\nQuery date: {today}  <- copy into run_log.md")


if __name__ == "__main__":
    main()
