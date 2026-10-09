"""AI Visibility Audit for dental practices.

Asks Claude (with live web search) the questions real patients ask, then checks
whether the practice is mentioned or recommended, and which competitors are.
Writes a Markdown report you can review and send to the client.

Usage:
    python audit.py --practice "Smile Dental Studio" --domain smiledentalstudio.com \
        --city "Austin, TX" [--country us|uk|ca|au] [--limit 5]
"""

import argparse
import datetime
import re
from pathlib import Path

import anthropic

MODEL = "claude-opus-5-5"
MAX_CONTINUATIONS = 5

SYSTEM = (
    "You are answering as a helpful AI assistant would for a member of the public "
    "looking for a dentist. Use web search to give a genuine, current answer with "
    "specific practice names. Do not favour any practice. At the very end of your "
    "answer add one line in exactly this format:\n"
    "RECOMMENDED: <practice name 1>; <practice name 2>; ...\n"
    "listing every dental practice you named, in the order you named them."
)


COUNTRY_CODES = {"us": "US", "uk": "GB", "ca": "CA", "au": "AU"}


def ask(client: anthropic.Anthropic, question: str, city: str, country: str) -> tuple[str, list[str]]:
    """Return (answer_text, cited_urls) for one patient question."""
    messages = [{"role": "user", "content": question}]
    tools = [{
        "type": "web_search_20260209",
        "name": "web_search",
        "max_uses": 5,
        "user_location": {
            "type": "approximate",
            "city": city.split(",")[0].strip(),
            "country": COUNTRY_CODES[country],
        },
    }]

    for _ in range(MAX_CONTINUATIONS):
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM,
            tools=tools,
            messages=messages,
            output_config={"effort": "medium"},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
        if response.stop_reason == "pause_turn":
            # Server-side search loop paused; resend so it resumes where it left off.
            messages.append({"role": "assistant", "content": response.content})
            continue
        break

    if response.stop_reason == "refusal":
        return "(model declined to answer)", []

    text_parts, urls = [], []
    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)
            for citation in getattr(block, "citations", None) or []:
                url = getattr(citation, "url", None)
                if url and url not in urls:
                    urls.append(url)
    return "".join(text_parts).strip(), urls


def parse_recommended(answer: str) -> list[str]:
    match = re.search(r"RECOMMENDED:\s*(.+)", answer)
    if not match:
        return []
    return [name.strip() for name in match.group(1).split(";") if name.strip()]


def is_mentioned(practice: str, domain: str, answer: str, urls: list[str]) -> bool:
    haystack = answer.lower()
    if practice.lower() in haystack:
        return True
    domain = domain.lower().removeprefix("www.")
    return bool(domain) and (domain in haystack or any(domain in u.lower() for u in urls))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--practice", required=True, help="Practice name as patients know it")
    parser.add_argument("--domain", default="", help="Practice website domain")
    parser.add_argument("--city", required=True, help='e.g. "Austin, TX"')
    parser.add_argument("--country", choices=sorted(COUNTRY_CODES), default="us")
    parser.add_argument("--questions", default="", help="Question file (default: questions_<country>.txt)")
    parser.add_argument("--limit", type=int, default=0, help="Only ask the first N questions")
    parser.add_argument("--out", default="", help="Report path (default: reports/<practice>.md)")
    args = parser.parse_args()

    questions_path = Path(args.questions) if args.questions else Path(__file__).with_name(f"questions_{args.country}.txt")
    templates = [
        line.strip() for line in questions_path.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if args.limit:
        templates = templates[: args.limit]
    questions = [t.replace("{city}", args.city) for t in templates]

    client = anthropic.Anthropic()
    results = []
    competitor_counts: dict[str, int] = {}

    for i, question in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] {question}")
        answer, urls = ask(client, question, args.city, args.country)
        recommended = parse_recommended(answer)
        mentioned = is_mentioned(args.practice, args.domain, answer, urls)
        for name in recommended:
            if args.practice.lower() not in name.lower():
                competitor_counts[name] = competitor_counts.get(name, 0) + 1
        results.append({
            "question": question, "answer": answer, "urls": urls,
            "recommended": recommended, "mentioned": mentioned,
        })

    hits = sum(r["mentioned"] for r in results)
    score = round(100 * hits / len(results)) if results else 0
    top_competitors = sorted(competitor_counts.items(), key=lambda kv: -kv[1])[:10]
    sources: dict[str, int] = {}
    for r in results:
        for u in r["urls"]:
            host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
            sources[host] = sources.get(host, 0) + 1
    top_sources = sorted(sources.items(), key=lambda kv: -kv[1])[:10]

    lines = [
        f"# AI Visibility Audit: {args.practice}",
        "",
        f"*{args.city} · {datetime.date.today():%d %B %Y} · {len(results)} patient questions asked to an AI assistant with live web search*",
        "",
        "## Summary",
        "",
        f"- **AI visibility score: {score}%.** Mentioned in {hits} of {len(results)} answers.",
        "- Note: AI answers change over time and differ between assistants. This is a snapshot, not a ranking guarantee.",
        "",
        "## Competitors recommended instead",
        "",
        "| Practice | Times recommended |",
        "|---|---|",
        *[f"| {name} | {count} |" for name, count in top_competitors],
        "",
        "## Sources the AI relied on",
        "",
        "Being listed accurately on these sites is the most direct way to improve visibility.",
        "",
        "| Website | Times cited |",
        "|---|---|",
        *[f"| {host} | {count} |" for host, count in top_sources],
        "",
        "## Question-by-question results",
        "",
    ]
    for r in results:
        status = "✅ Mentioned" if r["mentioned"] else "❌ Not mentioned"
        lines += [
            f"### {r['question']}",
            f"**{status}** · Recommended: {', '.join(r['recommended']) or 'none named'}",
            "",
            "<details><summary>Full AI answer</summary>",
            "",
            r["answer"],
            "",
            "</details>",
            "",
        ]
    lines += [
        "## Recommended next steps",
        "",
        "*(Reviewer: tailor these to the findings above before sending.)*",
        "",
        "1. Claim and complete profiles on the top cited sources above (Google Business Profile, Healthgrades, Zocdoc, Yelp…), with identical name, address, phone and hours.",
        "2. Add plain-language pages answering the exact questions where you were missing (e.g. emergency hours, insurance accepted, costs, sedation, children).",
        "3. Ask happy patients for reviews on the platforms the AI cites most.",
        "4. Make your homepage state clearly what you offer, where and for whom.",
        "5. Re-run this audit monthly to track progress.",
    ]

    slug = re.sub(r"[^a-z0-9]+", "-", args.practice.lower()).strip("-")
    out = Path(args.out) if args.out else Path(__file__).with_name("reports") / f"{slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    print(f"\nScore {score}% - report written to {out}")


if __name__ == "__main__":
    main()
