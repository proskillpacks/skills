# Dispute reasons, evidence and submission rules

Sources (fetched 2026-10-03): Shopify Help Center (chargeback-process, chargeback-reasons, chargebacks-in-admin, resolve-chargeback, shopify-protect, network-dispute-resolution-programs), Shopify Admin API `ShopifyPaymentsDisputeEvidence` / `ShopifyPaymentsDisputeReason`, Stripe docs (disputes/categories, reason-codes-defense-requirements, best-practices, responding, how-disputes-work, api/disputes, visa-ce3). Rules change: if the merchant's dispute page says something different, the dispute page wins.

## 0. Check these first (they can end the job)
| Situation | What to tell the merchant |
|---|---|
| Order shows **Shopify Protect: protected** and reason is Fraudulent or Unrecognized | "No action needed. Shopify reimburses protected fraud/unrecognized chargebacks as a credit." (US stores, Shop Pay orders only.) Don't draft unless asked. |
| Status **resolved** (network dispute resolution program, e.g. Visa RDR) | Already refunded automatically; there's no evidence window. Nothing to draft. |
| Status **won / lost** | Decisions are final; no appeal or new evidence. A bank *can* re-dispute after a win (new deadline). |
| Reason **noncompliant** | Rare compliance case; contesting it can carry a large extra fee (Stripe: 500 USD, refunded if won). Tell them to read the dispute page and contact Shopify Support before doing anything. |
| Deadline passed | Nothing can be submitted. Say so. |
| Merchant already refunded the full amount before the chargeback | Fight as **credit already processed**: the refund record is the core evidence. Never refund again during an open dispute (Shopify/Stripe can't refund an open dispute; refunding twice is how merchants lose double). |

## 1. Inquiry vs chargeback
- **Inquiry**: no money withdrawn yet; the bank wants information. Mostly Amex/Discover (Visa/Mastercard largely no longer use this stage). Submitting evidence can close it; ignoring it usually leads to a chargeback that's hard to win. Shopify: a full refund stops a chargeback but is "possible but not recommended" during an inquiry; if the merchant refunds, still submit evidence of the refund.
- **Chargeback**: funds and the fee are withdrawn. Respond or accept.

## 2. Money facts
- Shopify chargeback fee (Shopify Payments): US 15 USD · UK 10 GBP · most EU countries 15 EUR (Ireland adds 23% VAT) · Canada 15 CAD or 15 USD · Australia 25 AUD · NZ 20 NZD. When you tell the merchant, write the amount the way they would read it ("15 USD"). Returned if the merchant wins (Shopify says it "might" depend on region); **not** returned when accepting. The amount and the fee are withdrawn as soon as the chargeback is opened. Shopify's page states no separate fee for submitting a response and says nothing either way, so don't call fighting "free" or say it "costs nothing extra": say the cost of fighting is the merchant's time, and name no figure for it.
- Accepting is not an admission of wrongdoing (Stripe). It returns the disputed amount to the cardholder.
- Winning doesn't remove the dispute from the merchant's chargeback rate.
- Review takes up to ~75 days (Shopify). Partial wins are possible.
- Don't invent win rates. The only official number set is Stripe Radar's estimate for Stripe accounts; don't quote it for Shopify.
- Accept-vs-fight line: "Fighting recovers [amount] [+ fee] if you win and costs your preparation time. Accepting costs [amount] + [fee] now and ends it."

## 3. Categories
Shopify labels in the admin: Fraudulent, Unrecognized, Duplicate, Subscription canceled, Product not received, Product unacceptable, Credit not processed, General. API enums in brackets.

### Fraudulent [FRAUDULENT]: Visa 10.3/10.4, Amex F29
- **What the bank needs**: proof the **real cardholder** (or someone they authorised, e.g. a family member) made the purchase. Proof of delivery alone does **not** answer fraud: a stolen card can ship to the thief's address.
- **Core evidence**: AVS match (billing address verified) **and** shipping address = billing address, CVV match, 3D Secure authentication, IP/device consistent with the cardholder's location, prior undisputed orders from the same customer/card, customer communication linking the recipient to the cardholder.
- **Visa 10.4 Compelling Evidence 3.0**: two earlier undisputed payments on the same card, 120–365 days before the dispute, matching on IP + device, or one of those plus shipping address / email / account ID. If the merchant has this, say so; it's the strongest Visa fraud defence. Shopify includes undisputed order history automatically.
- **Argument order**: authorization data → match between cardholder and delivery → order history → communication → delivery.
- **Usually lost when**: AVS/CVV mismatch or unavailable, ship-to ≠ billing with no explanation, high fraud risk flag ignored, no prior history, no 3D Secure, only tracking as evidence, hand delivery with no link to the cardholder. Visa 10.5 has no recourse.
- **Unfulfilled fraud-flagged order**: don't ship. Accepting (or not shipping and letting it close) is the right call; there's nothing to defend.
- **Good move first**: contact the customer. Many "fraud" disputes are a forgotten purchase or a family member. If the cardholder agrees to withdraw, see "When the customer says they withdrew the dispute" below.

#### When the customer says they withdrew the dispute
- **The dispute stays open until the bank closes it.** A customer saying "I cancelled it" changes nothing in Shopify or Stripe. The merchant still has to respond before the deadline: "you still need to submit evidence if you want to win the dispute… Many card issuers treat failure to submit evidence as an acceptance of liability" (Stripe, Dispute withdrawals).
- **Shopify Payments: ask the customer for the bank's chargeback withdrawal letter.** Shopify's Help Center (Resolve a chargeback) says the letter must: be on official bank letterhead; display the case number; confirm the original charge date and amount; confirm the store or business name; confirm that the chargeback has been cancelled; confirm that the funds have been re-debited from the customer's account; and confirm that the funds have been returned to the merchant. In plain words: the letter says the dispute is cancelled, **the customer has been charged again, and the money is going back to the merchant**. It does not say the charge "won't be re-debited"; the re-debit of the customer is the point.
- "A screenshot of the customer's bank statement isn't sufficient. The customer must obtain an official withdrawal letter from their bank" (Shopify). Stripe is looser: it accepts "a confirmation email from their bank or a screenshot of their mobile banking statement that shows they were re-billed for the charge", and says this "isn't required… but provide it if you can".
- **Where it goes:** Shopify: submit the letter as dispute evidence in the Chargeback response form on the order (uncategorized file). Then the banks review it; Shopify says this "can take up to 30-90 days or sooner".
- **One piece of advice, stated once:** respond before the deadline in every case. Wait for the letter only as long as the deadline allows; if it hasn't arrived, submit what you have. Never tell the merchant both to hold off and to submit.
- Don't refund while the dispute is open.
- Sources (fetched 2026-10-04): help.shopify.com/en/manual/payments/chargebacks/resolve-chargeback; docs.stripe.com/disputes/withdrawing. Neither page quotes card-network rule text; Stripe states that every card network lets a cardholder retract a dispute and that the process varies by issuer.

### Unrecognized [UNRECOGNIZED]: Mastercard 6321, Amex 127/176
- Cardholder doesn't recognise the statement descriptor. Treat like Fraudulent.
- **Core evidence**: same as Fraudulent, plus the billing descriptor and its connection to the store name, order confirmation email, any message where the customer acknowledges the order.
- **Prevention**: a recognisable statement descriptor.

### Product not received [PRODUCT_NOT_RECEIVED]: Visa 13.1, Mastercard 4855, Amex C08
- **Core evidence**: carrier tracking showing **Delivered** (or a carrier confirmation of delivery). **Strengtheners**: delivery address matching the checkout shipping address (check it; a mismatch drops it to Weak), proof of delivery (signature or carrier delivery photo), delivered date. Shopify auto-attaches a fulfillment PDF and sometimes the carrier's delivery photo.
- **Or**: the delivery date hasn't come yet (stated delivery estimate in policy/checkout + tracking in transit), or held in customs.
- **Argument order**: shipped date → carrier/tracking → delivered date and address → POD → communication (customer didn't report a problem, or did and what was offered).
- **If it was delivered after the dispute was filed**: say so explicitly with the delivered date ("delivered on [date], after the dispute was opened").
- **Usually lost when**: no tracking, tracking stops at "in transit"/"label created", delivered to a different address than checkout, no POD on a high-value item, merchant shipped late.
- **Don't include**: the return policy (not relevant to non-receipt; Stripe says irrelevant evidence weakens the case).
- **Partial non-receipt** (some items arrived): argue the dispute exceeds the value of what wasn't received; offer the evidence for what was delivered.

### Product unacceptable / not as described [PRODUCT_UNACCEPTABLE]: Visa 13.3/13.4/13.5, Mastercard 4853, Amex C31/C32
- **Core evidence**: the product listing as it was at purchase (description, photos, sizing, disclaimers), proof the item shipped as listed (pre-shipment photos, QC), the return/refund policy and where it was shown, communication showing the merchant offered a return/replacement/refund under the policy and the customer didn't take it, or the customer never contacted the merchant.
- Networks expect the cardholder to try to resolve it with the merchant first; if they didn't, say so (only if true) and show the store's contact/return process and that the merchant would have resolved it.
- If the item wasn't returned, say so.
- **Usually lost when**: the item really was damaged/wrong and no remedy was offered, the listing doesn't match the item, the merchant refused a return the policy allows, no listing evidence, the merchant referred the customer to the manufacturer.
- **Partly at fault** (e.g. 3 of 14 items damaged): concede the faulty part, fight the rest; say the disputed amount exceeds the value of the faulty items and offer a partial refund of that part if allowed.

### Subscription canceled [SUBSCRIPTION_CANCELLED]: Visa 13.2, Mastercard 4841, Amex C28
- Can also mean the customer expected a reminder before each renewal.
- **Core evidence**: the subscription terms and cancellation policy and where they were shown at signup, proof the charged subscription was **still active** (no cancellation request before the charge date), how to cancel (link in emails/account) and that the customer knew (they cancelled a different one, or used the process before), renewal reminder emails **actually sent** (sent log or copy, not just a setting), delivery of the order paid for by the disputed charge.
- **Usually lost when**: the customer cancelled before the charge, no renewal notice where one is required, cancellation was hard to find, merchant can only show a notification setting and not the sent email.
- If the merchant charged after a valid cancellation: accept (Shopify: "you have to accept the chargeback").

### Duplicate [DUPLICATE]: Visa 12.6.1/12.6.2
- **Core evidence**: each charge is a separate order (different order numbers, items, dates, shipping), both fulfilled; or one was refunded/voided (refund record).
- Customers often mistake an authorization hold for a second charge; explain if the order record shows that.
- If it really was charged twice: accept (or show a refund was already issued).

### Credit not processed [CREDIT_NOT_PROCESSED]: Visa 13.6/13.7, Amex C02/C04/C05
- **Core evidence**: the refund was already issued (refund record, date, amount, and that refunds take X days to appear), **or** the customer isn't entitled to one under a policy shown before purchase (policy + where shown + `refund_refusal_explanation`: e.g. item not returned, outside window, final sale), return tracking if a return was required.
- **Usually lost when**: the merchant promised a refund and hadn't processed it, the policy wasn't shown before purchase, the item was returned and no refund followed.
- If a refund is owed and wasn't paid: accept. (A refund can't be issued during an open chargeback; accepting returns the money.)

### General [GENERAL]: Visa 12.2/12.5, Amex P05/P23
- Uncategorised. Contact the customer to learn the real complaint, then use the evidence for the closest category. For amount disputes: itemised receipt, the total shown at checkout, currency/exchange information.

## 4. Where evidence goes (field map)
Shopify's **Chargeback response** page (Orders → order → chargeback banner → **Add evidence**) has an additional-information text box and file uploads per evidence type; Shopify fills in a lot automatically. The underlying fields mirror Stripe's evidence object:

| Evidence | Shopify (API field) | Stripe field |
|---|---|---|
| Written argument / summary | uncategorizedText ("additional information") | uncategorized_text ("Why you should win") |
| Emails, chats, SMS with the customer | customerCommunicationFile | customer_communication |
| Tracking, carrier, delivery proof, POD | fulfillments (auto) + shippingDocumentationFile | shipping_carrier, shipping_tracking_number, shipping_date, shipping_documentation |
| Billing / shipping address, IP, customer email | billingAddress, shippingAddress, customerPurchaseIp, customerEmailAddress (auto) | billing_address, shipping_address, customer_purchase_ip, customer_email_address |
| Refund policy + where shown | refundPolicyFile, refundPolicyDisclosure | refund_policy, refund_policy_disclosure |
| Why no refund is owed | refundRefusalExplanation | refund_refusal_explanation |
| Cancellation policy, where shown, rebuttal | cancellationPolicyFile, cancellationPolicyDisclosure, cancellationRebuttal | cancellation_policy, cancellation_policy_disclosure, cancellation_rebuttal |
| Product listing/description | productDescription | product_description |
| Access/usage log (digital, subscriptions) | accessActivityLog | access_activity_log |
| Other duplicate-charge docs | uncategorizedFile | duplicate_charge_documentation, duplicate_charge_id, duplicate_charge_explanation |
| Anything else (photos, order history, withdrawal letter) | uncategorizedFile | uncategorized_file |

Automatically included by Shopify (tell the merchant not to re-upload unless it's missing): product details, customer name/email, billing/shipping address, IP, fulfillment details and a tracking PDF (sometimes with the carrier delivery photo), refund records, undisputed previous orders, previous disputes, sometimes payment verification results and the relevant policy.

## 5. Submission rules (Shopify Payments)
- Files: PDF, JPEG or PNG only. Each file ≤ 2 MB; all files together ≤ 4 MB; each PDF < 50 pages; PDF/A, no portfolios. **One file per evidence type**: combine screenshots into one PDF per type.
- No audio, video, links, or "please call/email us". Screenshots, not URLs.
- High contrast, readable in black and white (some banks get evidence by fax), cropped to the relevant part, no zooming needed, no colour highlighting. Label each file (e.g. "Order confirmation email sent [date], itemised total [amount]").
- Order evidence: direct proof → customer acknowledgement → policy → supporting context. The reviewer may spend only a few minutes.
- Deadline: shown on the order (store time zone; 11:59 PM if no time). Shopify submits automatically on the due date; **Submit now** sends early and locks edits. One submission only.
- Accept: **Accept chargeback** → **Submit**. Accepted by mistake? Contact Support before the deadline.
- Stripe (non-Shopify) limits for reference: total ≤ 4.5 MB, < 50 pages (19 for Mastercard), text fields ≤ 20,000 chars.

## 6. Tone (from Stripe best practice)
Neutral, factual, chronological, short. One clear sentence of why the claim doesn't hold, then evidence. Model: "[Cardholder] purchased [product] on [date]. We shipped it on [date] to the address provided, and it was delivered on [date], as shown in the tracking file, so the claim that it wasn't received isn't accurate." Only include relevant excerpts; no whole terms documents.

## 7. Prevention tips (use only these; each follows from the evidence lists above)
- A statement descriptor the customer will recognise (Unrecognized).
- Ship every order with tracking. On higher-value orders, use a delivery option that gives a signature or a delivery photo: both are listed as strengtheners for Product not received.
- For digital goods and software, keep the download, activation or access log: it is the delivery evidence for those orders.
- Keep customer conversations in a form you can attach (email, chat or text), because the customer communication file takes screenshots or PDFs, not calls.
- Show the refund and cancellation policy before purchase and keep a screenshot of where it appears (Credit not processed, Subscription canceled, Product unacceptable).
- Don't ship orders that carry a high fraud-risk flag until you've checked them (Fraudulent).
- Send an order confirmation email that names the store and the items (listed as evidence for Unrecognized).
