#!/usr/bin/env python3
"""
agent-ready-quick-check: 6 quick checks of how well AI shopping agents can read a
Shopify store, compared with a 99-store benchmark (references/study-benchmarks.json).

Usage:  python3 quick_check.py <store-url> [--json]

Read-only, standard library only. Every request sends the script's own user agent (never a browser
one) and obeys robots.txt for it, read as RFC 9309 says: 4xx = no rules, a server error or no answer =
the whole site is off limits. Waits 1 second between requests (about 15 in total). No cart, no checkout.
"""
import gzip, html, json, os, re, statistics, sys, time, urllib.error, urllib.parse, urllib.request, zlib

UA_OWN = "AgentReadyQuickCheck/1.0 (read-only; python-urllib)"
AI_LIVE = ["OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User", "Claude-SearchBot", "Claude-User", "Googlebot", "Bingbot"]
REVIEW_APPS = {"Judge.me": r"jdgm-|judge\.me/", "Yotpo": r"yotpo\.com|shopify://apps/yotpo", "Okendo": r"okendo\.io|shopify://apps/okendo",
               "Loox": r"loox\.io", "Stamped": r"stamped\.io", "Junip": r"junip\.co", "Reviews.io": r"reviews\.io/",
               "Trustpilot": r"widget\.trustpilot\.com", "Fera": r"fera\.ai", "Air Reviews": r"air-reviews"}
HERE = os.path.dirname(os.path.abspath(__file__))
_last = [0.0]


def get(url, ua=UA_OWN):
    wait = 1.0 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "text/html,application/json,*/*", "Accept-Encoding": "gzip, deflate"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            raw, enc, st, final = r.read(6_000_000), r.headers.get("Content-Encoding", ""), r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, "", url
    except Exception:
        return None, "", url
    try:
        raw = gzip.decompress(raw) if "gzip" in enc else (zlib.decompress(raw) if "deflate" in enc else raw)
    except Exception:
        pass
    return st, raw.decode("utf-8", "replace"), final


def parse_robots(txt):
    groups, cur, last_agent = [], None, False
    for line in txt.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]
        k = k.lower()
        if k == "user-agent":
            if cur is None or not last_agent:
                cur = {"agents": [], "rules": []}
                groups.append(cur)
            cur["agents"].append(v.lower()); last_agent = True
        elif k in ("allow", "disallow"):
            last_agent = False
            if cur is not None and v:
                cur["rules"].append((k == "allow", v))
        else:
            last_agent = False
    return groups


def allowed(groups, agent, path):
    a = agent.lower()
    named = [g for g in groups if a in g["agents"]]   # RFC 9309: exact product token, case-insensitive
    rules = [r for g in (named or [g for g in groups if "*" in g["agents"]]) for r in g["rules"]]
    best, ok = -1, True
    for is_allow, pat in rules:
        rx = "".join(".*" if c == "*" else re.escape(c) for c in pat.rstrip("$")) + ("$" if pat.endswith("$") else "")
        if re.match(rx, path) and (len(pat) > best or (len(pat) == best and is_allow)):
            best, ok = len(pat), is_allow
    return ok


def strip(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg|template)[^>]*>.*?</\1>", " ", h or "")
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", h))).strip()


def nwords(t):
    return len(re.findall(r"[A-Za-zÀ-ÿ0-9']+", t or ""))


def jsonld(h):
    out = []
    for m in re.findall(r'(?is)<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', h):
        for cand in (m.strip(), re.sub(r",\s*([}\]])", r"\1", m.strip())):
            try:
                o = json.loads(cand)
                break
            except Exception:
                o = None
        stack = o if isinstance(o, list) else [o]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                if isinstance(x.get("@graph"), list):
                    stack.extend(x["@graph"])
                out.append(x)
            elif isinstance(x, list):
                stack.extend(x)
    return out


def types(o):
    t = o.get("@type", [])
    return [t] if isinstance(t, str) else list(t or [])


def lst(x):
    return x if isinstance(x, list) else ([] if x is None else [x])


