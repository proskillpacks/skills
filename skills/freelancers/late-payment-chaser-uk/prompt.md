# Late Payment Chaser (UK): prompt and template

Use this in any chatbot (ChatGPT, Claude, Gemini and others). Nothing to install.

**How to use it**
1. Have these ready: the unpaid amount, the invoice date, the date your client received it (if different), and the agreed payment date or terms, if there were any.
2. Copy everything from "COPY FROM HERE" to the end of this file and paste it into a new chat.
3. Under it, describe the invoice in your own words.

You get the statutory interest and fixed sum you can claim on a late UK business-to-business invoice, with the working shown, and three reminder emails. The installed skill works the figures out with a script and reads the Bank of England rate live; in this version the chatbot does the arithmetic and uses the rate table below, so check the working, and check the Bank of England page if the date is after December 2025. Not legal advice.

**Prefer to do it by hand?** Interest = unpaid amount × (8% + the base rate on the right reference date) ÷ 365 × days late, plus a fixed £40, £70 or £100. The rules and the rate table are below.

---

COPY FROM HERE

You are helping a UK business chase one late invoice from another business. Work only from the facts given below and the rules and table in this prompt. Do not use anything from memory about UK law. This is arithmetic on published rules plus drafting, not legal advice; say that once.

Rules (quoted from GOV.UK and the Late Payment of Commercial Debts (Interest) Act 1998):
- The Act applies "where the purchaser and the supplier are each acting in the course of a business". If the client is a private individual, no statutory interest or fixed sum: write reminders without them.
- Agreed payment date: interest starts the day after it. "If you agree a payment date, it must usually be within 30 days for public authorities or 60 days for business transactions." "You can agree a longer period than 60 days for business transactions - but it must be fair to both businesses."
- No agreed date: "the law says the payment is late 30 days after either: the customer gets the invoice; you deliver the goods or provide the service (if this is later)". The last day to pay on time is the 30th day counting the day the client got the invoice as day 1 (so: that date plus 29 days). Interest starts the next day. If the user doesn't say when the client got the invoice, assume the invoice date, say so, and add [CONFIRM: date the client received the invoice].
- Rate: "8 per cent per annum over the official dealing rate in force on the 30th June (in respect of interest which starts to run between 1st July and 31st December) or the 31st December (in respect of interest which starts to run between 1st January and 30th June)" immediately before. The rate then stays fixed for that debt.
- Fixed sum, once per invoice: "for a debt less than £1000, the sum of £40; for a debt of £1000 or more, but less than £10,000, the sum of £70; for a debt of £10,000 or more, the sum of £100".
- A contract with its own late-payment interest clause: GOV.UK says "You cannot claim statutory interest if there's a different rate of interest in a contract", but section 8 says that holds only if the clause is a "substantial remedy". Use the contract rate, give the statutory figure beside it as a comparison, and say which one applies is a question for a solicitor. Don't add the fixed sum in that case.
- "Send a new invoice if you decide to add interest to the money you're owed."
- Use the amount as the user gives it. If they say "plus VAT", calculate on the figure given and add [CONFIRM: the unpaid invoice total], because the interest and the fixed-sum band can change with the total.

Bank of England base rate changes (date the rate took effect, rate). To find the rate "in force on" a reference date, use the last change on or before that date:
1998-06-04 7.5%; 1998-10-08 7.25%; 1998-11-05 6.75%; 1998-12-10 6.25%; 1999-01-07 6%; 1999-02-04 5.5%; 1999-04-08 5.25%; 1999-06-10 5%; 1999-09-08 5.25%; 1999-11-04 5.5%; 2000-01-13 5.75%; 2000-02-10 6%; 2001-02-08 5.75%; 2001-04-05 5.5%; 2001-05-10 5.25%; 2001-08-02 5%; 2001-09-18 4.75%; 2001-10-04 4.5%; 2001-11-08 4%; 2003-02-06 3.75%; 2003-07-10 3.5%; 2003-11-06 3.75%; 2004-02-05 4%; 2004-05-06 4.25%; 2004-06-10 4.5%; 2004-08-05 4.75%; 2005-08-04 4.5%; 2006-08-03 4.75%; 2006-11-09 5%; 2007-01-11 5.25%; 2007-05-10 5.5%; 2007-07-05 5.75%; 2007-12-06 5.5%; 2008-02-07 5.25%; 2008-04-10 5%; 2008-10-08 4.5%; 2008-11-06 3%; 2008-12-04 2%; 2009-01-08 1.5%; 2009-02-05 1%; 2009-03-05 0.5%; 2016-08-04 0.25%; 2017-11-02 0.5%; 2018-08-02 0.75%; 2020-03-11 0.25%; 2020-03-19 0.1%; 2021-12-16 0.25%; 2022-02-03 0.5%; 2022-03-17 0.75%; 2022-05-05 1%; 2022-06-16 1.25%; 2022-08-04 1.75%; 2022-09-22 2.25%; 2022-11-03 3%; 2022-12-15 3.5%; 2023-02-02 4%; 2023-03-23 4.25%; 2023-05-11 4.5%; 2023-06-22 5%; 2023-08-03 5.25%; 2024-08-01 5%; 2024-11-07 4.75%; 2025-02-06 4.5%; 2025-05-08 4.25%; 2025-08-07 4%; 2025-12-18 3.75%.
This table was read on 4 October 2026. If the reference date is after that, say the rate must be checked at bankofengland.co.uk.

Working (show every step):
1. Last day to pay on time, and the day interest starts.
2. Reference date (30 June or 31 December before the start day) and the base rate in force then; statutory rate = 8% + that rate.
3. Days late = from the start day to today (or the date the user gives), counting both days.
4. Daily interest = amount × rate ÷ 100 ÷ 365 (keep 4 decimal places). Interest = daily interest × days, rounded to the penny at the end.
5. Fixed sum from the band. Total = amount + interest + fixed sum.
Check the arithmetic a second time before you answer.

Answer in this shape, under 650 words:

# Late payment: [invoice ref or "your invoice"] · £[amount]
**Position on [date]:** one sentence: last day to pay on time, the day interest runs from, and the number of days. Add "Assumes the customer is a business" if the user didn't say.

## What you can claim
| Item | Amount | Basis |
(unpaid invoice; interest with days and rate; fixed sum; total today, and what it adds each day)
Then up to 4 short bullets: the working in brief, any assumption, any [CONFIRM].

## Emails
1. Friendly reminder (now): no mention of interest or the Act.
2. Firm reminder (7 to 14 days later): states the statutory position with the figures.
3. Final reminder (7 days later): asks for payment by a date, then says you will consider formal recovery. No threats.
Each under 130 words, with [CONFIRM: …] for names, invoice number and bank details.

## Before you send
Every [CONFIRM], one per line. Then: "UK business-to-business debts only. This is not legal advice."

If the amount or the invoice date is missing below, ask for both in one line and stop.

Here is my invoice:
