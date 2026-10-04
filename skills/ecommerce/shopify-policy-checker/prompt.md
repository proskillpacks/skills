# Shopify Policy Checker: prompt and template

Use this in any chatbot (ChatGPT, Claude, Gemini and others). Nothing to install.

**How to use it**
1. Open these pages on your store and copy their text: `/policies/refund-policy`, `/policies/shipping-policy`, `/policies/contact-information`, and any returns, shipping or FAQ page (`/pages/...`). Also copy any shipping or returns promises from your homepage banner and footer ("Free shipping over $50", "30-day returns"). The privacy policy and terms of service are optional; add them if you want those checked too. Put the page address above each block of text.
2. Copy everything from "COPY FROM HERE" to the end of this file and paste it into a new chat.
3. Under it, paste the texts.

You get a score, the problems ranked by risk (chargebacks, support emails, Google Merchant Center, consumer law), contradictions between your pages quoted side by side, and fixed wording you can paste into Settings > Policies. The installed skill collects all the pages itself with a script; in this version it checks only what you paste, and it says which policies it didn't see. Not legal advice.

**Prefer to check by hand?** The checklist below is the template.

---

COPY FROM HERE

You are auditing a Shopify store's policies. Work only from the texts pasted below. Make sensible assumptions about where the store sells (from currency, addresses, language) and state them. Never invent a number, an address or an email: use a clear blank like "[X] business days" and say what the owner must fill in.

Checklist ("must" = flag as missing if absent):
- Refund (25 points): return window in days and from when (delivery or order); item condition; how to start a return; who pays return shipping; refund method and timing; non-returnable items (must if any); damaged or wrong items (how, by when, photos, who pays); return contact (must); exchanges, restocking fee, sale items, late refunds, store-credit expiry (should).
- Shipping (25): processing time; methods and delivery times by region; costs or free-shipping threshold (the same number everywhere); where you ship and don't; duties and taxes if international (all must); tracking, lost or "delivered but not received" parcels, wrong address, delays (should).
- Privacy (20, only if pasted): business name and contact; data collected; why; who it's shared with; cookies and opt-out; customer rights; matches reality, no template placeholders (must); last-updated date, retention, children (should).
- Terms and contact (15): business name and contact method (must); terms don't contradict the refund or shipping policy, for example boilerplate "all sales final" against a 30-day return policy (must); governing law, price errors and cancellation (should).
- Consistency (15): compare every number and promise across all the pasted sources: return window, who pays return shipping, restocking fees, final-sale items, refund timing, free-shipping threshold and currency, processing and delivery times, warranty, contact details, business name, countries served.
- Region rules, only for regions the store plausibly sells to: EU 14-day right of withdrawal from delivery, refund within 14 days, trader identity and address; UK 14-day cancellation right, goods as described and of satisfactory quality, faulty goods can be rejected within 30 days; Australia: consumer guarantees apply whatever the policy says, so "no refunds" is misleading; US: ship within the stated time or 30 days, offer cancellation if delayed. "No returns" or "store credit only" for EU or UK consumers is High.
Also look for confusing wording: vague time frames, undefined store credit, placeholders like [STORE NAME], another brand's name, the wrong country's law.

Scoring: start each section at its maximum; take off 5 to 10 for each High issue, 2 to 4 for each Medium, 1 for each Low; a missing or empty policy gets 0 for its section; never below 0. If a policy wasn't pasted, mark its section "not checked" and score out of the sections you checked.
Severity: High = missing refund or shipping policy, a contradiction about money or time, a promise that breaks a region rule, placeholder or other-brand text, no contact method. Medium = a missing must-have detail, vague time frames. Low = tone and structure.

Answer in this shape:

# Policy check: [store] ([date])
Not legal advice. This flags common gaps; a lawyer should review anything high-stakes.
## Score: NN/100 (or NN out of the sections checked)
Refund N/25 · Shipping N/25 · Privacy N/20 or not checked · Terms & contact N/15 · Consistency N/15
## Fix these first (3 to 5, highest risk first)
1. **[issue in 6 to 10 words]** (High). Where: [page]. Quote: "[exact text]". Why it matters: [one sentence]. Fix: [replacement text, ready to paste]
## Contradictions
| Topic | Source A says | Source B says | Fix |
## Missing must-haves
| Policy | Missing item | Paste-ready text |
## Confusing wording
| Quote | Problem | Rewrite |
## What's already good (2 to 4 specific bullets)
## Where to paste
Shopify admin > Settings > Policies > [policy]; pages under Online Store > Pages; also check Settings > Policies > Return rules, which should use the same window and fees.

Write fixes in short, plain sentences using "you" and "we", as plain paragraphs and simple lists. Quote exactly. No promises such as "this will prevent chargebacks"; say "reduces" or "helps".

If no policy text is pasted below, ask for it in one line and stop.

Here are my policies and pages:
