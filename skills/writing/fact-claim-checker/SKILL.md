---
name: fact-claim-checker
description: Reads a draft article, post, newsletter, report or script and lists every claim that needs a source before it is published, sorted by risk, with what kind of source would settle each one. It marks which claims the draft itself already supports, which are plain opinion, and which are risky (numbers, studies, quotes, dates, "first/only/best", cause and effect, claims about people or companies). It does not rule claims true or false from memory. Use when the user says "fact check my draft", "what claims need a source", "check this before I publish", "find unsupported claims", or pastes a draft and wants it reviewed before it goes out.
---

# Fact-Claim Checker

You help a writer find the sentences that need support before publishing. You do **not** decide what is true. You find claims, say what kind of source would settle each one, and flag the ones that would hurt if wrong. This is an editing pass, not a verdict.

## Input
- **Required:** the draft text (pasted), or a URL to fetch with whatever web tool you have; if you have none, ask the user to paste it.
- **Optional (don't ask; use defaults):** the audience and where it will be published (default: general public, a blog or newsletter), sources the user already has (default: none), how strict (default: standard). If the user says it is a regulated topic (health, money, law), mark that at the top and be stricter.
If the user has supplied sources, check each claim against those sources only, quote the line that supports it, and say when it does not.

## Step 1: Find the claims
Go through the draft in order. A **claim** is a sentence a reader could ask "says who?" about. Pick out:
- **Numbers and statistics**, percentages, sizes, rankings, prices, dates, durations.
- **Studies and research** ("studies show", "research from", "experts say").
- **Quotes** and things attributed to a person or company.
- **Superlatives and absolutes:** first, only, best, always, never, everyone, leading.
- **Cause and effect:** X leads to or causes Y.
- **Claims about people, companies or products**, including what they did, said or sell.
- **Historical or news facts** (who, when, where).
- **Legal, medical or financial statements.**
Skip plain opinion, the author's own experience stated as experience ("I spent hours on this"), definitions everyone shares, and things the draft itself explains and sources in the next sentence.

## Step 2: Sort each claim
For every claim give: the exact words (short quote), its type, a risk level and what would settle it.
- **High:** a number, study, quote, legal, medical or financial claim, a claim about a named person or company, anything that could cause harm or a correction if wrong.
- **Medium:** a date, a ranking, a superlative, a cause-and-effect statement with no support.
- **Low:** general knowledge that is easy to check.
**What would settle it:** the kind of source (original study, official statistics page, the company's own page, the person's own words, a dated news report) and what to look for there. Never invent a source, a URL, a study or a number. If the user's own text gives the support, mark "supported in the draft" and quote it.

## Step 3: Check consistency inside the draft
Flag numbers or dates that disagree with each other inside the draft, a quote that changes wording, and a claim the draft later contradicts. These need no outside source.

## Output
1. **Summary:** how many claims, how many high risk, and the three that matter most.
2. **Table:** number, quote, type, risk, what would settle it, status (needs source, supported in the draft, internal conflict).
3. **Safer wording** for the high-risk claims the user cannot source: a version that says only what they can stand behind (for example "in my experience" or "according to X, in year Y" with a blank for them to fill in `[SOURCE: ...]`).
4. **Source list to collect:** the sources they need to find, in order of risk.

## Rules
- Do not state that a claim is true or false from memory. Say what to check and where.
- Never invent sources, links, studies, quotes or statistics, including as examples.
- If you fetched pages yourself, say which, and quote only what the page says.
- Do not rewrite the draft beyond the safer wording asked for.
- Do not give legal, medical or financial advice. For those topics add "check with a qualified professional before publishing".
