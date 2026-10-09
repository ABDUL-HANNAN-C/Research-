# AskedFirst: AI Visibility Audits for Dental Practices

A ready-to-launch kit for Pick 1 from `../2027-opportunities-research.md`.

| Folder / file | What it is |
|---|---|
| `market-targeting.md` | Which countries and cities to target, in what order, with local pricing |
| `demand-validation.md` | Why dentists, the competition, risks, and a 2-week validation plan with success criteria |
| `landing-page/index.html` | Single-file landing page with pricing, FAQ and a free-check signup form |
| `audit-tool/audit.py` | Runs the audit: asks Claude (with live web search) real patient questions and writes a Markdown report |
| `audit-tool/questions_{us,ca,au,uk}.txt` | 20 patient questions per country (`{city}` is filled in automatically). Swap these to target another niche |

## 1. Run an audit

```bash
cd audit-tool
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...        # from console.anthropic.com
python audit.py --practice "Smile Dental Studio" --domain smiledentalstudio.com \
    --city "Austin, TX" --limit 3          # free check: 3 questions
python audit.py --practice "Smile Dental Studio" --domain smiledentalstudio.com \
    --city "Austin, TX"                    # full audit: all 20
python audit.py --practice "Maple Dental" --city "Toronto" --country ca   # uk | ca | au | us
```

The report is saved to `audit-tool/reports/<practice>.md`. **Always read it before sending.** Edit the "next steps" section to fit the findings.

Cost: roughly a few cents to about $0.30 per question (model plus web searches). Check your usage in the Anthropic Console after the first run.

## 2. Publish the landing page

1. Create a free form at [formspree.io](https://formspree.io) (or Tally) and replace `YOUR_FORM_ID` in `index.html`.
2. Deploy the `landing-page/` folder for free on Netlify Drop, Cloudflare Pages or GitHub Pages.
3. Optional: buy a domain (~$10/yr) and add a Stripe Payment Link for the $149 audit.

## 3. What only you can do
- Own the accounts (Stripe, domain, email, Anthropic API key)
- Send the outreach emails and talk to dentists
- Approve each report before it goes out
