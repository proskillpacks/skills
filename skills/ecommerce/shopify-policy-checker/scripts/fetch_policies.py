#!/usr/bin/env python3
"""Fetch a Shopify store's legal policies plus the shipping/returns claims made elsewhere on the site.
Python 3 standard library only.

Usage
  python3 fetch_policies.py <store-domain-or-url> [-o policies.md] [--pages faq,shipping-returns]

Output: one Markdown file with
  1. Each Shopify policy (/policies/<name>.json): refund, shipping, privacy, terms, contact, legal notice, subscription
  2. Store pages that commonly repeat policy terms (/pages/faq, /pages/shipping, /pages/returns, ...) if they exist
  3. "Claims" found on the homepage and one product page: sentences about shipping, returns, refunds,
     guarantees, warranty and delivery times (announcement bars and footers often contradict the policies)
"""
import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import polite  # noqa: E402  honest user agent + robots.txt (RFC 9309) for every request

TOOL = "shopify-policy-checker"
UA = polite.user_agent(TOOL)
POLICIES = ["refund-policy", "shipping-policy", "privacy-policy", "terms-of-service",
            "contact-information", "legal-notice", "subscription-policy"]
PAGES = ["shipping", "shipping-policy", "shipping-information", "shipping-returns", "shipping-and-returns",
         "returns", "return-policy", "returns-policy", "returns-exchanges", "returns-and-exchanges",
         "refund-policy", "faq", "faqs", "help", "warranty", "guarantee", "contact", "contact-us"]
CLAIM_RE = re.compile(r"(free (shipping|delivery|returns?)|ships? (in|within)|deliver(y|ed) (in|within)|"
                      r"\b\d+[- ]day|return|refund|exchange|money[- ]back|guarantee|warranty|"
                      r"business days|dispatch|same[- ]day|next[- ]day|duties|customs)", re.I)


SKIPPED = []


def fetch(url, accept="text/html"):
    """Every fetch goes through polite.fetch: honest user agent, robots.txt obeyed (RFC 9309).
    --owner skips the robots.txt check only (the user says it is their store)."""
    try:
        body, final = polite.fetch(url, TOOL, accept=accept, tries=4, owner="--owner" in sys.argv)
        return final, body
    except polite.RobotsDisallowed as e:
        SKIPPED.append(str(e))
        return None, None
    except Exception:
        return None, None


def html_to_text(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg|template)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</(p|div|li|h[1-6]|tr|section|details|summary)>", "\n", h)
    h = re.sub(r"(?i)<li[^>]*>", "- ", h)
    h = re.sub(r"(?i)<h([1-6])[^>]*>", lambda m: "\n" + "#" * (int(m.group(1)) + 2) + " ", h)
    h = re.sub(r"<[^>]+>", " ", h)
    h = html.unescape(h).replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in h.split("\n")]
    out, prev = [], None
    for l in lines:
        if l and l != prev:
            out.append(l)
        prev = l
    return "\n".join(out)


def main_content(page_html):
    m = re.search(r"(?is)<main[^>]*>(.*)</main>", page_html)
    return m.group(1) if m else page_html


TOS_RE = re.compile(r"(order|payment|price|pricing|ship|deliver|return|refund|cancel|exchange|warrant|guarantee|"
                    r"dispute|arbitrat|govern|law|jurisdiction|contact|chargeback|subscription|risk of loss|title)", re.I)


def relevant_paragraphs(text):
    keep = []
    for para in text.split("\n"):
        if para.startswith("#") or TOS_RE.search(para):
            keep.append(para)
    return "\n".join(keep)


def claims(text, limit=40):
    found = []
    for line in text.split("\n"):
        if 8 <= len(line) <= 300 and CLAIM_RE.search(line) and line not in found:
            found.append(line)
    return found[:limit]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("store")
    ap.add_argument("-o", "--out", default="policies.md")
    ap.add_argument("--pages", help="extra /pages/ handles to include, comma-separated")
    ap.add_argument("--owner", action="store_true", help="the user says this is their store: skip the robots.txt check only")
    a = ap.parse_args()
    s = a.store.strip()
    if not s.startswith("http"):
        s = "https://" + s
    u = urllib.parse.urlparse(s)
    base = f"{u.scheme}://{u.netloc}"
    out = [f"# Policy bundle for {base}", f"Fetched {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}", ""]
    summary = []

    out.append("## Part 1: Shopify policies (/policies/)")
    for p in POLICIES:
        _, body = fetch(f"{base}/policies/{p}.json", "application/json")
        text = ""
        if body:
            try:
                pol = json.loads(body).get("policy", {})
                text = html_to_text(pol.get("body") or "")
                meta = f"title: {pol.get('title')} | updated_at: {pol.get('updated_at')} | url: {pol.get('url')}"
            except Exception:
                text, meta = "", ""
        words = len(text.split())
        status = "MISSING" if not body else ("EMPTY" if words == 0 else (f"VERY SHORT, {words} words" if words < 40 else f"{words} words"))
        summary.append(f"- /policies/{p}: {status}")
        out.append(f"\n### /policies/{p} ({status})")
        if body and words:
            out.append(meta)
            out.append("")
            if p == "terms-of-service" and words > 2500:
                text = relevant_paragraphs(text)
                out.append("(Long terms of service: only paragraphs about orders, payment, shipping, returns, "
                           "refunds, cancellations, warranty, disputes, governing law and contact are included.)")
            out.append(text)
        time.sleep(0.3)

    out.append("\n## Part 2: Store pages that repeat policy terms (/pages/)")
    handles = PAGES + ([h.strip() for h in a.pages.split(",")] if a.pages else [])
    seen_final = set()
    for h in handles:
        final, body = fetch(f"{base}/pages/{h}")
        if not body or not final or final in seen_final or "/pages/" not in final:
            continue
        seen_final.add(final)
        text = html_to_text(main_content(body))
        if len(text.split()) < 20:
            continue
        summary.append(f"- page {final}: {len(text.split())} words")
        out.append(f"\n### {final}\n")
        out.append(text[:12000] + ("\n[...truncated]" if len(text) > 12000 else ""))
        time.sleep(0.3)

    out.append("\n## Part 3: Shipping / returns claims on the homepage and a product page")
    _, home = fetch(base + "/")
    pages = [("homepage", home)]
    _, pj = fetch(f"{base}/products.json?limit=1", "application/json")
    try:
        handle = json.loads(pj)["products"][0]["handle"]
        _, prod = fetch(f"{base}/products/{handle}")
        pages.append((f"/products/{handle}", prod))
    except Exception:
        pass
    for name, body in pages:
        if not body:
            continue
        c = claims(html_to_text(body))
        summary.append(f"- claims on {name}: {len(c)}")
        out.append(f"\n### {name}")
        out.extend(f"- {x}" for x in c) if c else out.append("(none found)")

    if SKIPPED:
        out.append("\n## Not fetched (robots.txt)")
        out.extend("- " + x for x in dict.fromkeys(SKIPPED))
        out.append("Don't fetch these pages any other way. If the user says this is their store, run again with --owner; otherwise ask them to paste the text.")
        summary.append(f"- not fetched because of robots.txt: {len(set(SKIPPED))} (see the end of the file)")
    out.insert(3, "## Summary\n" + "\n".join(summary) + "\n")
    open(a.out, "w", encoding="utf-8").write("\n".join(out))
    print("\n".join(summary))
    print(f"wrote {a.out} ({len(' '.join(out).split())} words)")


if __name__ == "__main__":
    main()
