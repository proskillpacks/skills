#!/usr/bin/env python3
"""Helper for the shopify-alt-text-writer skill. Python 3 standard library only.

Subcommands
  fetch   <store|product-url|products.json|product export .csv>  -> work.json (one entry per image, with facts + a draft alt)
  thumbs  work.json                           -> small JPG/PNG/WebP thumbnails to look at
  csv     work.json alts*.json                -> Shopify import CSV + review CSV + report

Examples
  python3 alt_text.py fetch example.com -o work.json --max-products 20
  python3 alt_text.py fetch https://example.com/products/some-handle -o work.json
  python3 alt_text.py fetch products_export.csv -o work.json
  python3 alt_text.py thumbs work.json -d thumbs --batch 1
  python3 alt_text.py csv work.json alts_*.json -o alt-text
"""
import argparse
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

TOOL = "shopify-alt-text-writer"
UA = polite.user_agent(TOOL)
MAX_ALT = 125  # screen readers handle longer, but ~125 chars is the common guidance

VIEW_WORDS = [  # (filename token regex, human phrase)
    (r"left", "left side view"), (r"right", "right side view"),
    (r"top|overhead|td|topdown|flatlay|flat", "top-down view"),
    (r"sole|bottom|outsole", "sole view"), (r"back|rear", "back view"),
    (r"front", "front view"), (r"side|profile|sd", "side view"),
    (r"3q|threequarter|angle", "three-quarter angle view"),
    (r"detail|macro|closeup|close|zoom|texture", "close-up detail"),
    (r"pair", "pair"), (r"swatch|armswatch", "colour swatch"),
    (r"model|onmodel|worn|fit|look\d*", "worn by a model"),
    (r"lifestyle|lifestyle\d*|scene|insitu", "lifestyle photo"),
    (r"pack|packaging|box", "packaging"), (r"infographic|chart|sizechart|size-chart", "infographic"),
]
NON_VARIANT_OPTIONS = {"size", "title", "length", "width", "waist", "inseam", "quantity", "amount", "value", "denominations"}


def norm_base(arg):
    """Return (base_url, handle_or_None) for a store domain / URL."""
    a = arg.strip()
    if not a.startswith("http"):
        a = "https://" + a
    u = urllib.parse.urlparse(a)
    base = f"{u.scheme}://{u.netloc}"
    m = re.search(r"/products/([^/?#.]+)", u.path)
    return base, (m.group(1) if m else None)


def get_json(url, tries=5):
    """Every fetch goes through polite.fetch: honest user agent, robots.txt obeyed (RFC 9309)."""
    body, _ = polite.fetch(url, TOOL, accept="application/json", tries=tries)
    return json.loads(body)


def _col(row, *names):
    for n in names:
        v = row.get(n)
        if v not in (None, ""):
            return v.strip()
    return ""


def load_export_csv(path):
    """Shopify product export CSV (legacy headers like 'Handle' / 'Image Src' or current ones like
    'URL handle' / 'Product image URL') -> list of products shaped like /products.json, with image alt."""
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig", newline="")))
    if not rows or not any(k in rows[0] for k in ("Handle", "URL handle")):
        sys.exit("error: this doesn't look like a Shopify product export (no 'Handle' / 'URL handle' column)")
    prods, order = {}, []
    for r in rows:
        h = _col(r, "Handle", "URL handle")
        if not h:
            continue
        if h not in prods:
            prods[h] = {"handle": h, "title": "", "vendor": "", "product_type": "", "status": "",
                        "options": [], "variants": [], "images": [], "_vimg": {}}
            order.append(h)
        p = prods[h]
        if _col(r, "Title") and not p["title"]:
            p["title"] = _col(r, "Title"); p["vendor"] = _col(r, "Vendor")
            p["product_type"] = _col(r, "Type", "Product type"); p["status"] = _col(r, "Status").lower()
            for i in (1, 2, 3):
                n = _col(r, f"Option{i} Name", f"Option{i} name")
                if n:
                    p["options"].append({"name": n, "values": []})
        vals = [_col(r, f"Option{i} Value", f"Option{i} value") for i in (1, 2, 3)]
        if any(vals):
            vid = len(p["variants"]) + 1
            v = {"id": vid}
            for i, val in enumerate(vals, 1):
                v[f"option{i}"] = val or None
                if val and i <= len(p["options"]) and val not in p["options"][i - 1]["values"]:
                    p["options"][i - 1]["values"].append(val)
            p["variants"].append(v)
            vimg = _col(r, "Variant Image", "Variant image URL")
            if vimg:
                p["_vimg"].setdefault(vimg.split("?")[0], []).append(vid)
        src = _col(r, "Image Src", "Product image URL")
        if src:
            pos = _col(r, "Image Position", "Image position")
            p["images"].append({"src": src, "position": int(pos) if pos.isdigit() else len(p["images"]) + 1,
                                "alt": _col(r, "Image Alt Text", "Image alt text") or None, "variant_ids": []})
    out = []
    for h in order:
        p = prods[h]
        for img in p["images"]:
            img["variant_ids"] = p["_vimg"].get(img["src"].split("?")[0], [])
        del p["_vimg"]
        out.append(p)
    return out


