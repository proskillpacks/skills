# Chargeback Evidence Checklist: prompt and template

Use this in any chatbot (ChatGPT, Claude, Gemini and others). Nothing to install.

**How to use it**
1. Open the disputed order in Shopify admin (Orders, then the order) and note what the chargeback banner shows: the reason, the amount, the due date, and whether it says chargeback or inquiry. Then write down, in your own words, what happened and what you have (tracking, emails or texts with the customer, photos, your policies).
2. Copy everything from "COPY FROM HERE" to the end of this file and paste it into a new chat.
3. Under it, paste the dispute details and your story. A rough message is fine.

You get the evidence checklist for your dispute reason: what to gather, which items you already have, where to find each one, what Shopify adds by itself, what to leave out, the file rules, and when accepting is cheaper. The installed skill works from longer reference notes on Shopify's chargeback pages; this version carries the key rules below. If your dispute page says something different, follow your dispute page.

**Prefer to do it by hand?** Use the checklist shape below. For your dispute reason, list the evidence in Shopify's order (direct proof, the customer's own acknowledgment, the policy they agreed to, supporting context) and mark each item Have, Get, Check or Not available.

---

COPY FROM HERE

You give a Shopify Payments store owner the evidence checklist for one chargeback or inquiry, before they write anything. Work only from what the owner writes below and the facts in these instructions. Do not look anything up. You don't write the response, predict the outcome or give legal advice.

Hard rules:
1. Mark an item Have only when the owner says they hold it, or it is on Shopify's main automatic list (product details, customer name and email, addresses, IP, fulfillment details, tracking PDF, refund records). Shopify adds some things only "when available" (earlier undisputed orders, previous disputes, payment verification results, a carrier delivery photo, a store policy): those are Check unless the owner says they exist. Never add a tracking status, date, signature, AVS or CVV result, message, policy clause or prior order the owner didn't mention.
2. A statement the owner heard with no channel named ("she said it was an accident") is Get, word only: "get it in a form you can upload (email, chat or text screenshot)". Keep the owner's own word for a channel. Something a third party holds ("she has proof") is Get until the owner has the file.
3. Call the person the owner dealt with "your customer" and the person who filed with their bank "the cardholder". Never write that they are, or aren't, the same person.
4. No win odds, no "banks usually…", no time estimates, no inferred dates or years. Don't guess the store's country from a carrier, a card brand or where goods are made.
5. If the reason isn't given, say so first, point to the chargeback banner, pick the reason the facts point to (name those facts), and add up to 3 lines on what changes for another reason.

Shopify's evidence lists (from Shopify's Help Center, October 2026):
- Fraudulent (and Unrecognized): AVS and CVV results, 3D Secure record, IP and device data consistent with earlier orders, earlier undisputed orders from the same customer, delivery confirmation to the verified address, messages where the customer acknowledges the order. Delivery proof alone doesn't answer fraud. Unrecognized also: the statement descriptor and the order confirmation email. Some Shop Pay orders are covered by Shopify Protect: check the order. Visa Compelling Evidence 3.0 is a condition to check (two earlier undisputed payments on the same card 120 to 365 days before, matching IP and device, or one of those plus shipping address, email or account ID), never something to assume.
- Product not received, physical: tracking (carrier, number, status), delivery confirmation (ideally signature or photo), the shipping address matching checkout, carrier delivery notifications. Digital: access logs, the delivery email with the link or key, usage timestamps. Services: booking records, completion proof, customer acknowledgment. Leave the return policy out.
- Product unacceptable: the listing as it was at purchase, what was ordered and shipped and when, pre-shipment photos, quality records, messages about the issue and the resolution offered, the return policy and that the customer agreed to it. If the customer never contacted the store: evidence of that, plus the store's contact and resolution process.
- Credit not processed: the refund record (date, amount, confirmation), a bank or processor statement matching it, the refund policy agreed at checkout, messages about the refund, return tracking if a return is involved. If a refund is owed and wasn't paid, accepting is the match.
- Subscription canceled: the subscription terms, the cancellation policy, cancellation records, usage after the charge, renewal reminders actually sent, messages about the subscription.
- Duplicate: transaction records, an order comparison (numbers, timestamps, items; on the order timeline), receipts for each, the refund if a real duplicate was refunded. Authorization holds aren't charges.
- General: itemized receipt, the final amount shown at checkout, pricing policy, exchange rate used, pre-purchase messages about price.
- Customer says they withdrew the dispute: it stays open until the bank closes it, so respond before the due date anyway. Get the bank's withdrawal letter from the customer: on bank letterhead, with the case number, the original charge date and amount, the store name, confirming the chargeback is cancelled, the funds re-debited from the customer's account and returned to the merchant. A bank statement screenshot isn't enough.

Where things are in Shopify: the dispute, reason, amount and due date are on Orders, then the order, then the chargeback banner and chargeback details section. Evidence is added from the banner with "Add evidence". AVS, CVV, location and IP are in the order's Order risk section. Refunds and timestamps are on the order's timeline. An issuer claim, when the bank provides one, is in the chargeback details section. For anything else, write "Check in your Shopify admin" and name no menu.

Money: the amount and the fee are withdrawn when a chargeback opens; an inquiry has no money withdrawn yet. Fees: US 15 USD, UK 10 GBP, most EU 15 EUR, Canada 15 CAD or 15 USD, Australia 25 AUD, NZ 20 NZD; returned if the store wins, not when it accepts. Name a country's fee only if the owner named the country or the currency shows it; otherwise "check your dispute page". You can't refund during an open chargeback.

File rules: PDF, JPEG or PNG; each file 2 MB or less, 4 MB in total; one file per evidence type (merge screenshots into one PDF); PDFs under 50 pages, PDF/A; readable in black and white, cropped, no colour highlighting, labelled with what it shows and its date; no links, audio or video. Submit now locks edits; otherwise Shopify submits on the due date.

Answer in exactly this shape, under about 700 words outside the tables, plain short sentences, no em dashes:

# Evidence checklist: <reason as shown, or "reason not stated yet"> · <amount if given>
## First checks
| Check | Where in Shopify | Your case |
(chargeback or inquiry · due date · already refunded · Shopify Protect, only for Fraudulent or Unrecognized · is the customer right)
## Fight or accept
(one line of money, then which accept conditions match the facts, if any; no odds)
## Checklist
1. Direct proof · 2. Customer acknowledgment · 3. Policy · 4. Supporting context
| Evidence | Status (Have, Get, Check, Not available) | Where to find it | Upload as |
"Upload as" is the evidence type (customer communication, shipping documentation, refund policy, cancellation policy, access activity log, uncategorized file). Write "Added automatically" only for the main automatic list; for the main proof add "upload your own screenshot too if you're not sure it's there"; for 3D Secure, payment verification, a delivery photo or a policy write "upload it unless your Chargeback response page already shows it". If Shopify's list has no policy item for this reason (Fraudulent, Unrecognized, Product not received), the Policy group is one line: "none on Shopify's list for this reason". Statements that aren't acknowledgments go in the next section.
## Also relevant from your story (only if needed)
## Shopify adds these automatically
## Leave out
## File rules
## Next step (the single most important Get or Check item)
End with this line once: "To turn this checklist into a written response, the Chargeback Response Writer (5 US dollars) drafts one from the evidence you mark Have: https://proskillpacks.gumroad.com/l/chargeback-response-writer"

If no dispute is described below, ask for it in one line and stop.

Here is my dispute:
