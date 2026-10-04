# Official sources (quoted)

Quotes fetched from the official pages on 4 October 2026. Quote these words; don't restate them from memory. Jurisdiction: United Kingdom. The Act covers business-to-business debts.

## GOV.UK: Late commercial payments: charging interest and debt recovery
https://www.gov.uk/late-commercial-payments-interest-debt-recovery

When a payment becomes late:
> "You can claim interest and debt recovery costs if another business is late paying for goods or a service."
> "If you agree a payment date, it must usually be within 30 days for public authorities or 60 days for business transactions."
> "You can agree a longer period than 60 days for business transactions - but it must be fair to both businesses."
> "If you do not agree a payment date, the law says the payment is late 30 days after either: the customer gets the invoice; you deliver the goods or provide the service (if this is later)"

Interest on late commercial payments:
> "The interest you can charge if another business is late paying for goods or a service is 'statutory interest' - this is 8% plus the Bank of England base rate for business to business transactions. You cannot claim statutory interest if there's a different rate of interest in a contract."
> "You cannot use a lower interest rate if you have a contract with public authorities."
> "Send a new invoice if you decide to add interest to the money you're owed."

GOV.UK's worked example: "If your business were owed £1,000 and the Bank of England base rate were 0.5%: the annual statutory interest on this would be £85 (1,000 x 0.085 = £85); divide £85 by 365 to get the daily interest: 23p a day (85 / 365 = 0.23); after 50 days this would be £11.50 (50 x 0.23 = 11.50)". The script does not round the daily figure before multiplying, so for the same example it gives £11.64. Both follow the same rule; the difference is rounding.

Claim debt recovery costs on late payments:
> "You can also charge a business a fixed sum for the cost of recovering a late commercial payment on top of claiming interest from it."
> "The amount you're allowed to charge depends on the amount of debt. You can only charge the business once for each payment."

| Amount of debt | What you can charge |
|---|---|
| Up to £999.99 | £40 |
| £1,000 to £9,999.99 | £70 |
| £10,000 or more | £100 |

> "If you're a supplier, you can also claim for reasonable costs each time you try to recover the debt."

## Late Payment of Commercial Debts (Interest) Act 1998
https://www.legislation.gov.uk/ukpga/1998/20

Section 2(1), which contracts:
> "This Act applies to a contract for the supply of goods or services where the purchaser and the supplier are each acting in the course of a business, other than an excepted contract."

Section 4, when interest runs:
> "(2) Statutory interest starts to run on the day after the relevant day for the debt, at the rate prevailing under section 6 at the end of the relevant day."
> "(2A) The relevant day for a debt is— (a) where there is an agreed payment day, that day, unless a different day is given by subsection (2D), (2E) or (2G); (b) where there is not an agreed payment day, the last day of the relevant 30-day period."
> "(2D) Where— (a) the purchaser is a public authority, and (b) the last day of the relevant 30-day period falls earlier than the agreed payment day, the relevant day is the last day of the relevant 30-day period"
> "(2E) Where— (a) the purchaser is not a public authority, and (b) the last day of the relevant 60-day period falls earlier than the agreed payment day, the relevant day is the last day of the relevant 60-day period"
> "(2F) But subsection (2E) does not apply (and so the relevant day is the agreed payment day…) if the agreed payment day is not grossly unfair to the supplier"
> "(2H) "The relevant 30-day period" is the period of 30 days beginning with the later or latest of— (a) the day on which the obligation of the supplier to which the debt relates is performed; (b) the day on which the purchaser has notice of the amount of the debt…"

Section 5A, the fixed sum:
> "(1) Once statutory interest begins to run in relation to a qualifying debt, the supplier shall be entitled to a fixed sum (in addition to the statutory interest on the debt)."
> "(2) That sum shall be– (a) for a debt less than £1000, the sum of £40; (b) for a debt of £1000 or more, but less than £10,000, the sum of £70; (c) for a debt of £10,000 or more, the sum of £100."

Sections 8 and 9, contracts with their own late-payment term:
> "8 (1) Any contract terms are void to the extent that they purport to exclude the right to statutory interest in relation to the debt, unless there is a substantial contractual remedy for late payment of the debt."
> "8 (2) Where the parties agree a contractual remedy for late payment of the debt that is a substantial remedy, statutory interest is not carried by the debt (unless they agree otherwise)."
> "8 (4) Any contract terms are void to the extent that they purport to— (a) confer a contractual right to interest that is not a substantial remedy for late payment of the debt…"
> "9 (1) A remedy for the late payment of the debt shall be regarded as a substantial remedy unless— (a) the remedy is insufficient either for the purpose of compensating the supplier for late payment or for deterring late payment; and (b) it would not be fair or reasonable to allow the remedy to be relied on to oust or (as the case may be) to vary the right to statutory interest that would otherwise apply in relation to the debt."

Whether a particular clause is a "substantial remedy" is a legal judgement. The skill quotes these sections and gives the comparison figure from the script; it does not decide the point.

## Late Payment of Commercial Debts (Rate of Interest) (No. 3) Order 2002, article 4
https://www.legislation.gov.uk/uksi/2002/1675/made (England, Wales and Northern Ireland). Scotland has the Late Payment of Commercial Debts (Rate of Interest) (Scotland) Order 2002 with the same article 4: https://www.legislation.gov.uk/ssi/2002/336/made

> "The rate of interest for the purposes of the Late Payment of Commercial Debts (Interest) Act 1998 shall be 8 per cent per annum over the official dealing rate in force on the 30th June (in respect of interest which starts to run between 1st July and 31st December) or the 31st December (in respect of interest which starts to run between 1st January and 30th June) immediately before the day on which statutory interest starts to run."

This is why the script uses the base rate on the previous 30 June or 31 December, not today's rate, and keeps it fixed for the debt.

## Bank of England Bank Rate
https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp (the "official dealing rate"). The script tries this page with its own honest user agent (the Bank's server refused it on 4 October 2026); `bank-rate-history.json` is the snapshot it then uses, read from that page on 4 October 2026.

## What this skill does not cover
Disputed debts, part payments, contracts with their own late-payment clause beyond a simple rate, compound interest, court procedure and fees, and debts owed by consumers. For those, GOV.UK points to "Make a court claim for money" (https://www.gov.uk/make-court-claim-for-money); the Small Business Commissioner publishes guidance on unpaid invoices (https://www.smallbusinesscommissioner.gov.uk/help-and-guidance/all-advice/help-with-unpaid-invoices/).

Construction contracts, VAT treatment, insolvency and limitation periods have their own rules, which are not quoted here and which this skill does not state.
