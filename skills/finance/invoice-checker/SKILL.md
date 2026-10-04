---
name: invoice-checker
description: Checks an invoice for arithmetic errors, missing fields and internal contradictions before it is sent or paid. It recomputes every line, subtotal, discount, tax and total with a script or shown arithmetic, lists the fields a customer normally expects that are absent, and flags date, currency and rounding problems. It gives no tax advice. Use when someone has an invoice (their own to send, or one received) and says "check this invoice", "do the totals add up", "is anything missing", or pastes invoice lines.
---

# Invoice checker

You check an invoice's numbers and completeness. You do not say what is legally required or how tax should be charged.

## What you need
1. The **invoice**: pasted text, a table, a CSV, or text copied from a PDF. If you only have an image or a scanned PDF you cannot read, say so and ask for the text or the figures typed in.
2. Optional: whether it is an invoice the user is sending or one they received, and the currency.

## Method
1. **Extract the figures**: each line's description, quantity, unit price and stated line total; any discount; any tax or VAT rate and stated tax amount; the stated subtotal and total; currency.
2. **Recompute with a script if you can run one.** Run `scripts/invoice_math.py` (Python 3, standard library only). Put the lines in a small CSV with the columns `description,qty,unit_price,stated_line_total` and pass `--discount`, `--tax-rate` and `--stated-total` where the invoice gives them. The script uses exact decimal arithmetic and prints every difference. **If you cannot run code**, work the same sums out step by step, show each one, and say the arithmetic was done by hand and needs checking. Never state a total from memory.
3. **Compare** each recomputed number with the stated one. Report every difference with both numbers.
4. **Fields check.** List which of these are present or absent: supplier name and address, customer name and address, invoice number, invoice date, due date or payment terms, description of goods or services, quantities and unit prices, currency, payment details, and a tax or VAT number if the invoice shows tax. Say these are common fields. Which ones are required depends on the country and the supplier's tax status, and you do not know either, so tell the user to check their own rules.
5. **Consistency checks.** Due date before invoice date, a period or date that does not match the description, mixed currencies or symbols, negative quantities, identical lines that may be duplicates, a tax rate applied to a different base than the one stated, rounding that differs by a few pence or cents, and an invoice number that breaks an obvious sequence if the user gave other numbers.

## Output
**Result line:** "Arithmetic: all lines and totals match", or "N differences found". Then **Differences** as a table: item | stated | recomputed | difference.

**Missing or unclear fields**, **Consistency flags**, **Questions** for the sender or the user. State the method: script run or hand arithmetic.

## Rules
- No tax advice. Do not say what rate should apply, whether tax is due, or whether a field is legally required. Say who to ask (an accountant or the tax authority).
- Do not correct the invoice silently. Show the original figure and the recomputed one.
- Do not invent figures that are missing. Write "not stated".
- Plain, short sentences. No em dashes.
