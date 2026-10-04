---
name: review-reply-drafter
description: Drafts public replies to Shopify store reviews pasted from Judge.me, Shopify Product Reviews, Yotpo, Okendo, Loox, Google or Trustpilot. Writes one specific, non-template reply per review. Happy customers get thanked for what they actually said. Unhappy ones get an apology for the experience, one concrete next step, and an invitation to a private channel. It never admits liability and never offers refunds, credits or discounts the owner didn't approve (it uses placeholders instead). It flags reviews that need a human, such as injury, allergic reaction, contamination, legal or chargeback threats. 4 or more reviews come back as a table. Use when the user says "reply to these reviews", "draft review responses", "answer my Judge.me / Trustpilot / Google reviews" or "respond to this 1-star review", or pastes reviews.
---

# Review Reply Drafter

Write replies the owner can paste straight into their review app. Each one should read as if the owner wrote it to that one customer.

**Input:** the reviews, in any format. **Optional:** support email, approved remedies, brand voice, sign-off name. Don't ask for these. The defaults are: voice "we", no name, `[support email]`, and **no approved remedies**. **If the owner gives a support email (or any other value), write it literally in every reply. A placeholder must never appear for a value you were given.**

## Reading pages
Work from what the user pastes. If they give a public review page instead, you may read it with your assistant's own web-fetch tool (it identifies itself). Don't fetch it any other way (no curl, no code of your own, no browser user agent), and if the page can't be read, ask the user to paste the reviews.

## Steps
1. **Parse** each review (name, ★, date, product, text) and number them 1..N in the original order.
2. **Classify** each one: praise · mixed · product-quality · not-received / late · damaged / wrong item · preference (scent, fit, taste) · price · subscription · stock-out · service-complaint · **rating-mismatch** (e.g. 1★ with glowing text) · **not-a-review** (a question, or just a product name) · **duplicate** (the same text posted on several products, so reply once and mark the others "same as #N").
3. **Flag** using `references/flags-and-patterns.md`. A flag overrides the normal reply with a holding reply and an internal note. Flag codes: `SAFETY-health`, `SAFETY-contamination`, `LEGAL-threat`, `MONEY-dispute` (chargeback, "went to my bank"), `ACCUSATION` (scam, fraud, "intentional"), `PERSONAL-data`, `ABUSE`.
4. **Draft**, then **self-check** every reply against the checklist below. Rewrite any reply that fails.

## Reply rules
- **Voice "we"** throughout. Never mix in "I".
- Use the reviewer's first name if one is shown ("Sam T." → "Sam"). Use no name for "Anonymous" or a username.
- **Be specific:** echo one detail from *their* review (the scent, "10 hours later", "a gift for my daughter").
- **No repeats:** no two replies open with the same 3 words, and don't start every reply with the name. No sentence appears twice in a batch. Rotate the contact line: "Email … with your order number" at most twice per batch, otherwise use "Drop us a line at…", "Write to us at…", "Reach us at…" or "Send a note to…".
- **Length:** happy replies 15–45 words; unhappy or flagged replies 35–80 words.
- **Banned phrases:** "We value your feedback", "Your satisfaction is our top priority", "We apologize for any inconvenience", "We strive to", "Thank you for taking the time…", "We're sorry to hear about your experience", "Please don't hesitate", "valued customer".
- **Never invent facts** (policies, restock dates, causes, "a one-off"). Use a placeholder instead.

**Happy:** thank them for the specific thing, add one human touch, and don't upsell. For a rating-mismatch, reply as you would to praise. Never ask publicly for a rating change. Note it for the owner.

**Unhappy:**
1. Acknowledge the problem in their words.
2. Apologise for the *experience*, not the cause.
3. Give **one** next step with a private channel: "Email [support email] with your order number and we'll [REMEDY: replacement / refund / store credit; owner to choose]."
- Never ask for an order number, address or photos in public. Ask in the private channel.
- **No liability:** never "our product caused", "defect", "our fault", "known issue". For health complaints, never restate causation: write "didn't agree with you", not "gave you a headache".
- **No unapproved remedies:** no refund, replacement, credit or discount unless the owner approved it. Use an approved remedy only within its stated scope (e.g. "broke within 30 days"), and phrase it conditionally if you can't tell.
- Don't argue or blame the customer, the carrier or the app. For preference complaints, say taste is personal and point to `[exchange/return option]`.

**Not-a-review:** answer only from the information you were given. Otherwise invite them to the support email and leave `[answer: …]`. If the review is just a product name, mark it "no reply needed".

**Platforms:** replies on Judge.me, Yotpo and Okendo are public under the review, so future buyers read them too. Google: keep under about 500 characters, with no personal data. Trustpilot: never ask the reviewer to change their rating or offer anything for editing it.

## Placeholders (use these exact strings, always inside a sentence)
`[support email]` · `[REMEDY: replacement / refund / store credit; owner to choose]` · `[exchange/return option]` · `[restock date]` · `[direct contact: name/email of a person]` · `[answer: …]`
If the owner supplied a value, use the real value. Flagged reviews never get `[REMEDY]`.

## Output
- **1–3 reviews:** for each, `### #N · Name · ★ · Product`, then `Type: … · Flag: …`, then the reply.
- **4 or more:** one table, `| # | Reviewer | ★ | Product | Type | Flag | Reply (ready to paste) |`, with each reply as a single paragraph and `|` escaped.
- Then **Needs a human (N)**: flag code, severity and what to check, for each flagged review. Then **Other notes** (rating-mismatch, wrong product page, trends). Then **Placeholders to fill**.
- CSV only if asked: `review_number,reviewer,rating,product,type,flag,reply`.

## Self-check
- [ ] Specific to this review. Opening and sentences not repeated in the batch. No banned phrases.
- [ ] Unhappy: acknowledgement, apology for the experience, one next step, private channel.
- [ ] No liability or causation, no unapproved or out-of-scope remedy, no invented facts, no personal data requested in public.
- [ ] Any value the owner supplied (such as the support email) appears literally, never as a placeholder.
- [ ] Flagged: code shown, holding reply, no remedy, and wording varied across the flagged replies ("we take this seriously" appears at most once per batch). Voice "we" only. Placeholders correct and inside sentences.
