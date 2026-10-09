# Market Targeting: USA plus English-Speaking Countries

*October 2026*

## Recommendation in one line

**Start in the USA only, in 3 fast-growing metros. Add Canada, Australia and the UK one at a time, and only after the first 3–5 paying US customers.** Expanding to four countries at once spreads your outreach too thin, and each country's patients ask different questions.

## Why the USA first

- **Biggest market and highest prices:** about 200k dental practices, and practices already pay $1k–$5k/mo to marketing agencies, so $149 or $299/mo is an easy yes.
- **Highest AI-search adoption:** Google AI Overviews and ChatGPT search are most widespread in the US.
- **Same pitch everywhere:** one landing page and one question set, priced in USD.

## Which US cities, and why fast-growing ones

**New residents need a new dentist, and new residents are the people most likely to ask AI** ("best dentist near me, just moved to Charlotte"). Fast-growing metros also get many newly opened practices with few reviews, which have the most to gain.

| Metro | Why | Suggested test areas |
|---|---|---|
| **Charlotte, NC** | Added ~278k people from 2020 to 2025, 7th fastest-growing US metro | Charlotte, Matthews, Huntersville, Fort Mill SC |
| **Dallas–Fort Worth, TX** | +~124k in 2025 alone, growth concentrated in the suburbs | Frisco, McKinney, Prosper, Celina |
| **Houston, TX** | Largest numeric gain in 2025 (+~127k) | Katy, Cypress, Sugar Land, The Woodlands |
| Backups | Fastest % growth | Ocala FL, Myrtle Beach SC, St. George UT, Atlanta suburbs |

**Pick one metro first** (Charlotte is a good start: big enough, not as saturated as DFW). Run 10 free checks there, then move to the next.

**Who to target in each city:** independent practices, not DSO chains such as Aspen or Heartland, because those have corporate marketing teams. The best prospects:
- 4.5★+ on Google but **missing from AI answers** (good practice, invisible: an easy story to sell)
- practices that opened recently
- practices offering high-value services: implants, Invisalign, sedation, cosmetic

## Expansion order after the US

| Order | Country | Why it's attractive | The angle (the question patients ask AI) | Suggested pricing |
|---|---|---|---|---|
| 2 | **Canada** | The Canadian Dental Care Plan now covers **6.5M+ people**. Many are looking for a participating dentist for the first time | "Which dentists in Toronto accept CDCP?" | CA$199 audit · CA$399/mo |
| 3 | **Australia** | Private-pay heavy market with strong spending on health-fund-covered dental | "No-gap check-up with my health fund", "bulk bill Child Dental Benefits Schedule" | A$229 audit · A$449/mo |
| 4 | **UK** | Severe NHS access shortage (around 9 in 10 practices weren't taking new NHS patients in BDA/BBC research), which pushes patients to search for private dentists | "Can't find an NHS dentist in Bristol, which private dentist?", "dental plan", "composite bonding" | £119 audit · £249/mo |
| Skip for now | Ireland, New Zealand | Small markets | — | — |

Question sets for each country are ready in `audit-tool/questions_{us,ca,au,uk}.txt`. Run with `--country ca` and so on.

**Notes:**
- In the UK and Australia, health-service advertising has rules (GDC and AHPRA guidance, for example on testimonials and claims). The audit itself is fine, but check those rules before writing marketing content for clinics there.
- Use local spelling and terms on country pages: "practice" and "clinic", "Invisalign" (universal), "bulk bill" (AU), "hygienist" (UK).

## 90-day plan

| Weeks | Goal |
|---|---|
| 1–2 | Charlotte: 10 free checks → personalised emails → **3 paid audits** |
| 3–6 | Add DFW suburbs and Houston suburbs. Convert audit buyers to the $299/mo plan. Write 1 anonymised case study (with permission) |
| 7–10 | If US has ≥5 paying customers: launch Canada (Toronto, Calgary, Vancouver suburbs) with the CDCP angle |
| 11–13 | Australia (Brisbane, Perth suburbs), then the UK |

## Sources
- [Census Bureau: metro growth story (May 2026)](https://www.census.gov/library/stories/2026/05/major-city-outer-edge-growth.html) · [RealPage: fastest growing metros 2025](https://www.realpage.com/analytics/population-growth-markets-2025/) · [WSOC: Charlotte top-10 growth](https://www.wsoctv.com/news/local/one-americas-fastestgrowing-metros-charlotte-lands-top-10/PGS3WDVAGRDSDLJQTZIQ4UA2DA) · [Atlanta Regional Commission](https://33n.atlantaregional.com/population/the-metro-shuffle-winners-and-losers-in-2025-population-growth)
- [Health Canada: 6.5M+ can use CDCP (April 2026)](https://www.canada.ca/en/health-canada/news/2026/04/more-than-65-million-canadians-can-now-receive-services-under-the-canadian-dental-care-plan.html)
- [Australian Dept of Health: CDBS](https://www.health.gov.au/our-work/child-dental-benefits-schedule) · [ADA: CDBS cap 2026–27](https://ada.org.au/cdbs-benefits-cap-to-increase-to-1-158-for-2026-2027)
- [NationalWorld: NHS dentist access](https://www.nationalworld.com/health/nhs-dentist-how-many-dentists-are-accepting-nhs-patients-near-me-4726893)
