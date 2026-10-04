# Shopify: evidence by dispute type, and where to find it in the admin

Sources, read on 2026-10-04: Shopify Help Center pages "Responding to chargebacks and inquiries" (help.shopify.com/en/manual/payments/chargebacks/chargeback-process: Responding by dispute type, Provide the best evidence, Evidence included automatically, Chargeback fees), "Managing chargebacks in the Shopify admin" (…/chargebacks/chargebacks-in-admin), "Resolving a chargeback or inquiry" (…/chargebacks/resolve-chargeback) and "Reviewing orders with fraud analysis" (help.shopify.com/en/manual/orders/fraud-analysis). Admin menus change: if the merchant's screen or dispute page says something different, follow it.

Use this file for **where things are** in Shopify and **what Shopify lists for each dispute type**. Use `reason-codes.md` for core evidence, "usually lost when", the Check-these-first table, file rules and money facts.

## 1. Where things are in the Shopify admin
| What | Where (quote the path as written) |
|---|---|
| The dispute itself: reason, amount, due date, status | **Orders** → click the disputed order → the chargeback banner and the chargeback details section |
| List of all open chargebacks and inquiries | **Orders** → **Search and filter** → **Add filter** → **Chargeback and inquiry status** → **Open** |
| Why the customer's bank opened it (when the bank provides it) | Order → chargeback details section → **Issuer claim** (summary plus a downloadable document). Not available for every dispute |
| Guidance on the reason code | Order → chargeback details section → click the chargeback reason code (Sidekick) |
| Where evidence is added | Order → chargeback banner → **Add evidence** → **Chargeback response** page: an additional-information box and file uploads |
| Accept instead | Chargeback banner → **Accept chargeback**, or **Add evidence** → **Accept chargeback**, then **Submit** |
| AVS and CVV results, location vs payment method, device or network activity, IP address | Order → **Order risk** section → **Order risk evaluation** or **About this order** (fraud indicators; the IP address is listed separately). Shown for online credit card orders Shopify can verify |
| Shopify Protect status | "Check your order details to confirm if an order is protected" (Shopify). The fraud analysis page says to review the protection status separately from the fraud indicators |
| Transaction timestamps (two charges, refunds) | The order's **timeline** |
| Statuses | open (you can still add evidence), submitted, won, lost, resolved (resolved by a network dispute resolution program, no evidence window) |
| Due date | Shown on the dispute, in the store's time zone; 11:59 PM if no time is shown. Typically 7 to 21 days after the chargeback is filed |
| Chargeback emails go to | The store contact email (Settings → Store details) |

Things that are **not** in the Shopify admin and must come from elsewhere: emails, chats and texts with the customer (the merchant's inbox or helpdesk); carrier proof of delivery, signature or delivery photo if not already in Shopify's tracking PDF (the carrier's tracking page or account); screenshots of the product listing as it was at purchase (the merchant's own saved copies or archive); access, download or usage logs for digital goods (the app or system that delivers them); subscription app records and sent renewal emails (the subscription app or email platform); a bank withdrawal letter (from the customer, who gets it from their bank).

## 2. Evidence Shopify includes automatically (Shopify Payments)
"When the information is available for the order": product details (title, variant, quantity); customer name and email; billing and shipping addresses saved on the order; the IP address used to place the order; fulfillment details (shipping date, carrier, tracking number); a shipping tracking PDF for orders with a tracking number (for some carriers it includes the carrier's delivery photo); refund records; the customer's previous orders that weren't disputed; previous disputes by the same customer. Depending on the dispute type and payment method, it can also include payment verification results or the relevant store policy (shipping policy for product not received; return policy for credit not processed and product unacceptable; subscription policy for subscription canceled).

The response is submitted on the due date even if the merchant adds nothing. What Shopify can't add, in its own list: emails, chat logs and other communication with the customer; the policies that apply and **where the customer agreed to them**; a carrier delivery photo or signature if not already in the tracking PDF; access or usage logs for digital products and services; the product listing from the time of purchase.

## 3. Evidence Shopify lists by dispute type (seven categories)
Shopify's page: "Strong evidence improves your chances of success, but it doesn't guarantee that you win a chargeback."

- **Credit not processed.** Refund transaction record (timestamps, amount, confirmation number); a bank or processor statement showing when the refund was processed and that it matches the disputed charge; the refund policy and the terms agreed at checkout; customer communications about the refund status or policy; return tracking, if a return is involved.
- **Duplicate.** Transaction logs (one charge, or separate orders); order details comparison (order numbers, timestamps, items; timestamps are on the order's timeline); pre-authorization explanation if one was a temporary hold; receipts for each transaction; refund confirmation if a real duplicate was already refunded. Customers can mistake authorization holds for duplicate charges.
- **Fraudulent.** AVS and CVV verification; device and IP data consistent with earlier orders; 3D Secure record; order history (earlier successful orders from the same customer, email or shipping address); delivery confirmation to the customer's verified address; customer communications acknowledging the order. "The strongest evidence includes matching addresses, consistent device or location data, and delivery confirmation to the billing address." Some Shop Pay orders are covered by Shopify Protect.
- **Product not received.** Physical: tracking (carrier, number, status), delivery confirmation (ideally signature or photo), shipping address matches checkout, carrier delivery notifications sent to the customer. Digital: access logs, delivery email with link, key or credentials, usage timestamps. Services: booking records, completion proof, customer acknowledgement.
- **Product unacceptable.** Product listing at time of purchase; order and fulfillment records; pre-shipment photos; quality control records if any; customer communications about the issue and the resolution offered; return policy and process, showing the customer agreed to it; support ticket history. If the customer never contacted the merchant before disputing, include evidence of that and the merchant's resolution process.
- **Subscription canceled.** Subscription agreement (billing cycle, auto-renewal); cancellation policy; cancellation records (or evidence that no request exists); usage logs after the charge date; billing notifications (renewal reminders or receipts sent before the charge); customer communications about the subscription.
- **General.** Itemized receipt; checkout confirmation of the final amount; pricing policy (taxes, fees, currency); exchange rate used, for international orders; pre-purchase messages about the price; system logs of the amount authorized and charged.

Shopify's admin also shows the label **Unrecognized**; `reason-codes.md` treats it like Fraudulent plus the statement descriptor and order confirmation email.

## 4. Order of evidence (Shopify)
1. **Direct proof:** delivery confirmation with signature, tracking showing delivered at the matching address, refund transaction record, or usage logs.
2. **Customer acknowledgment:** emails or messages where the customer confirmed receipt, discussed the product or acknowledged the transaction.
3. **Policy documentation:** terms or refund policy the customer agreed to at checkout.
4. **Supporting context:** order history, address and payment verification results, communication timeline.
Use screenshots, not links. Label every file with what it shows and its date.

## 5. Customer contact
Card networks expect the customer to contact the merchant first. If they went to the bank without contacting the merchant: evidence that no support request was received, the merchant's contact information and resolution process, and a note that the merchant would have resolved it.

## 6. Refunds during a dispute
"You can't issue a refund after a cardholder initiates a chargeback." During an inquiry a full refund is possible (a partial refund can still lead to a full chargeback); submit evidence of the refund too. If a refund is owed on an open chargeback, the cardholder must first drop the chargeback; then the merchant can refund.
