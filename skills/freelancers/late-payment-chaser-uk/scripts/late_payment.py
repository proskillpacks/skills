#!/usr/bin/env python3
"""
late-payment-chaser-uk helper: work out what a UK business can claim on one late commercial invoice.

Usage:
  python3 late_payment.py --amount 3256.58 --invoice-date 2022-07-31 [options]

  --amount N              the unpaid amount of the invoice, in pounds (required)
  --invoice-date DATE     the day the customer got the invoice (required, YYYY-MM-DD)
  --delivered DATE        the day the goods were delivered or the service finished, if later than the invoice
  --due-date DATE         the agreed payment date, if one was agreed
  --terms-days N          or: agreed payment terms as days from the invoice date (e.g. 30)
  --customer TYPE         business (default) | public (public authority) | consumer
  --as-of DATE            work the interest out up to this day (default: today)
  --contract-rate PCT     the contract sets its own late-payment interest: PCT % a year (fixed)
  --contract-over-base PCT  ... or PCT % over the Bank of England base rate
  --offline               don't fetch the Bank Rate page; use the bundled snapshot
  --json                  print JSON instead of text

What it applies (sources are printed with the result):
  - Late Payment of Commercial Debts (Interest) Act 1998, sections 2, 4, 5A, 8 and 9
  - Late Payment of Commercial Debts (Rate of Interest) (No. 3) Order 2002, article 4
    (Scotland: the equivalent (Scotland) Order 2002, same wording)
  - GOV.UK "Late commercial payments: charging interest and debt recovery"
  - Bank of England Bank Rate history: tries the live page through polite.py (honest user agent, robots.txt per
    RFC 9309); the Bank's server currently refuses non-browser requests, so the bundled snapshot is used and named
Simple interest, 365-day year, rounded to the penny at the end. One invoice, no part payments.
This is arithmetic on published rules, not legal advice.
"""
import argparse, datetime, json, os, re, sys, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import polite  # noqa: E402  (shared honest fetcher: own user agent, robots.txt per RFC 9309, pacing)

TOOL = "late-payment-chaser-uk"

BOE_URL = "https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp"
GOVUK = "https://www.gov.uk/late-commercial-payments-interest-debt-recovery"
ACT = "https://www.legislation.gov.uk/ukpga/1998/20"
ORDER = "https://www.legislation.gov.uk/uksi/2002/1675/made"
HERE = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT = os.path.join(HERE, "..", "references", "bank-rate-history.json")


def d(s):
    try:
        return datetime.date.fromisoformat(s)
    except ValueError:
        sys.exit(f"'{s}' is not a date in YYYY-MM-DD form")


def fmt(x):
    return f"{x.day} {x.strftime('%B %Y')}"


def money(x):
    return f"£{x:,.2f}"


def bank_rate_changes(offline):
    """Return (changes sorted oldest first as [(date, rate)], source description)."""
    why = "you asked for --offline"
    if not offline:
        try:
            page, _ = polite.fetch(BOE_URL, TOOL, accept="text/html", tries=2, timeout=20)
            rows = re.findall(r'<td[^>]*>\s*(\d{1,2} \w{3} \d{2})\s*</td>\s*<td[^>]*>\s*([\d.]+)\s*</td>', page)
            out = []
            for ds, rate in rows:
                dt = datetime.datetime.strptime(ds, "%d %b %y").date()
                if dt > datetime.date.today() + datetime.timedelta(days=366):
                    dt = dt.replace(year=dt.year - 100)
                out.append((dt, float(rate)))
            if len(out) >= 20:
                return sorted(out), f"Bank of England Bank Rate history, read live from {BOE_URL}"
            why = "the live page had no rate table this script could read"
        except polite.RobotsDisallowed:
            why = "robots.txt keeps this helper out, so it was not fetched another way"
        except urllib.error.HTTPError as e:
            why = (f"the Bank's server refused this helper's honest request (HTTP {e.code}); "
                   "it is not disguised as a browser to get round that")
        except Exception as e:
            why = f"the page could not be reached ({e.__class__.__name__})"
    snap = json.load(open(SNAPSHOT, encoding="utf-8"))
    out = sorted((datetime.date.fromisoformat(a), float(b)) for a, b in snap["changes"])
    return out, (f"Bank of England Bank Rate history, bundled snapshot of {snap['fetched']} (the live page was not read: {why}). "
                 f"Check {BOE_URL} if a rate changed after that date.")


