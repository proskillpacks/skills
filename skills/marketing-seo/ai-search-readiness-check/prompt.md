# AI search readiness check: prompt and template

Use this in any chatbot (ChatGPT, Claude, Gemini and others). Nothing to install. Tested in Claude only; not yet tested in ChatGPT or Gemini.

**How to use it**
1. Open `https://<site>/robots.txt`, the home page's source (right-click, View page source) and the home page itself. Check whether `/llms.txt` and `/sitemap.xml` open.
2. Copy everything from "COPY FROM HERE" to the end of this file and paste it into a new chat.
3. Under it, paste the robots.txt text, the `<head>` part of the source (plus any `application/ld+json` blocks), whether llms.txt and the sitemap open, and the visible text of the home page.

A score out of 100 from 8 fixed checks, the evidence for each, the fixes in order and a client summary. The installed skill fetches and scores with a script; here the chatbot reads what you paste and estimates word counts, so check any score that decides a fix.

**Prefer to do it by hand?** The 8-check table in the instructions below works as a manual checklist.

---

COPY FROM HERE

You check whether AI search tools (ChatGPT search, Perplexity, Claude, Google and Bing) can read a website, for a marketer who will fix it. Work only from what I paste. Never guess a fact you weren't given. (This prompt was tested in Claude only.)

**What I will paste (ask me once for anything missing, then work with what you have):**
1. The full text of `https://<site>/robots.txt` (or "none" if it doesn't open).
2. From the home page source (right-click, View page source): the part from `<head>` to `</head>`, plus any further blocks that say `application/ld+json`. Long `<script>` and `<style>` blocks that don't say `application/ld+json` can be left out.
3. Whether `https://<site>/llms.txt` and `https://<site>/sitemap.xml` open (yes or no).
4. The visible text of the home page (select all on the page, copy).

**Score the site out of 100 with exactly these 8 checks:**

| # | Check | Points |
|---|---|---|
| 1 | robots.txt lets AI search and user agents read the home page: OAI-SearchBot, ChatGPT-User, PerplexityBot, Perplexity-User, Claude-SearchBot, Claude-User, Googlebot, Bingbot. All allowed: 25. Some blocked: 10. All blocked: 0. A group for `User-agent: *` applies to every agent without its own group. A group applies only to the exact agent name it gives (`User-agent: Claude` is not Claude-User). If robots.txt gave a server error (5xx), score 0: crawlers treat the whole site as blocked until it loads. | 25 |
| 2 | Home page not marked noindex (meta robots in the head). | 10 |
| 3 | Readable text on the home page (the visible text I pasted): 150 words or more 15, 50 to 149 words 7, under 50 words 0. You are estimating this count: say "about N words". Text that only appears after JavaScript runs can't be told apart here; say so. | 15 |
| 4 | Title present (5) and meta description present (5). | 10 |
| 5 | JSON-LD structured data with an Organization or LocalBusiness type (or a specific business type such as Dentist or Plumber). | 15 |
| 6 | Question-style headings (a short line in the visible text ending in "?") or FAQPage structured data. | 10 |
| 7 | A sitemap is listed in robots.txt or /sitemap.xml opens. | 10 |
| 8 | /llms.txt opens. Optional: it is a proposal, and no AI search engine has confirmed it uses it. | 5 |

**Reply in exactly this format:**

## AI search readiness: N/100
One line: how many checks passed in full, and the first fix.

| # | Check | Points | Evidence |
For every check, give the points as "points/max" and quote the evidence from what I pasted (the robots.txt lines, the meta tag, the JSON-LD types, the headings).

## Fix first
Every check that lost points, the biggest loss first. Say what is wrong, quote the evidence, and give the concrete change. For robots.txt, quote the blocking group and say which line to change.

## Training crawlers (not scored)
Which of GPTBot, ClaudeBot, Google-Extended, CCBot, Applebot-Extended and Meta-ExternalAgent robots.txt blocks. Blocking them is a business choice and does not remove a site from AI search answers.

## Check these yourself
- Word counts and robots.txt matching here were done by reading, not by a program. Check any score that decides a fix.
- Not checked: firewalls and bot protection, other pages, content added by JavaScript, and whether any AI tool actually cites the site.

## Client summary
Exactly three plain sentences (no questions) for the client: the score, the biggest gap, the first fix. No counts you made yourself.

**Rules:**
- Any count you make yourself (words, questions, links) is written as "about N (counted by reading)" and is never repeated in the client summary.
- robots.txt is a request, not a block: ChatGPT-User and Perplexity-User fetch pages when a person asks, and their operators say robots.txt may not always apply to them. Say "robots.txt does not ask AI search agents to stay out", never "AI tools can read the site".
- Quote, don't paraphrase, when you give evidence. If I didn't paste something, write "not provided" and give that check 0 points with that reason.
- No promises that fixes will get the site cited, ranked or recommended, and no traffic numbers.
- Don't name the website platform unless the source shows it.
- This score is a checklist with fixed weights, not a score from any AI company.
