---
name: late-payment-chaser-uk
description: Chases one late business invoice for UK freelancers, consultants and small suppliers. Works out the statutory interest (8% over the Bank of England base rate) and the fixed £40 / £70 / £100 recovery sum under the Late Payment of Commercial Debts (Interest) Act 1998 with a script, shows the working with official sources, and writes staged reminder emails ready to send. Use when the user says "my client hasn't paid my invoice", "invoice is overdue", "chase a late payment", "how much late payment interest can I charge", "write a payment reminder", "statutory interest on an unpaid invoice", or gives an invoice amount and date and asks what to do about non-payment. UK business-to-business invoices only; not for consumer debts and not legal advice.
---

# Late Payment Chaser (UK)

Turn the details of one unpaid invoice into (1) a checked calculation of what the supplier can claim under UK late-payment law and (2) a short sequence of reminder emails they can send today. Done means: every figure comes from the script, every rule is quoted from an official source, and the emails need nothing but the names filled in.

Jurisdiction: United Kingdom, business-to-business debts only. This is arithmetic on published rules plus drafting. It is not legal advice, and the output must say so once.

## Input (ask for nothing that has a sensible default)
- **Required:** the unpaid amount and the invoice date. If either is missing, ask for both in one question and stop.
- **Optional (don't ask; use these defaults and say which you used):**

| Input | Default |
|---|---|
| Agreed payment date or terms | None agreed → the law's 30-day rule (the script applies it) |
| Delivery / completion date | Same as the invoice date |
| Date the client received the invoice | The invoice date. With no agreed payment date, the 30 days run from when the client had notice of the amount, so say this assumption in one line and add `[CONFIRM: date the client received the invoice]`; if it arrived later, re-run with that date as `--invoice-date` |
| Customer type | Business. Use `public` if the customer is a council, NHS body, government department or other public authority. Use `consumer` if the client is a private individual buying for themselves |
| Contract late-interest clause | None. If the user mentions one, see Step 1 |
| "As of" date | Today. If the user states a date ("today is…", "as of…"), use that date |
| Names, invoice number, bank details | `[CONFIRM: …]` placeholders |
| Tone | Polite and firm; plain English |

## Step 1: Get the real facts (run the script once)
Run the helper with the user's facts. Dates must be `YYYY-MM-DD`.

```
python3 scripts/late_payment.py --amount 3256.58 --invoice-date 2022-07-31 --due-date 2022-08-28 --as-of 2022-09-30
```
If no payment date or terms were agreed, pass neither `--due-date` nor `--terms-days`: the script then applies the law's 30-day rule, which is not the same as agreed 30-day terms.

Options: `--terms-days 30` (only for agreed terms, instead of `--due-date`), `--delivered DATE`, `--customer business|public|consumer`, `--contract-rate PCT` or `--contract-over-base PCT` (only when the user says their contract or terms set their own late-payment interest), `--offline`.

- The amount is the unpaid figure as the user gave it. Don't add or remove VAT yourself and don't state any rule about VAT. If the user gave a net figure "plus VAT", calculate on the figure given, say so in one line, and add `[CONFIRM: the unpaid invoice total]` so they can re-run with it. Say also that the interest and the fixed-sum band can change with the total, so they should re-run with the invoice total before sending.
- The script tries the Bank of England rate page with its own honest user agent (the Bank's server currently refuses it); it then uses its bundled rate table and says so. Pass that note on. Never fetch the Bank's page another way (no curl, own code or browser user agent).
- **Never compute interest, dates, rates or the fixed sum yourself, and never change the script's figures.** If the script can't run, say so and give only the rules from `references/sources.md`, with no figures.
- If the user gives several invoices, run the script once per invoice and keep the results separate (the fixed sum applies per invoice). More than 5 invoices: do the first 5 and offer the rest.
- If you need to quote a rule in more detail, read `references/sources.md`. Quote only from that file or from the script output.

## Step 2: Decide what can be claimed
Follow the script's result, which is one of:
- **statutory**: interest and the fixed sum can be claimed. Use the figures.
- **not late yet**: no interest, no fixed sum. Write only the friendly reminder (and offer the later stages for when the date passes). Don't mention a claim figure.
- **contract**: the contract has its own interest clause. Use the script's contract-rate figure and say plainly that it applies only if the clause is a "substantial remedy" (section 8, as the script quotes it); if it is not, statutory interest may apply instead. Give the statutory comparison beside it, say which one applies is a question for a solicitor, repeat the `!` warnings in plain words, don't claim the fixed sum, and ask the user to check the clause wording with `[CONFIRM: …]`. Never say statutory interest "is not used" or "doesn't apply" as a settled fact.
- **consumer**: the Act doesn't apply. Write reminders with no interest, no fixed sum and no mention of the Act.

Pass on every line the script marks with `!`, shortened to plain words. In the contract case the script also prints a statutory comparison figure: report it in one bullet of at most 45 words as a comparison, quote section 8(2) or 8(4) from the script, and keep it out of the emails. Give no view on whether the user's clause is a substantial remedy or on what would decide that; say only that it is a legal question this skill can't answer.

## Step 3: Output
Use exactly this structure and add no other sections. Keep the whole answer under 650 words: the notes are short, and the emails carry the detail.

```
# Late payment: [invoice ref or "your invoice"] · £[amount]

**Position on [as-of date]:** [one sentence: "The last day to pay on time was X; interest runs from Y ([n] days)." / not late until X / the Act does not apply. If the user didn't say what kind of customer it is, add "Assumes the customer is a business."]

## What you can claim
| Item | Amount | Basis |
|---|---|---|
| Unpaid invoice | £… | your figure |
| Interest to [date] ([n] days at [rate]%) | £… | [8% + base rate of x% on reference date, with the Order cited] |
| Fixed sum | £… | Late Payment of Commercial Debts (Interest) Act 1998, s.5A |
| **Total today** | **£…** | interest adds £… a day |

[At most 4 short bullets, each under 30 words: how the due date was worked out; each "!" warning from the script; the rate-source note if the snapshot was used; one "not covered" line if needed (see Rules)]

## Emails
### 1. Friendly reminder (send now / at 1–7 days late)
Subject: …
…
### 2. Firm reminder with the statutory position (7–14 days after email 1)
Subject: …
…
### 3. Final reminder before formal action (7 days after email 2)
Subject: …
…

## Before you send
- [CONFIRM: …] list: every placeholder used anywhere above, including dates and totals, grouped onto at most 6 lines. Placeholders only; no other advice here
- GOV.UK: "Send a new invoice if you decide to add interest to the money you're owed."

Sources: [the script's source lines, as links]. UK business-to-business debts only. This is not legal advice.
```

Email rules:
- Email 1 never mentions interest or the Act. It assumes an oversight, restates amount, invoice reference, date and due date, and says how to pay.
- Email 2 states the right to statutory interest and the fixed sum under the Late Payment of Commercial Debts (Interest) Act 1998 and gives the figures as of the as-of date, plus the daily amount.
- Email 3 gives the total now due, a clear deadline of 7 days as `[CONFIRM: date]`, and says the supplier will then *consider* formal recovery (use exactly: "we will consider formal recovery, for example a court claim"; name no other route). No threats, no mention of credit ratings, insolvency or publicity, and no claim that court action has started.
- Each email is under 130 words, plain text, with `[CONFIRM: …]` for names, invoice number and payment details the user didn't give.
- In the not-late, consumer and contract cases, adjust as Step 2 says. Never state the statutory figures where they don't apply.

## Rules (non-negotiable)
- **No invented facts.** Amounts, dates, rates and names come only from the user and the script. Anything missing is a `[CONFIRM: …]` placeholder, listed under "Before you send".
- **Only sourced law.** Every legal statement in the answer must come from the script output or `references/sources.md`, named as the source. Nothing from memory: no section numbers, Acts, schemes, court steps, fees, time limits, VAT rules or rate history that those two sources don't contain. This applies to the notes as much as to the table.
- **Things this skill doesn't cover get one neutral line, with no rule stated.** If the facts hint at something outside the sources (a construction contract, a dispute over the amount, an insolvent customer, part payments), write exactly one sentence of the form "This looks like [X]. This skill doesn't cover the rules for that; check with a solicitor before relying on these figures." and nothing more on the subject: don't say what those rules are, what they might change, or which documents or notices matter under them.
- **Never do your own arithmetic.** Not for comparisons, not for "roughly" figures. A figure is either in the script output or it is a `[CONFIRM: …]`. For a future total, write `[CONFIRM: total on the day you send]` and give the script's daily amount.
- **No overclaiming.** Never say the client "must" pay the interest "by law" as a certainty, never promise the debt will be recovered, and never say what a court will do. Say what the supplier is entitled to claim under the Act.
- **Scope:** one calculation and three emails. No contract drafting, no court forms. If the user asks about those, say this skill doesn't cover them and point to GOV.UK "Make a court claim for money".
- **Stay in your lane:** if the debt is disputed, the customer is insolvent, the contract has its own clause, or the term is longer than 60 days, flag it in one line and suggest a solicitor (the Small Business Commissioner also publishes guidance on unpaid invoices). Don't resolve it.
- **Unsure stays unsure.** Anything the input marks as unsure, unconfirmed or missing stays marked (for example `[CONFIRM: ...]`) in every output, including the final text meant for someone else to read, and is never restated as fact.

## Self-check (before output)
- [ ] Every number in the table and emails matches the script output to the penny.
- [ ] Email 1 has no interest or Act wording; emails 2–3 use it only when the script result is "statutory" (or the contract figure, labelled as contractual).
- [ ] "Not legal advice" and the jurisdiction appear once; sources are linked.
- [ ] Every `[CONFIRM: …]` in the emails is listed under "Before you send".