def rate_on(changes, day):
    cur = None
    for dt, rate in changes:
        if dt <= day:
            cur = (dt, rate)
    if cur is None:
        sys.exit(f"no Bank Rate on record for {day}")
    return cur


def reference_date(start):
    """Article 4: the 30 June or 31 December immediately before the day statutory interest starts to run."""
    if start.month >= 7:
        return datetime.date(start.year, 6, 30)
    return datetime.date(start.year - 1, 12, 31)


def compute(a):
    amount = round(a.amount, 2)
    if amount <= 0:
        sys.exit("--amount must be more than 0")
    if a.terms_days is not None and a.terms_days < 0:
        sys.exit("--terms-days cannot be negative")
    inv = d(a.invoice_date)
    base_day = max(inv, d(a.delivered)) if a.delivered else inv
    as_of = d(a.as_of) if a.as_of else datetime.date.today()
    agreed = d(a.due_date) if a.due_date else (inv + datetime.timedelta(days=a.terms_days) if a.terms_days is not None else None)
    res = {"amount": amount, "invoice_date": inv.isoformat(), "as_of": as_of.isoformat(), "customer": a.customer,
           "notes": [], "warnings": [], "sources": []}
    n = res["notes"].append
    w = res["warnings"].append

    if a.customer == "consumer":
        res["regime"] = "none"
        w("The customer is a consumer, not a business. The Late Payment of Commercial Debts (Interest) Act 1998 applies only "
          "\"where the purchaser and the supplier are each acting in the course of a business\" (section 2(1)). "
          "No statutory interest or fixed sum is calculated. You can still send reminders, and charge interest only if your contract says so.")
        res["sources"].append(f"Act 1998, section 2(1): {ACT}/section/2")
        return res

    # The relevant day (section 4): the last day on which payment is on time.
    day30 = base_day + datetime.timedelta(days=29)   # last day of "the period of 30 days beginning with" base_day
    day60 = base_day + datetime.timedelta(days=59)
    if agreed is None:
        relevant = day30
        n(f"No agreed payment date, so the 30-day rule applies: the last day to pay on time was {fmt(day30)} "
          f"(30 days beginning with {fmt(base_day)}, the later of the invoice and delivery). Section 4(2A)(b) and 4(2H).")
        w(f"The 30 days run from when the customer had notice of the amount (section 4(2H)(b)), usually the day they received "
          f"the invoice. This assumes they received it on {fmt(inv)}. If it arrived later, re-run with that date as --invoice-date: "
          "starting too early overstates the interest.")
    else:
        relevant = agreed
        n(f"Agreed payment date: {fmt(agreed)}. Section 4(2A)(a).")
        if a.customer == "public" and day30 < agreed:
            relevant = day30
            n(f"The customer is a public authority and the agreed date is more than 30 days out, so the 30-day date "
              f"({fmt(day30)}) is used instead. Section 4(2D).")
        elif a.customer == "business" and day60 < agreed and inv >= datetime.date(2013, 3, 16):
            w(f"The agreed date is more than 60 days after {fmt(base_day)}. Under section 4(2E)-(2F) the 60-day date "
              f"({fmt(day60)}) applies instead unless the longer term is \"not grossly unfair to the supplier\". "
              f"This calculation uses the agreed date ({fmt(agreed)}); interest could run from {fmt(day60 + datetime.timedelta(days=1))} if the term is unfair.")
    start = relevant + datetime.timedelta(days=1)
    if start < datetime.date(2002, 8, 7):
        sys.exit("Interest would start before 7 August 2002. The Act's rules for older debts are different and are not covered here.")
    if inv < datetime.date(2015, 6, 21):
        n("Section 4 as worded before 21 June 2015 applies to this invoice (subsections (2A) to (2I) were inserted by SI 2015/1336). "
          "For an agreed payment date or the 30-day rule the result is the same.")
    days = max(0, (as_of - relevant).days)
    res.update(relevant_day=relevant.isoformat(), interest_starts=start.isoformat(), days_late=days)

    changes, rate_source = bank_rate_changes(a.offline)
    res["sources"].append(rate_source)
    if "snapshot" in rate_source and reference_date(start) > changes[-1][0] and as_of > changes[-1][0]:
        w(f"The live Bank of England page was not read, and the bundled rate table ends at {fmt(changes[-1][0])}. "
          f"If the base rate changed after that, these figures are wrong: check {BOE_URL} before you send anything.")

    if days == 0:
        res["regime"] = "not_late"
        left = (start - as_of).days
        n(f"The invoice is not late yet on {fmt(as_of)}. It becomes late on {fmt(start)} ({left} day{'s' if left != 1 else ''} away). "
          "No interest or fixed sum can be claimed before then.")
        res["sources"].append(f"GOV.UK, When a payment becomes late: {GOVUK}")
        return res

    contract = a.contract_rate is not None or a.contract_over_base is not None
    if contract:
        res["regime"] = "contract"
        if a.contract_rate is not None:
            rate = a.contract_rate
            n(f"Contract rate: {rate:g}% a year, as you described it.")
        else:
            bdt, base = rate_on(changes, relevant)
            rate = base + a.contract_over_base
            n(f"Contract rate: {a.contract_over_base:g}% over base. Bank Rate on {fmt(relevant)} was {base:g}% "
              f"(in force since {fmt(bdt)}), so {rate:g}% a year. Check which base rate and which date your clause names.")
        w("Your contract sets its own late-payment interest. GOV.UK: "
          "\"You cannot claim statutory interest if there's a different rate of interest in a contract.\" "
          "This figure uses the contract rate. If the clause is not a substantial remedy (section 8), statutory interest may apply "
          "instead; see the comparison below. Which one applies is a legal question for a solicitor. "
          "The figure is simple interest at the contract rate as you described it; read the clause for its own rules (compounding, start date).")
        w("The £40 / £70 / £100 fixed sum is not included: section 5A gives it \"once statutory interest begins to run\", "
          "and if your contract term applies, statutory interest does not run. Whether you can still claim it depends on your contract; ask a solicitor if it matters.")
        res["fixed_sum"] = None
        # For comparison only: what the statutory regime would give if the clause is not a "substantial remedy".
        cref = reference_date(start)
        _, cbase = rate_on(changes, cref)
        cfixed = 40 if amount < 1000 else (70 if amount < 10000 else 100)
        cint = round(amount * (cbase + 8.0) / 100 / 365 * days + 1e-9, 2)
        res["statutory_comparison"] = {"rate": cbase + 8.0, "interest": cint, "fixed_sum": cfixed}
        w(f"For comparison only: section 8(2) says statutory interest is not carried \"where the parties agree a contractual remedy "
          f"for late payment of the debt that is a substantial remedy\"; section 8(4) makes a contractual interest term void if it "
          f"\"is not a substantial remedy\". If your clause were not a substantial remedy, statutory interest for the same {days} days "
          f"would be {money(cint)} at {cbase + 8.0:g}% (base rate {cbase:g}% on {fmt(cref)}) plus a {money(cfixed)} fixed sum. "
          "Whether a clause is a substantial remedy is a legal question this tool cannot answer. Do not put the comparison figure in a demand without advice.")
        res["sources"] += [f"Act 1998, sections 8 and 9 (contract terms, substantial remedy): {ACT}/section/8",
                           f"GOV.UK, Interest on late commercial payments: {GOVUK}/charging-interest-commercial-debt",
                           f"Act 1998, section 5A: {ACT}/section/5A"]
    else:
        res["regime"] = "statutory"
        ref = reference_date(start)
        bdt, base = rate_on(changes, ref)
        rate = base + 8.0
        n(f"Statutory rate: 8% over the Bank of England base rate in force on {fmt(ref)} (the reference date for interest "
          f"that starts to run on {fmt(start)}). Bank Rate on {fmt(ref)} was {base:g}% (set {fmt(bdt)}), so {rate:g}% a year. "
          "The rate stays fixed for this debt.")
        fixed = 40 if amount < 1000 else (70 if amount < 10000 else 100)
        res["fixed_sum"] = fixed
        res.update(reference_date=ref.isoformat(), base_rate=base)
        band = "less than £1,000" if fixed == 40 else ("£1,000 or more but less than £10,000" if fixed == 70 else "£10,000 or more")
        n(f"Fixed sum for recovery costs: {money(fixed)} (debt of {band}). Section 5A(2). Charged once for this invoice.")
        if a.customer == "public":
            n("The customer is a public authority: GOV.UK says \"You cannot use a lower interest rate if you have a contract with public authorities.\"")
        res["sources"] += [f"Rate of Interest (No. 3) Order 2002, article 4: {ORDER}",
                           f"Act 1998, section 4 (when interest starts): {ACT}/section/4",
                           f"Act 1998, section 5A (fixed sum): {ACT}/section/5A",
                           f"GOV.UK, Late commercial payments: {GOVUK}"]

    daily = amount * rate / 100 / 365
    interest = round(daily * days + 1e-9, 2)
    res.update(rate=rate, daily_interest=round(daily, 4), interest=interest)
    res["total"] = round(amount + interest + (res.get("fixed_sum") or 0), 2)
    n(f"Interest: {money(amount)} x {rate:g}% / 365 = {money(daily)} a day (unrounded {daily:.4f}). "
      f"{days} day{'s' if days != 1 else ''} from {fmt(start)} to {fmt(as_of)} inclusive = {money(interest)}.")
    return res