def load_products(src, max_products=None, handles=None):
    if os.path.exists(src) and src.lower().endswith(".csv"):
        prods = load_export_csv(src)
        if handles:
            prods = [p for p in prods if p["handle"] in handles]
        return None, prods[:max_products] if max_products else prods
    if os.path.exists(src):
        data = json.load(open(src, encoding="utf-8"))
        prods = data.get("products") or ([data["product"]] if "product" in data else data)
        return None, prods
    base, handle = norm_base(src)
    if handle:
        return base, [get_json(f"{base}/products/{handle}.json")["product"]]
    if handles:
        return base, [get_json(f"{base}/products/{h}.json")["product"] for h in handles]
    prods, page = [], 1
    while True:
        batch = get_json(f"{base}/products.json?limit=250&page={page}").get("products", [])
        if not batch:
            break
        prods.extend(batch)
        if max_products and len(prods) >= max_products:
            break
        page += 1
        time.sleep(0.5)
    return base, prods[:max_products] if max_products else prods


def filename(src):
    return urllib.parse.unquote(src.split("/")[-1].split("?")[0])


def view_hint(src):
    stem = filename(src).rsplit(".", 1)[0].lower()
    stem = re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "", stem)
    tokens = [t for t in re.split(r"[_\-\s\.]+", stem) if t]
    for pat, phrase in VIEW_WORDS:
        if any(re.fullmatch(pat, t) for t in tokens):
            return phrase
    return None


def variant_label(product, image):
    ids = set(image.get("variant_ids") or [])
    if not ids:
        return None
    opts = product.get("options") or []
    keep = [i for i, o in enumerate(opts) if (o.get("name") or "").strip().lower() not in NON_VARIANT_OPTIONS]
    vals = []
    for v in product.get("variants", []):
        if v.get("id") in ids:
            for i in keep:
                val = v.get(f"option{i + 1}")
                if val and val not in vals:
                    vals.append(val)
    return " / ".join(vals[:3]) or None


def draft_alt(title, var, view, pos):
    t = re.sub(r"\s+", " ", title).strip()
    parts = [t]
    if var and var.lower() not in t.lower():
        parts[0] = f"{t} in {var}"
    if view:
        parts.append(view)
    elif pos > 1:
        parts.append(f"alternate view {pos}")
    s = ", ".join(parts)
    return s[:MAX_ALT].rstrip(" ,")


