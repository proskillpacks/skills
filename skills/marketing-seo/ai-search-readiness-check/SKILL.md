---
name: ai-search-readiness-check
description: Checks whether AI search tools such as ChatGPT search, Perplexity, Claude and Google can read a website, and returns a 0-100 score from 8 checks with the evidence for each, then a fix list in order of points lost. It reads robots.txt rules for AI search agents (and lists training crawlers separately, unscored), noindex, the text in the server-rendered home page, title and meta description, Organization or LocalBusiness structured data, question-style content, the sitemap and llms.txt. A script does the fetching and scoring, so the same site gets the same score. Use when the user says "can ChatGPT find my site", "is my site ready for AI search", "AI search readiness", "check if AI can read my website", "are we blocking AI crawlers", "GEO audit", "AEO check", or gives a website URL and asks about AI search or AI visibility.
---

# AI Search Readiness Check

Tell a marketer, in one pass, whether AI search tools can read a client's site and what to fix first. Done means a score anyone can reproduce, evidence for every check, and fixes they can act on today.

## Input
- **Required:** a website URL (the home page is checked).
- Don't ask for anything else.

## Step 1: Run the script
Run `python3 <skill>/scripts/site_check.py ai <url>` (the script is in this skill's `scripts/` folder; use its full path). It fetches robots.txt, the home page, /llms.txt and the sitemap, politely and as itself, and prints JSON: `score`, `checks` (id, check, max, points, evidence), `fix_order`, `ai_search_agents`, `ai_training_crawlers`.

If the home page could not be fetched (`home_status` not 200, or `fetch_error`), say so with the status, give no score, and stop. If robots.txt blocks our own checker (`score` is null), say that the site asks automated readers to stay out and give no score. If the output still lists `ai_search_agents`, report which AI search agents and training crawlers robots.txt blocks (that comes from robots.txt alone), then stop. If the output has a `finding` (robots.txt returned a server error), report it as the main problem: crawlers that follow the robots.txt standard treat the whole site as blocked until robots.txt loads.

If the script can't reach the site at all (a network error or an unreadable response such as a content encoding it cannot decode, not an HTTP status), say so and offer the prompt version instead: the user pastes the page source and robots.txt into it.

## Step 2: Write the report
Use exactly this structure. Copy every number, status and evidence string from the script; never estimate or recount one, and don't comment on the script's output format.

```
## AI search readiness: <score>/100
<one line: "<checks_passed_in_full> of <checks_total> checks passed in full" copied from the script, and the first fix with its points>

| # | Check | Points | Evidence |
|---|---|---|---|
<all 8 checks in the script's order, points as "<points>/<max>", evidence copied>

## Fix first
1. <the check with the most points lost: what is wrong, quoting the evidence, and the concrete change>
<every check that lost points, in the script's fix_order>

## Training crawlers (not scored)
<one line: which of GPTBot, ClaudeBot, Google-Extended, CCBot, Applebot-Extended, Meta-ExternalAgent are blocked, from ai_training_crawlers. Blocking them is a business choice and does not remove a site from AI search answers.>

## Not checked
- Firewalls and bot-protection services, which can block AI agents even when robots.txt allows them.
- Pages other than the home page, and content that only appears after JavaScript runs.
- Whether any AI tool actually cites the site. No tool can promise that.

## Client summary
<exactly three plain sentences a marketer can paste into an email to the client: the score, the biggest gap, the first fix>
```

## How to write the fixes
- **robots.txt blocks an AI search agent:** quote the blocking `User-agent` group and say which line to remove or change. Name only agents the script listed as blocked.
- **What robots.txt can show:** it is a request, not a block. ChatGPT-User and Perplexity-User fetch pages when a person asks, and their operators say robots.txt may not always apply to those fetches. Say "robots.txt does not ask AI search agents to stay out", never "AI tools can read the site".
- **`content_signal_lines`** (for example `Content-Signal: ai-input=no`): if present, quote them in one line under the table as unscored information. The convention is new and not every AI company says it follows it.
- **noindex:** quote the meta robots or X-Robots-Tag value and say it tells all search engines to leave the page out.
- **Little server text:** say the home page shows N words before JavaScript runs, so readers that don't run JavaScript see little. Suggest server-rendered text describing what the business does, for whom and where. Don't claim to know which AI tools run JavaScript.
- **Missing title or description:** say which is missing. Don't write new ones; that's the page fix sheet's job. You may say a rewrite needs the page's own facts.
- **Structured data types:** the script counts schema.org Organization and all its subtypes (Dentist, Plumber, VeterinaryCare and so on). Name the type exactly as the script prints it, and don't say which parent type it belongs to.
- **No Organization or LocalBusiness structured data:** say what it is for in one line (it states who the business is in a form machines read) and that it must use the business's real name, address and phone.
- **No question-style content:** suggest an FAQ section built from questions the business really gets, and FAQPage structured data only if the page shows those questions and answers.
- **No sitemap / no llms.txt:** a sitemap helps every crawler find pages. llms.txt is optional: it is a proposal, and no AI search engine has confirmed it uses it. Say so plainly; never rank it above the other fixes.

## Rules (non-negotiable)
- **Read the site only through `site_check.py`.** Don't fetch pages any other way: no curl, no built-in web-fetch tool, no code of your own and no browser user agent. If a fact isn't in the script's output, write "not found by the checker" and add a `[CONFIRM: ...]` line.
- **Numbers come from the script.** Score, points, word counts and agent names are copied. No percentages or benchmarks of other sites.
- **No promises.** Never say fixes will get the site cited, ranked or recommended by AI tools, or name a traffic effect.
- **Don't guess the platform.** Name the CMS only if the evidence shows it (a "/wp-" path, a "Shopify" string).
- **The score is our checklist, with our own weights.** Say so once if asked what it means. It is not a score from any AI company.
- **Never say you checked something the script didn't** (rendering, other pages, firewalls, live citations).

## Self-check (before output)
- [ ] All 8 checks in the script's order, numbers copied exactly.
- [ ] Fixes in the script's fix_order, each with the quoted evidence.
- [ ] llms.txt described as optional and unconfirmed; training crawlers unscored.
- [ ] No promise of AI visibility, rankings or traffic.
- [ ] Client summary is exactly three sentences, and claims no more than the checks show.
- [ ] Every fact came from the script's output; nothing was fetched another way.
- [ ] Never mention the skill, its rules or the script in the client-facing output.
