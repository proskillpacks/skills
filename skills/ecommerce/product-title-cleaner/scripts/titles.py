#!/usr/bin/env python3
"""Helper for the product-title-cleaner skill. Python 3 standard library only.

Subcommands
  fetch    <store|products.json|products_export.csv>  -> titles.json + printed analysis of the catalog
  csv      titles.json new_titles*.json               -> Shopify import CSV (URL handle, Title) + review CSV

Examples
  python3 titles.py fetch example.com -o titles.json
  python3 titles.py fetch products_export.csv -o titles.json
  python3 titles.py csv titles.json new_*.json -o example-titles
"""
import argparse
import collections
import csv
import glob
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import polite  # noqa: E402  honest user agent + robots.txt (RFC 9309) for every request

TOOL = "product-title-cleaner"
UA = polite.user_agent(TOOL)
SEPARATORS = [" - ", " – ", " — ", " | ", " / ", ", ", ": ", " · "]
PROMO = re.compile(r"\b(new|sale|hot|best ?seller|free shipping|limited|last call|clearance|% ?off|deal|"
                   r"discount|gift idea|must[- ]have|bogo)\b", re.I)
NOISE_TAG = re.compile(r"(::|=>|^yblock|^ygroup|^oos|^loop|^wc |^_|^shoprunner|^\d)", re.I)


def get_json(url, tries=5):
    """Every fetch goes through polite.fetch: honest user agent, robots.txt obeyed (RFC 9309)."""
    body, _ = polite.fetch(url, TOOL, accept="application/json", tries=tries)
    return json.loads(body)


def from_store(arg, max_products):
    a = arg if arg.startswith("http") else "https://" + arg
    u = urllib.parse.urlparse(a)
    base = f"{u.scheme}://{u.netloc}"
    m = re.search(r"/collections/([^/?#]+)", u.path)
    path = f"/collections/{m.group(1)}/products.json" if m else "/products.json"
    prods, page = [], 1
    while True:
        batch = get_json(f"{base}{path}?limit=250&page={page}").get("products", [])
        if not batch:
            break
        prods.extend(batch)
        if max_products and len(prods) >= max_products:
            break
        page += 1
        time.sleep(0.5)
    return base, prods[:max_products] if max_products else prods


def all_store_titles(base, cap_pages=40):
    """Every product title in the store (for duplicate checks when only part of the catalog is cleaned)."""
    out, page = {}, 1
    while page <= cap_pages:
        try:
            batch = get_json(f"{base}/products.json?limit=250&page={page}").get("products", [])
        except Exception as e:
            print(f"warn: could not read the full catalog for duplicate checks: {e}", file=sys.stderr)
            break
        if not batch:
            break
        out.update({p["handle"]: p["title"] for p in batch})
        page += 1
        time.sleep(0.5)
    return out


def from_csv(path):
    """Shopify product export (old or new header names)."""
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    def col(r, *names):
        for n in names:
            if n in r and r[n]:
                return r[n]
        return ""
    prods = {}
    for r in rows:
        h = col(r, "Handle", "URL handle")
        if not h:
            continue
        p = prods.setdefault(h, {"handle": h, "title": "", "vendor": "", "product_type": "", "tags": [],
                                 "options": [], "variants": []})
        if col(r, "Title"):
            p["title"] = col(r, "Title"); p["vendor"] = col(r, "Vendor")
            p["product_type"] = col(r, "Type", "Product type")
            p["tags"] = [t.strip() for t in col(r, "Tags").split(",") if t.strip()]
            for i in (1, 2, 3):
                n = col(r, f"Option{i} Name", f"Option{i} name")
                if n:
                    p["options"].append({"name": n, "values": []})
        for i, o in enumerate(p["options"], 1):
            v = col(r, f"Option{i} Value", f"Option{i} value")
            if v and v not in o["values"]:
                o["values"].append(v)
    return None, list(prods.values())