def render(res):
    L = ["LATE PAYMENT CALCULATION (UK, business-to-business)",
         f"Unpaid amount: {money(res['amount'])} · worked out to: {fmt(d(res['as_of']))} · customer: {res['customer']}", ""]
    for x in res["notes"]:
        L.append("- " + x)
    for x in res["warnings"]:
        L.append("! " + x)
    if res.get("regime") in ("statutory", "contract"):
        L += ["", "CLAIM SUMMARY",
              f"  Invoice amount still unpaid:   {money(res['amount'])}",
              f"  Interest to {fmt(d(res['as_of']))} ({res['days_late']} days at {res['rate']:g}%):   {money(res['interest'])}"]
        if res.get("fixed_sum"):
            L.append(f"  Fixed sum (section 5A):        {money(res['fixed_sum'])}")
        L += [f"  TOTAL on {fmt(d(res['as_of']))}:   {money(res['total'])}",
              f"  Interest keeps adding {money(res['daily_interest'])} for each further day unpaid."]
    L += ["", "SOURCES"] + ["  " + s for s in res["sources"]]
    L += ["", "Not legal advice. One invoice, simple interest, 365-day year, no part payments. Check the facts you entered."]
    return "\n".join(L)


def main():
    if len(sys.argv) == 1:
        sys.exit(__doc__)
    ap = argparse.ArgumentParser(add_help=True, description="Late payment calculation (UK). Run with no arguments for the full notes.")
    ap.add_argument("--amount", type=float, required=True)
    ap.add_argument("--invoice-date", required=True)
    ap.add_argument("--delivered")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--due-date")
    g.add_argument("--terms-days", type=int)
    ap.add_argument("--customer", choices=["business", "public", "consumer"], default="business")
    ap.add_argument("--as-of")
    c = ap.add_mutually_exclusive_group()
    c.add_argument("--contract-rate", type=float)
    c.add_argument("--contract-over-base", type=float)
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    res = compute(a)
    print(json.dumps(res, indent=1) if a.json else render(res))


if __name__ == "__main__":
    main()