def cmd_fetch(a):
    handles = [h.strip() for h in a.handles.split(",")] if a.handles else None
    base, prods = load_products(a.source, a.max_products, handles)
    check = a.check_existing if a.check_existing is not None else (base is not None and len(prods) <= 60)
    out = []
    for p in prods:
        existing = {}
        imgs = p.get("images") or []
        if any("alt" in i for i in imgs):
            existing = {i["src"]: i.get("alt") for i in imgs}
        elif check and base:
            try:
                full = get_json(f"{base}/products/{p['handle']}.json")["product"]
                existing = {i["src"]: i.get("alt") for i in full.get("images", [])}
                time.sleep(0.3)
            except Exception as e:  # keep going; mark unknown
                print(f"warn: could not read existing alt for {p['handle']}: {e}", file=sys.stderr)
        for img in sorted(imgs, key=lambda i: i.get("position", 0)):
            src = img["src"]
            var = variant_label(p, img)
            view = view_hint(src)
            pos = img.get("position", 0)
            sep = "&" if "?" in src else "?"
            out.append({
                "key": f"{p['handle']}#{pos}",
                "handle": p["handle"], "title": p["title"], "vendor": p.get("vendor"),
                "product_type": p.get("product_type"),
                "options": {o["name"]: o.get("values", [])[:12] for o in p.get("options", [])},
                "position": pos, "image_count": len(imgs), "src": src,
                "thumb": f"{src}{sep}width=400", "filename": filename(src),
                "variant_label": var, "has_variant_link": bool(img.get("variant_ids")),
                "view_hint": view,
                "existing_alt": existing.get(src) if existing else "UNKNOWN",
                "draft_alt": draft_alt(p["title"], var, view, pos),
            })
    json.dump({"store": base, "products": len(prods), "images": out}, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    has_alt = sum(1 for i in out if i["existing_alt"] not in (None, "", "UNKNOWN"))
    unknown = sum(1 for i in out if i["existing_alt"] == "UNKNOWN")
    print(f"products={len(prods)} images={len(out)} with_alt={has_alt} missing_alt={len(out) - has_alt - unknown} alt_unknown={unknown}")
    if not unknown:
        groups = {}
        for i in out:
            groups.setdefault(i["handle"], []).append(i)
        weak = sum(len(weak_alts(g)) for g in groups.values()) - (len(out) - has_alt)
        print(f"weak_existing_alt={weak} (title only, filename, very short, or the same text on several images)")
    else:
        print("existing alt text is checked per batch by the thumbs step (products.json doesn't include it)")
    print(f"variant_linked_images={sum(i['has_variant_link'] for i in out)} view_hint_found={sum(1 for i in out if i['view_hint'])}")
    inactive = sum(1 for p in prods if p.get("status") in ("draft", "archived"))
    if inactive:
        print(f"note: {inactive} products are draft or archived in the export; they're included")
    if base is None:
        print("source: local file. Existing alt text comes from the file. If thumbnails can't be downloaded "
              "(no network), write from the product data and say so.")
    print(f"wrote {a.out}")


def fill_existing(work, handle):
    """Read /products/<handle>.json to learn which images already have alt text (products.json omits it)."""
    if not work.get("store"):
        return False
    try:
        full = get_json(f"{work['store']}/products/{handle}.json")["product"]
    except Exception as e:
        print(f"warn: could not read existing alt for {handle}: {e}", file=sys.stderr)
        return False
    existing = {i["src"]: i.get("alt") for i in full.get("images", [])}
    for i in work["images"]:
        if i["handle"] == handle:
            i["existing_alt"] = existing.get(i["src"])
    time.sleep(0.3)
    return True


def weak_alts(imgs):
    """Keys of images whose existing alt is empty or weak: just the title, a filename, or repeated on several images."""
    weak = set()
    alts = [((i["existing_alt"] or "").strip().lower()) for i in imgs]
    for i, alt in zip(imgs, alts):
        if i["existing_alt"] == "UNKNOWN":
            continue
        stem = i["filename"].rsplit(".", 1)[0].lower()
        if (not alt or alt == i["title"].strip().lower() or alt == stem or alts.count(alt) > 1
                or len(alt) < 15 or re.match(r"^(img|dsc|image|photo)[_ -]?\d*", alt)
                or re.fullmatch(r"[\w'.*-]+", alt.split(" *")[0]) and ("-" in alt or "_" in alt)):
            weak.add(i["key"])
    return weak


def cmd_thumbs(a):
    work = json.load(open(a.work, encoding="utf-8"))
    by_handle = {}
    for i in work["images"]:
        by_handle.setdefault(i["handle"], []).append(i)
    batches, cur, changed, done_all = [], [], False, True
    handles = list(by_handle)
    for n, h in enumerate(handles):
        imgs = by_handle[h]
        if any(i["existing_alt"] == "UNKNOWN" for i in imgs):
            changed |= fill_existing(work, h)
        if a.mode == "all":
            cand = imgs
        elif a.mode == "missing":
            cand = [i for i in imgs if i["existing_alt"] in (None, "", "UNKNOWN")]
        else:  # missing + weak (default)
            wk = weak_alts(imgs)
            cand = [i for i in imgs if i["existing_alt"] in (None, "", "UNKNOWN") or i["key"] in wk]
        cur.extend(cand)
        if len(cur) >= a.size:
            batches.append(cur); cur = []
            if len(batches) == a.batch:
                done_all = n == len(handles) - 1
                break
    else:
        if cur:
            batches.append(cur)
    if changed:
        json.dump(work, open(a.work, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if len(batches) < a.batch:
        print(f"# no batch {a.batch}: all images are covered by batches 1-{len(batches)}")
        return
    sel = batches[a.batch - 1]
    os.makedirs(a.dir, exist_ok=True)
    failed = 0
    for i in sel:
        ext = os.path.splitext(i["filename"])[1].lower() or ".jpg"
        if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            ext = ".jpg"
        path = os.path.join(a.dir, re.sub(r"[^a-zA-Z0-9_-]", "_", i["key"]) + ext)
        if not os.path.exists(path):
            try:
                polite.check(i["thumb"], TOOL)   # robots.txt of the image host (Shopify's CDN)
                req = urllib.request.Request(i["thumb"], headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=30) as r, open(path, "wb") as f:
                    f.write(r.read())
            except Exception as e:
                print(f"warn: {i['key']}: could not download ({e})", file=sys.stderr)
                failed += 1
                path = "NO-IMAGE"
        old = i["existing_alt"] if i["existing_alt"] not in (None, "", "UNKNOWN") else ""
        print(f"{i['key']}\t{path}\t{i['title']}\t{i['variant_label'] or ''}\t{i['view_hint'] or ''}\t{old}")
    if failed:
        print(f"# {failed} of {len(sel)} thumbnails could not be downloaded (path NO-IMAGE). Write those from the "
              "product data, and don't describe what you can't see.")
    more = not done_all
    print(f"# batch {a.batch}: {len(sel)} images from {len({i['handle'] for i in sel})} products"
          + (f". More remain: run --batch {a.batch + 1}" if more else ". This is the last batch."))


BAD_START = re.compile(r"^(image|picture|photo|graphic) of\b", re.I)


def cmd_csv(a):
    work = json.load(open(a.work, encoding="utf-8"))
    alts = {}
    for pattern in a.alts:
        for f in sorted(glob.glob(pattern)) or [pattern]:
            d = json.load(open(f, encoding="utf-8"))
            if isinstance(d, list):
                d = {x["key"]: x["alt"] for x in d}
            alts.update(d)
    rows, review, warnings = [], [], []
    by_handle = {}
    for i in work["images"]:
        by_handle.setdefault(i["handle"], []).append(i)
    stats = {"written": 0, "from_draft": 0, "kept_existing": 0}
    by_title = {i["handle"]: i["title"] for i in work["images"]}
    kept_weak = 0
    variant_products = []
    skipped_unchecked = []
    for handle, imgs in list(by_handle.items()):
        if any(i["existing_alt"] == "UNKNOWN" and i["key"] not in alts for i in imgs):
            skipped_unchecked.append(handle)
            del by_handle[handle]
    for handle, imgs in by_handle.items():
        seen = set()
        if any(i["has_variant_link"] for i in imgs):
            variant_products.append(handle)
        for n, i in enumerate(imgs):
            ex = i["existing_alt"] if i["existing_alt"] != "UNKNOWN" else ""
            if i["key"] in alts:
                alt, source = alts[i["key"]], "written"
            elif ex and not a.overwrite:
                alt, source = ex, "kept_existing"
            else:
                alt, source = i["draft_alt"], "from_draft"
            alt = re.sub(r"\s+", " ", (alt or "")).strip().replace('"', "'")
            stats[source] += 1
            if source == "kept_existing":
                kept_weak += int(alt.lower() in seen or len(alt) < 15)
                seen.add(alt.lower())
                rows.append({"URL handle": handle, "Title": i["title"] if n == 0 else "",
                             "Product image URL": i["src"].split("?")[0], "Image position": i["position"],
                             "Image alt text": alt})
                review.append({"key": i["key"], "handle": handle, "position": i["position"], "old_alt": ex,
                               "new_alt": alt, "chars": len(alt), "source": source, "image_url": i["src"].split("?")[0]})
                continue
            if len(alt) > MAX_ALT:
                warnings.append(f"{i['key']}: {len(alt)} chars (> {MAX_ALT})")
            if BAD_START.match(alt):
                warnings.append(f"{i['key']}: starts with 'image of' / 'photo of'")
            if alt.lower() in seen and alt:
                warnings.append(f"{i['key']}: duplicate alt within product")
            seen.add(alt.lower())
            rows.append({"URL handle": handle, "Title": i["title"] if n == 0 else "",
                         "Product image URL": i["src"].split("?")[0], "Image position": i["position"],
                         "Image alt text": alt})
            review.append({"key": i["key"], "handle": handle, "position": i["position"], "old_alt": ex,
                           "new_alt": alt, "chars": len(alt), "source": source, "image_url": i["src"].split("?")[0]})
    if not rows:
        print("nothing to write: no product has all its images checked or written yet"); return
    with open(a.out + "-shopify-import.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open(a.out + "-review.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(review[0].keys())); w.writeheader(); w.writerows(review)
    print(f"rows={len(rows)} products={len(by_handle)} written_by_model={stats['written']} "
          f"draft_only={stats['from_draft']} kept_existing={stats['kept_existing']}")
    if skipped_unchecked:
        print(f"skipped_products_not_checked={len(skipped_unchecked)} (existing alt text unknown and no new alt written; "
              f"they are NOT in the CSV, so nothing gets overwritten. Run more thumbs batches to cover them.)")
    if variant_products:
        vp = set(variant_products)
        with open(a.out + "-paste-by-hand.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["URL handle", "Product title", "Image position", "Image URL", "Alt text to paste"])
            w.writeheader()
            for r in review:
                if r["handle"] in vp and r["source"] == "written":
                    w.writerow({"URL handle": r["handle"], "Product title": by_title.get(r["handle"], ""),
                                "Image position": r["position"], "Image URL": r["image_url"], "Alt text to paste": r["new_alt"]})
        print(f"products_with_variant_images={len(variant_products)} (all listed, with their new alt text, in {a.out}-paste-by-hand.csv)")
    else:
        print("products_with_variant_images=0")
    if kept_weak:
        print(f"kept_existing_but_weak={kept_weak} (existing alt text left as is because no batch has reached it yet)")
    print(f"warnings={len(warnings)} (on new alt text only)")
    for x in warnings[:40]:
        print("  " + x)
    print(f"wrote {a.out}-shopify-import.csv and {a.out}-review.csv")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    f = sp.add_parser("fetch"); f.add_argument("source"); f.add_argument("-o", "--out", default="work.json")
    f.add_argument("--max-products", type=int); f.add_argument("--handles")
    f.add_argument("--check-existing", dest="check_existing", action="store_true", default=None)
    f.add_argument("--no-check-existing", dest="check_existing", action="store_false")
    t = sp.add_parser("thumbs"); t.add_argument("work"); t.add_argument("-d", "--dir", default="thumbs")
    t.add_argument("--batch", type=int, default=1); t.add_argument("--size", type=int, default=40)
    t.add_argument("--mode", choices=["weak", "missing", "all"], default="weak",
                   help="weak (default): missing alt + weak alt (title only, filename, repeated); missing: only empty; all: every image")
    c = sp.add_parser("csv"); c.add_argument("work"); c.add_argument("alts", nargs="*")
    c.add_argument("-o", "--out", default="alt-text"); c.add_argument("--overwrite", action="store_true")
    a = ap.parse_args()
    {"fetch": cmd_fetch, "thumbs": cmd_thumbs, "csv": cmd_csv}[a.cmd](a)


if __name__ == "__main__":
    main()