def analyse(items):
    titles = [i["title"] for i in items]
    n = len(titles) or 1
    issues = collections.Counter()
    examples = collections.defaultdict(list)

    def flag(k, t):
        issues[k] += 1
        if len(examples[k]) < 5:
            examples[k].append(t)

    sep_count = collections.Counter()
    for i in items:
        t = i["title"]
        for s in SEPARATORS:
            if s in t:
                sep_count[s.strip() or s] += 1
        if t != t.strip() or "  " in t:
            flag("extra_spaces", t)
        letters = re.sub(r"[^A-Za-z]", "", t)
        if letters and letters.isupper() and len(letters) > 4:
            flag("all_caps", t)
        elif letters and letters.islower():
            flag("all_lowercase", t)
        if re.search(r"\b[A-Z]{4,}\b", t) and not (letters.isupper()):
            flag("shouting_word (check: brand/acronym?)", t)
        if PROMO.search(t):
            flag("promo_words_in_title", t)
        if re.search(r"[!?*~#]|[\U0001F300-\U0001FAFF]", t):
            flag("symbols_or_emoji", t)
        if re.search(r"[.,;:\-–|/]\s*$", t):
            flag("trailing_punctuation", t)
        if len(t) > 150:
            flag("over_150_chars (Google Shopping limit)", t)
        elif len(t) > 70:
            flag("over_70_chars (likely cut off in search results)", t)
        if len(t) < 12:
            flag("very_short (may lack product type)", t)
        v = (i.get("vendor") or "").strip()
        if v and t.lower().count(v.lower()) > 1:
            flag("brand_repeated", t)
        if re.search(r"\b(xs|s|m|l|xl|xxl|\d+(\.\d+)?\s?(oz|ml|cm|in|mm|g|kg|lb))\b", t, re.I):
            flag("contains_size_or_measure (fine if it's not a variant)", t)
        ptype = (i.get("product_type") or "").strip()
        if ptype and ptype.lower().rstrip("s") not in t.lower():
            flag("product_type_not_in_title", t)
    dup = [t for t, c in collections.Counter(x.lower() for x in titles).items() if c > 1]
    lengths = sorted(len(t) for t in titles)
    return {
        "products": len(titles),
        "median_length": lengths[len(lengths) // 2] if lengths else 0,
        "max_length": lengths[-1] if lengths else 0,
        "separator_usage": dict(sep_count.most_common()),
        "duplicate_titles": len(dup), "duplicate_examples": dup[:5],
        "vendors": dict(collections.Counter(i.get("vendor") or "" for i in items).most_common(8)),
        "product_types": dict(collections.Counter(i.get("product_type") or "" for i in items).most_common(12)),
        "issues": {k: {"count": c, "pct": round(100 * c / n), "examples": examples[k]} for k, c in issues.most_common()},
    }


def cmd_fetch(a):
    if os.path.exists(a.source) and a.source.lower().endswith(".csv"):
        base, prods = from_csv(a.source)
    elif os.path.exists(a.source):
        d = json.load(open(a.source, encoding="utf-8"))
        base, prods = None, d.get("products", d)
    else:
        base, prods = from_store(a.source, a.max_products)
    partial = bool(a.max_products) or "/collections/" in a.source
    others = {}
    if partial and base:
        allt = all_store_titles(base)
        scope = {p["handle"] for p in prods}
        others = {h: t for h, t in allt.items() if h not in scope}
    items = []
    for p in prods:
        opts = p.get("options") or []
        items.append({
            "handle": p["handle"], "title": p["title"], "vendor": p.get("vendor", ""),
            "product_type": p.get("product_type", ""),
            "options": {o["name"]: (o.get("values") or [])[:10] for o in opts if o.get("name") != "Title"},
            "tags": [t for t in (p.get("tags") or []) if not NOISE_TAG.search(t)][:12],
        })
    report = analyse(items)
    if others:
        lower = {}
        for h, t in others.items():
            lower.setdefault(t.lower(), h)
        report["out_of_scope_products"] = len(others)
        report["note"] = ("Only part of the catalog is being cleaned. The csv step also checks new titles against "
                          f"the other {len(others)} products in the store, so no duplicates get created.")
    json.dump({"store": base, "analysis": report, "products": items, "other_titles": others},
              open(a.out, "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print(f"wrote {a.out}")


def cmd_csv(a):
    data = json.load(open(a.work, encoding="utf-8"))
    old = {p["handle"]: p["title"] for p in data["products"]}
    new = {}
    for pattern in a.new:
        for f in sorted(glob.glob(pattern)) or [pattern]:
            d = json.load(open(f, encoding="utf-8"))
            if isinstance(d, list):
                d = {x["handle"]: x for x in d}
            for h, v in d.items():
                new[h] = v if isinstance(v, dict) else {"title": v}
    review, imp, warnings = [], [], []
    final = {h: re.sub(r"\s+", " ", (new.get(h, {}).get("title") or t)).strip() for h, t in old.items()}
    seen = collections.Counter(t.lower() for t in final.values())
    outside = {}
    for h, t in (data.get("other_titles") or {}).items():
        outside.setdefault(t.lower(), h)
    for h, t_old in old.items():
        v = new.get(h, {})
        t_new = re.sub(r"\s+", " ", (v.get("title") or t_old)).strip()
        changed = t_new != t_old
        if h not in new:
            warnings.append(f"{h}: no new title given, kept as is")
        if len(t_new) > 255:
            warnings.append(f"{h}: over Shopify's 255-char limit")
        if len(t_new) > 150:
            warnings.append(f"{h}: over 150 chars (Google Shopping)")
        if changed and seen[t_new.lower()] > 1:
            warnings.append(f"{h}: DUPLICATE: new title matches another product in this batch: {t_new}")
        if changed and t_new.lower() in outside:
            warnings.append(f"{h}: DUPLICATE: new title matches out-of-scope product '{outside[t_new.lower()]}': {t_new}")
        review.append({"URL handle": h, "Old title": t_old, "New title": t_new, "Changed": "yes" if changed else "no",
                       "Chars": len(t_new), "What changed": v.get("why", "")})
        if changed:
            imp.append({"URL handle": h, "Title": t_new})
    with open(a.out + "-shopify-import.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["URL handle", "Title"]); w.writeheader(); w.writerows(imp)
    with open(a.out + "-review.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(review[0].keys())); w.writeheader(); w.writerows(review)
    print(f"products={len(old)} changed={len(imp)} unchanged={len(old) - len(imp)} warnings={len(warnings)}")
    for x in warnings[:40]:
        print("  " + x)
    print(f"wrote {a.out}-shopify-import.csv (changed rows only) and {a.out}-review.csv (all rows)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    f = sp.add_parser("fetch"); f.add_argument("source"); f.add_argument("-o", "--out", default="titles.json")
    f.add_argument("--max-products", type=int)
    c = sp.add_parser("csv"); c.add_argument("work"); c.add_argument("new", nargs="+")
    c.add_argument("-o", "--out", default="titles")
    a = ap.parse_args()
    {"fetch": cmd_fetch, "csv": cmd_csv}[a.cmd](a)


if __name__ == "__main__":
    main()
