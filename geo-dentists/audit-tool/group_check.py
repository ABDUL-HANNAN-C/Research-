"""Free checks for many practices in one city, for the price of one.

City-wide patient questions get the same answer for every practice, so this asks
each question once, checks every practice against the answers, and writes:
  - outreach/<city>/results.md      summary table for all practices
  - outreach/<city>/emails/<slug>.md a personalised first email per practice
  - outreach/<city>/answers.json     raw answers, reused on re-runs (no new API cost)

Usage:
    python group_check.py --practices practices_charlotte.csv --city "Charlotte, NC" --limit 3
"""

import argparse
import csv
import datetime
import json
import os
import re
import sys
from pathlib import Path

import anthropic

from audit import COUNTRY_CODES, ask, estimate_cost, is_mentioned, parse_recommended

ROOT = Path(__file__).resolve().parent.parent


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def first_email(practice: dict, result: dict, city: str) -> str:
    competitors = [c for c in result["recommended"] if not is_mentioned(practice["name"], "", c, [])][:3]
    named = ", ".join(f"**{c}**" for c in competitors) or "other practices"
    strength = practice.get("strength") or "a strong reputation with your patients"
    display = practice["name"].split("|")[0]
    return f"""**To:** {practice.get('email') or '(find on their website contact page)'}
**Subject:** {display} isn't showing up when patients ask AI for a dentist

Hi {practice.get('contact') or 'there'},

I asked an AI assistant a question patients in {city.split(',')[0]} are now asking every day:

> "{result['question']}"

It recommended {named}. **{display}** wasn't mentioned, even though you have {strength}.

More patients now choose a dentist this way, and AI assistants tend to name only a handful of practices, based mostly on a few directories and review sites. It's usually fixable.

I'm offering free 3-question checks to a few {city.split(',')[0]} practices. They show where you appear, who gets named instead and which sites the AI relies on. Want me to send yours? No cost, no obligation.

Best,
[Your name]
AskedFirst | AI visibility for dental practices
askedfirst.audits@gmail.com

[Your mailing address]
*Not interested? Reply "no thanks" and I won't email again.*

---
*Before sending: ask ChatGPT the same question yourself and attach a screenshot. If the practice IS named there, don't send this claim.*
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--practices", required=True, help="CSV with columns: name,domain,strength,contact,email,lead")
    parser.add_argument("--city", required=True)
    parser.add_argument("--country", choices=sorted(COUNTRY_CODES), default="us")
    parser.add_argument("--limit", type=int, default=3, help="Number of questions to ask (default 3)")
    parser.add_argument("--refresh", action="store_true", help="Ignore saved answers and ask again (costs money)")
    args = parser.parse_args()

    practices = list(csv.DictReader(open(args.practices, newline="")))
    templates = [
        line.strip() for line in Path(__file__).with_name(f"questions_{args.country}.txt").read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ][: args.limit]
    questions = [t.replace("{city}", args.city) for t in templates]

    out_dir = ROOT / "outreach" / slugify(args.city)
    (out_dir / "emails").mkdir(parents=True, exist_ok=True)
    cache_path = out_dir / "answers.json"
    cache = {} if args.refresh or not cache_path.exists() else json.loads(cache_path.read_text())

    usage = {"in": 0, "out": 0, "searches": 0}
    missing = [q for q in questions if q not in cache]
    if missing:
        api_key = os.environ.get("AUDIT_ANTHROPIC_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            sys.exit("Set AUDIT_ANTHROPIC_KEY to your Anthropic API key.")
        client = anthropic.Anthropic(api_key=api_key, base_url="https://api.anthropic.com")
        for i, q in enumerate(missing, 1):
            print(f"[{i}/{len(missing)}] {q}")
            answer, urls = ask(client, q, args.city, args.country, usage)
            cache[q] = {"answer": answer, "urls": urls, "date": str(datetime.date.today())}
            cache_path.write_text(json.dumps(cache, indent=2))
    else:
        print("All answers already saved - no API calls needed.")

    results = [{"question": q, **cache[q], "recommended": parse_recommended(cache[q]["answer"])} for q in questions]

    rows = []
    for p in practices:
        hits = [is_mentioned(p["name"], p.get("domain", ""), r["answer"], r["urls"]) for r in results]
        rows.append((p, hits))
        missed = [r for r, hit in zip(results, hits) if not hit]
        preferred = int(p.get("lead") or 0) - 1  # optional 1-based question number to lead with
        lead = results[preferred] if 0 <= preferred < len(results) and not hits[preferred] else (missed[0] if missed else None)
        if lead:
            (out_dir / "emails" / f"{slugify(p['name'].split('|')[0])}.md").write_text(first_email(p, lead, args.city))

    lines = [
        f"# Free AI checks: {args.city}",
        "",
        f"*{datetime.date.today():%d %B %Y} · {len(questions)} patient questions asked to an AI assistant with live web search. "
        "AI answers vary between assistants and over time; confirm with your own ChatGPT screenshot before quoting.*",
        "",
        "## Who the AI recommended",
        "",
        "| Question | Practices named |",
        "|---|---|",
        *[f"| {r['question']} | {', '.join(r['recommended']) or '-'} |" for r in results],
        "",
        "## Your prospects",
        "",
        "| Practice | " + " | ".join(f"Q{i}" for i in range(1, len(questions) + 1)) + " | Email drafted |",
        "|---|" + "---|" * len(questions) + "---|",
    ]
    for p, hits in rows:
        marks = " | ".join("✅" if h else "❌" for h in hits)
        lines.append(f"| {p['name'].split('|')[0]} | {marks} | {'yes' if not all(hits) else 'no - already visible'} |")
    lines += ["", "## Full answers", ""]
    for i, r in enumerate(results, 1):
        lines += [f"### Q{i}: {r['question']}", "", r["answer"], "", "Sources: " + ", ".join(r["urls"][:8]), ""]
    (out_dir / "results.md").write_text("\n".join(lines) + "\n")

    print(f"\nWrote {out_dir / 'results.md'} and {sum(not all(h) for _, h in rows)} email drafts.")
    if missing:
        print(f"Estimated API cost this run: ${estimate_cost(usage):.2f} "
              f"({usage['in']} in / {usage['out']} out tokens, {usage['searches']} searches)")


if __name__ == "__main__":
    main()
