#!/usr/bin/env python3
"""Recompute an invoice with exact decimal arithmetic. Standard library only.
Usage: python3 invoice_math.py lines.csv [--discount 10%|25.00] [--tax-rate 20] [--stated-total 123.45] [--stated-subtotal 100.00] [--stated-tax 20.00]
lines.csv has a header row with: description,qty,unit_price and optionally stated_line_total.
Discount: a percentage (10%) applied to the subtotal, or a fixed amount (25.00). Tax is applied after the discount.
Rounding: each line total is rounded to 2 places half up; discount and tax are rounded to 2 places half up. Prints every comparison."""
import argparse, csv, sys
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
D = lambda x: Decimal(str(x).replace(",", "").replace("£", "").replace("$", "").replace("€", "").strip())
q = lambda x: x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("--discount"); ap.add_argument("--tax-rate"); ap.add_argument("--stated-total"); ap.add_argument("--stated-subtotal"); ap.add_argument("--stated-tax")
a = ap.parse_args()
rows = list(csv.DictReader(open(a.csv, newline="", encoding="utf-8-sig")))
if not rows: sys.exit("no lines found")
diffs = 0; sub = Decimal(0)
print("line | qty x unit | recomputed | stated | difference")
for i, r in enumerate(rows, 1):
    try: qty, unit = D(r["qty"]), D(r["unit_price"])
    except (InvalidOperation, KeyError): print(f"{i} | could not read qty or unit_price in row: {r}"); diffs += 1; continue
    tot = q(qty * unit); sub += tot
    st = r.get("stated_line_total", "").strip()
    if st:
        try: d = tot - D(st); flag = "" if d == 0 else "  <-- DIFFERENT"; diffs += d != 0
        except InvalidOperation: d, flag = "?", "  <-- stated total not readable"
        print(f"{i} | {qty} x {unit} | {tot} | {st} | {d}{flag}")
    else: print(f"{i} | {qty} x {unit} | {tot} | (none) | -")
print(f"recomputed subtotal: {sub}")
if a.stated_subtotal:
    d = sub - D(a.stated_subtotal); print(f"stated subtotal: {a.stated_subtotal} | difference {d}{'  <-- DIFFERENT' if d else ''}"); diffs += d != 0
net = sub
if a.discount:
    disc = q(sub * D(a.discount[:-1]) / 100) if a.discount.endswith("%") else q(D(a.discount)); net = sub - disc
    print(f"discount: {a.discount} -> {disc}; after discount: {net}")
tax = Decimal(0)
if a.tax_rate:
    tax = q(net * D(a.tax_rate) / 100); print(f"tax at {a.tax_rate}% on {net}: {tax}")
if a.stated_tax:
    d = tax - D(a.stated_tax); print(f"stated tax: {a.stated_tax} | difference {d}{'  <-- DIFFERENT' if d else ''}"); diffs += d != 0
total = net + tax; print(f"recomputed total: {total}")
if a.stated_total:
    d = total - D(a.stated_total); print(f"stated total: {a.stated_total} | difference {d}{'  <-- DIFFERENT' if d else ''}"); diffs += d != 0
print(f"RESULT: {'all compared figures match' if not diffs else str(int(diffs)) + ' difference(s) found'}")
