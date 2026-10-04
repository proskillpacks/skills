#!/usr/bin/env python3
"""Read-only profile of a CSV file. Standard library only. Never modifies the file.
Usage: python3 profile_csv.py file.csv [--max-rows 200000]
Prints a plain-text profile: rows, columns, per-column type, blanks, distinct values, numeric range, top values, and flags."""
import argparse, csv, re, statistics, sys
from collections import Counter
ap = argparse.ArgumentParser(); ap.add_argument("path"); ap.add_argument("--max-rows", type=int, default=200000); a = ap.parse_args()
raw = open(a.path, "rb").read()
for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
    try: text = raw.decode(enc); break
    except UnicodeDecodeError: continue
sample = text[:20000]
try: dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
except csv.Error: dialect = csv.excel
rows = list(csv.reader(text.splitlines(), dialect)); 
if not rows: sys.exit("empty file")
header, body = rows[0], rows[1:a.max_rows + 1]
print(f"file: {a.path} | encoding read as {enc} | delimiter {dialect.delimiter!r} | rows {len(body)}{' (capped)' if len(rows) - 1 > a.max_rows else ''} | columns {len(header)}")
ragged = sum(1 for r in body if len(r) != len(header)); print(f"rows with a different number of fields than the header: {ragged}")
dup_rows = sum(c - 1 for c in Counter(tuple(r) for r in body).values() if c > 1); print(f"exact duplicate rows: {dup_rows}")
num = re.compile(r"^[-+]?\d{1,3}(,\d{3})*(\.\d+)?$|^[-+]?\d+(\.\d+)?$"); dates = {"ISO yyyy-mm-dd": re.compile(r"^\d{4}-\d{2}-\d{2}"), "dd/mm/yyyy or mm/dd/yyyy": re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4}$"), "dd-Mon-yyyy": re.compile(r"^\d{1,2}[- ][A-Za-z]{3}[- ]\d{2,4}$")}
flags = []
for j, name in enumerate(header):
    col = [r[j].strip() if j < len(r) else "" for r in body]; filled = [v for v in col if v != ""]
    blanks = len(col) - len(filled); distinct = len(set(filled))
    kinds = Counter()
    for v in filled:
        if num.match(v): kinds["number"] += 1
        elif any(p.match(v) for p in dates.values()): kinds["date"] += 1
        elif v.lower() in ("true", "false", "yes", "no", "y", "n"): kinds["flag"] += 1
        else: kinds["text"] += 1
    main = kinds.most_common(1)[0][0] if kinds else "empty"
    line = f"- {name!r}: {main}, blank {blanks} ({100 * blanks // max(1, len(col))}%), distinct {distinct}"
    if main == "number":
        vals = [float(v.replace(",", "")) for v in filled if num.match(v)]
        line += f", min {min(vals):g}, median {statistics.median(vals):g}, max {max(vals):g}"
        if len(vals) >= 8:
            qs = statistics.quantiles(vals, n=4); iqr = qs[2] - qs[0]; out = [v for v in vals if v < qs[0] - 3 * iqr or v > qs[2] + 3 * iqr]
            if out and iqr > 0: flags.append(f"{name!r}: {len(out)} value(s) far outside the usual range (3 x IQR rule), for example {out[0]:g}")
        if any(re.match(r"^0\d+$", v) for v in filled): flags.append(f"{name!r}: values with leading zeros (a code, not a number?)")
    elif main == "text" and distinct <= 12 and filled: line += ", values: " + ", ".join(f"{k} ({c})" for k, c in Counter(filled).most_common(6))
    print(line)
    if len(kinds) > 1 and sum(kinds.values()) > 0 and kinds.most_common(2)[1][1] >= 1: flags.append(f"{name!r}: mixed content {dict(kinds)}")
    fm = Counter(k for v in filled for k, p in dates.items() if p.match(v))
    if len(fm) > 1: flags.append(f"{name!r}: dates in more than one format {dict(fm)}")
    if any(v != v.strip() for v in (r[j] for r in body if j < len(r))): flags.append(f"{name!r}: values with leading or trailing spaces")
    low = Counter(v.lower() for v in filled); variants = [k for k in low if len({v for v in filled if v.lower() == k}) > 1]
    if variants: flags.append(f"{name!r}: same value written in different cases, for example {variants[0]!r}")
    if distinct == 1 and len(filled) > 1: flags.append(f"{name!r}: constant column (one value)")
    if len(filled) == len(col) and distinct == len(col) and len(col) > 1 and (main != "number" or all("." not in v for v in filled)): flags.append(f"{name!r}: every value is different (possible ID column)")
    if blanks and blanks == len(col): flags.append(f"{name!r}: completely empty")
print("FLAGS:" if flags else "FLAGS: none found by these checks")
for f in flags: print("  *", f)