def check(store):
    if not store.startswith("http"):
        store = "https://" + store
    sp = urllib.parse.urlsplit(store)
    base = f"{sp.scheme}://{sp.netloc}"
    notes = []

    def load_robots(b):
        s_, t_, _ = get(b + "/robots.txt")
        if s_ and 200 <= s_ < 300:
            return s_, parse_robots(t_), False
        if s_ and 400 <= s_ < 500:
            return s_, [], False
        return s_, [{"agents": ["*"], "rules": [(False, "/")]}], True   # RFC 9309: unreadable = keep out
    rst, groups, closed = load_robots(base)
    may = lambda path: allowed(groups, "AgentReadyQuickCheck", path) if groups else True
    st, home, final = get(base + "/") if may("/") else (None, "", base)
    fs = urllib.parse.urlsplit(final or base)
    if fs.netloc and f"{fs.scheme}://{fs.netloc}" != base:
        base = f"{fs.scheme}://{fs.netloc}"
        rst, groups, closed = load_robots(base)
    if closed:
        notes.append(f"robots.txt returned {rst or 'no answer'}. Under RFC 9309 that means the whole site is off limits, so this check read nothing else; AI crawlers treat the store the same way until robots.txt loads.")

    # 1. AI access
    blocked = [a for a in AI_LIVE if groups and not (allowed(groups, a, "/") and allowed(groups, a, "/products/x"))]
    lst_, ltxt, _ = get(base + "/llms.txt") if may("/llms.txt") else (None, "", "")
    llms = lst_ == 200 and "<html" not in ltxt[:500].lower() and len(ltxt.strip()) > 20

    # catalog (with headless fallback to the bare domain)
    def products_at(b):
        if not may("/products.json"):
            return None
        s, body, _ = get(b + "/products.json?limit=250")
        try:
            return json.loads(body).get("products") if s == 200 else None
        except Exception:
            return None
    cat_base, products = base, products_at(base)
    if products is None and fs.netloc.startswith("www."):
        bare = f"{fs.scheme}://{fs.netloc[4:]}"
        products = products_at(bare)
        if products is not None:
            cat_base = bare
            notes.append(f"{base}/products.json was not available; the catalogue was read from {bare} (common on headless storefronts).")
    products = products or []

    # 5. descriptions
    desc = [nwords(strip(p.get("body_html"))) for p in products]
    desc80 = round(100 * sum(w >= 80 for w in desc) / len(desc)) if desc else None

    # sample up to 5 available, non-gift products; skip storefront 404s
    real = [p for p in products if "gift" not in (p.get("product_type") or "").lower() and "gift-card" not in p.get("handle", "")]
    avail = [p for p in real if any(v.get("available") for v in p.get("variants", []))] or real
    pool = avail[::max(1, len(avail) // 8)] + avail if avail else []
    if not pool:
        pool = [{"handle": h} for h in dict.fromkeys(re.findall(r'href="(?:/[a-z]{2}(?:-[a-z]{2})?)?/products/([a-z0-9\-_%]+)', home))]
    pages, seen = [], set()
    for p in pool:
        if len(pages) >= 5 or len(seen) >= 12:
            break
        if p["handle"] in seen or not may(f"/products/{p['handle']}"):
            continue
        seen.add(p["handle"])
        s, h, _ = get(f"{base}/products/{p['handle']}")
        if s != 200:
            continue
        js, jb, _ = get(f"{cat_base}/products/{p['handle']}.json")
        try:
            full = json.loads(jb)["product"] if js == 200 else None
        except Exception:
            full = None
        blocks = jsonld(h)
        prods = [o for o in blocks if set(types(o)) & {"Product", "ProductGroup"}]
        offers, ids, agg = [], set(), None
        for o in prods:
            agg = agg or o.get("aggregateRating")
            offers += [x for x in lst(o.get("offers")) if isinstance(x, dict)]
            for x in list(offers):
                offers += [y for y in lst(x.get("offers")) if isinstance(y, dict)]
            for hv in lst(o.get("hasVariant")):
                if isinstance(hv, dict):
                    offers += [y for y in lst(hv.get("offers")) if isinstance(y, dict)]
                    ids |= {k for k in hv if k.startswith("gtin") and hv.get(k)}
            ids |= {k for k in o if k.startswith("gtin") and o.get(k)}
        for x in offers:
            ids |= {k for k in x if k.startswith("gtin") and x.get(k)}
        txt = strip(h)
        counts = [int(x) for x in re.findall(r"data-number-of-reviews=['\"](\d+)", h)]
        counts += [int(x.replace(",", "")) for x in re.findall(r"(?i)\b(\d[\d,]*)\s+reviews?\b", txt)]
        if isinstance(agg, dict):
            try: counts.append(int(float(str(agg.get("reviewCount") or agg.get("ratingCount") or 0))))
            except Exception: pass
        imgs = (full or {}).get("images") or []
        pages.append({"handle": p["handle"], "product_ld": bool(prods),
                      "ship_return_ld": any(x.get("shippingDetails") or x.get("hasMerchantReturnPolicy") for x in offers) or any(o.get("hasMerchantReturnPolicy") for o in prods),
                      "gtin_ld": bool(ids), "rating_ld": bool(agg),
                      "reviews_visible": bool(agg) or (max(counts) if counts else 0) > 0,
                      "review_count": max(counts) if counts else None,
                      "review_apps": [k for k, rx in REVIEW_APPS.items() if re.search(rx, h, re.I)],
                      "alt_pct": round(100 * sum(bool((i.get("alt") or "").strip()) for i in imgs) / len(imgs)) if imgs else None})

    # 3. rating status (same rules as the benchmark)
    withrev = [p for p in pages if p["reviews_visible"]]
    apps = sorted({a for p in pages for a in p["review_apps"]})
    if withrev:
        share = sum(p["rating_ld"] for p in withrev) / len(withrev)
        rating = "schema_ok" if share >= 0.85 else ("partial" if share > 0 else "reviews_shown_no_schema")
    elif apps and all(p["review_count"] == 0 for p in pages if p["review_apps"]):
        rating = "zero_reviews"
    elif apps:
        rating = "js_only"
    else:
        rating = "no_reviews_app"
    alts = [p["alt_pct"] for p in pages if p["alt_pct"] is not None]
    alt_avg = round(sum(alts) / len(alts)) if alts else None
    P = bool(pages)
    results = {
        "ai_access": {"pass": (not blocked) and llms, "blocked_agents": blocked, "llms_txt": llms, "robots_found": rst == 200, "robots_unreadable": closed},
        "ship_returns_schema": {"pass": any(p["ship_return_ld"] for p in pages) if P else None,
                                "pages_with": sum(p["ship_return_ld"] for p in pages), "pages": len(pages)},
        "rating_schema": {"pass": rating == "schema_ok" if P else None, "status": rating, "apps": apps,
                          "pages_with_reviews": len(withrev), "pages_with_rating_ld": sum(p["rating_ld"] for p in withrev)},
        "gtin_schema": {"pass": any(p["gtin_ld"] for p in pages) if P else None, "pages_with": sum(p["gtin_ld"] for p in pages), "pages": len(pages)},
        "descriptions": {"pass": (desc80 >= 50) if desc80 is not None else None, "pct_products_80plus_words": desc80,
                         "median_words": int(statistics.median(desc)) if desc else None, "products_read": len(desc)},
        "alt_text": {"pass": (alt_avg >= 80) if alt_avg is not None else None, "avg_alt_pct": alt_avg, "products": len(alts)},
    }
    if not pages:
        notes.append("No product page could be read (blocked by robots.txt, or the storefront renders products only with JavaScript). Page-based checks are not measurable.")
    bench = json.load(open(os.path.join(HERE, "..", "references", "study-benchmarks.json")))
    passed = sum(1 for v in results.values() if v["pass"])
    measurable = sum(1 for v in results.values() if v["pass"] is not None)
    return {"store": base, "checked_at": time.strftime("%Y-%m-%d"), "passed": passed, "measurable": measurable,
            "results": results, "sampled_pages": [p["handle"] for p in pages], "notes": notes, "benchmark": bench}


LABEL = {"ai_access": "AI agents allowed in + llms.txt", "ship_returns_schema": "Shipping/returns in structured data",
         "rating_schema": "Star rating in structured data", "gtin_schema": "GTIN (barcode) in structured data",
         "descriptions": "Descriptions long enough (80+ words)", "alt_text": "Image alt text"}


def text(R):
    B = R["benchmark"]
    out = [f"AGENT-READY QUICK CHECK  {R['store']}  ({R['checked_at']})",
           f"Passed {R['passed']}/{R['measurable']} measurable checks. Median store in our {B['stores_measured']}-store study: {B['checks_passed_of_6']['median']}/6.", ""]
    for k, v in R["results"].items():
        res = "n/a" if v["pass"] is None else ("PASS" if v["pass"] else "GAP")
        ev = {k2: v2 for k2, v2 in v.items() if k2 != "pass"}
        out.append(f"[{res:4}] {LABEL[k]}  | study: {B['pass_pct'][k]}% of stores pass  | {json.dumps(ev)}")
    out.append(f"\nStudy medians: {B['median_pct_products_80plus_words']}% of products with 80+ words; "
               f"median description {B['median_store_median_description_words']} words; average alt-text share {B['median_avg_image_alt_pct']}%.")
    for n in R["notes"]:
        out.append("NOTE: " + n)
    out.append("Sampled product pages: " + ", ".join(R["sampled_pages"]))
    return "\n".join(out)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    R = check(args[0])
    print(json.dumps(R, indent=1) if "--json" in sys.argv else text(R))
