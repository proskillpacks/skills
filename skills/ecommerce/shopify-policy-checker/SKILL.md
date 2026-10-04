---
name: shopify-policy-checker
description: Audits a Shopify store's refund, shipping, privacy, terms and contact policies. It flags missing must-haves, contradictions (between policies, FAQ pages and the "free shipping" or "30-day returns" claims in banners) and confusing wording, then gives plain-English fixes you can paste into Settings > Policies. Works from a store URL or pasted policy text. Use when someone asks to "check my store policies", "review my refund/return policy", "is my shipping policy OK", "audit my Shopify policies", "Google Merchant Center misrepresentation", "why are customers confused about returns", or before launching a store. Not legal advice.
---

# Shopify policy checker

Goal: in one pass, tell the store owner what's missing, what contradicts itself, and what will confuse customers, with fixed wording they can paste into **Shopify admin > Settings > Policies**. Rank by how likely each issue is to cost them money: chargebacks, support tickets, a Google Merchant Center review, or a consumer-law problem.

Don't ask questions first. If you have a store URL or policy text, start. Make sensible assumptions and state them (e.g. "Assumed you sell to the US and EU because prices show USD and the privacy policy mentions GDPR").

## Reading the store: only through the script
- **Fetch store pages only with `scripts/fetch_policies.py`.** Don't fetch them any other way: no curl or wget, no code of your own, no browser user agent and no retries under another name. The script sends an honest user agent and obeys the store's robots.txt (RFC 9309).
- **If the script prints `NOT FETCHED`** (robots.txt does not allow the page, or robots.txt itself could not be read), stop for that page. If the user says it is their store, run it again with `--owner` (it skips the robots.txt check, nothing else). Otherwise ask the user to paste the text, and say why.
- **If the script returns an error or leaves a fact out**, say "not found by the script" and use a placeholder or ask the user to paste it. Never write a fetcher to get round it.
- **No shell at all?** Your assistant's own web-fetch tool may read the same public pages the script would (it identifies itself). Never use it for a page the script reported as not fetched, and don't use it to get round an error.

## Step 1. Collect the text

**With a shell** (preferred, gets everything in one go):

```bash
python3 <skill-dir>/scripts/fetch_policies.py <store-domain> -o policies.md
```

It saves one Markdown file with:
1. Each Shopify policy from `/policies/<name>.json`: refund, shipping, privacy, terms of service, contact information, legal notice, subscription. Each is marked MISSING (no policy set), EMPTY (no text), VERY SHORT (under 40 words) or with its word count. Long terms of service are cut down to the paragraphs about orders, shipping, returns, refunds, warranty, disputes, governing law and contact.
2. Store pages that often repeat policy terms (`/pages/faq`, `/pages/shipping`, `/pages/returns`, `/pages/warranty`, and so on) if they exist.
3. Sentences about shipping, returns, refunds, guarantees and warranty found on the homepage and one product page (announcement bars and footers).

Read the whole file.

**Without a shell:** fetch `https://<store>/policies/refund-policy`, `/policies/shipping-policy`, `/policies/privacy-policy`, `/policies/terms-of-service`, `/policies/contact-information`, and the homepage. Ask the fetch tool for the full policy text verbatim, and for any shipping/returns/warranty claims on the homepage. If the user pasted policy text, use that.

A policy that is EMPTY or MISSING at `/policies/` but exists as a normal page (e.g. `/pages/returns`) is a finding in itself. Shopify links the `/policies/` versions in checkout and in the store footer, so customers can end up on a blank page. Tell the user to paste the real text into Settings > Policies (or, for shipping and returns, at least link to the page there).

## Step 2. Check against the checklist

Open `references/checklist.md` and go through every item for each policy. Then run these checks:

- **Contradictions.** Compare every number and promise across all sources: return window (days), who pays return shipping, restocking fees, final-sale items, refund method and timing, free-shipping threshold, processing time, delivery times, regions served, warranty length, contact email and address. Two different values for the same thing is a contradiction. Quote both, with where each one appears.
- **Confusing wording.** Vague time frames ("in a timely manner"), undefined terms ("store credit" without saying whether it expires), double negatives, legal boilerplate that contradicts the friendly FAQ, placeholder text (`[STORE NAME]`, `[email]`, "Lorem ipsum"), another brand's or an old store name, the wrong country's law, references to things the store doesn't sell.
- **Region rules** (only for regions the store plausibly sells to, inferred from currency, addresses, shipping zones and language): see the region section of the checklist.

## Step 3. Write the report

Use this structure. Keep it tight. The owner should be able to act on the first screen.

```
# Policy check: <store> (<date>)
Not legal advice. This flags common gaps; a lawyer should review anything high-stakes.

## Score: NN/100
Refund N/25 · Shipping N/25 · Privacy N/20 · Terms & contact N/15 · Consistency N/15

## Fix these first (top 3–5, highest risk first)
1. **<issue in 6–10 words>** (High). Where: <policy/page>. Quote: "<exact text>"
   Why it matters: <one sentence: chargebacks / tickets / Google Merchant Center / law>.
   Fix: <exact replacement text, ready to paste>

## Contradictions
| Topic | Source A says | Source B says | Fix |

## Missing must-haves
| Policy | Missing item | Paste-ready text |

## Confusing wording
| Quote | Problem | Rewrite |

## What's already good
<2–4 bullets, specific>

## Where to paste
Shopify admin > Settings > Policies > <policy>. For pages: Online Store > Pages > <page>. Also check Settings > Policies > Return rules, which should use the same window and fees as the refund policy text.
```

Scoring guide: start each section at its maximum. Take off 5–10 for each High issue, 2–4 for each Medium, 1 for each Low. A MISSING or EMPTY policy gets 0 for its section. Never go below 0.

Severity:
- **High:** missing or empty refund or shipping policy; a contradiction about money or time (return window, fees, free-shipping threshold); a promise that breaks a region rule (e.g. "no refunds" for EU or Australian customers); placeholder or other-brand text; no contact method.
- **Medium:** missing must-have detail (who pays return shipping, processing time, refund timing); vague time frames; outdated date.
- **Low:** tone, structure, readability.

## Rules for the fixes

- **Use the store's own facts.** Take numbers from the store's other text (e.g. the FAQ says 30 days, so the fix says 30 days). If a fact is unknown, put a clear blank like `[X] business days` and say which fact the owner must fill in. Never invent a number, an address or an email.
- Write fixes at about an 8th-grade reading level: short sentences, "you" and "we", one idea per sentence.
- Make paste-ready text plain paragraphs and simple lists (the Shopify policy editor is a rich-text box).
- Quote exactly. When you say "the FAQ says 60 days", include the sentence.
- Don't pad. If a policy is fine, say so in one line.
- No fear-mongering and no promises ("this will prevent chargebacks"). Say "reduces" or "helps".
