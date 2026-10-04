---
name: product-title-cleaner
description: Cleans up messy Shopify product titles so the whole catalog follows one consistent pattern (brand, product type, key attribute, variant). It removes promo words, ALL CAPS, stray symbols and size clutter, keeps your product names and trademarks, and outputs a CSV you can import into Shopify (URL handle + Title, changed rows only) plus a before/after review sheet. Works from a store URL, a collection URL, a products.json file or a Shopify product export CSV. Use when someone says "clean up my product titles", "make my product names consistent", "standardize titles across my catalog", "fix ALL CAPS titles", "product naming convention for my Shopify store", or "bulk rename products".
---

# Product title cleaner

Goal: one naming pattern across the catalog, applied to every product, delivered as a CSV the owner can import as is. Change titles only where it helps. A clean catalog with 40 changes is better than 250 pointless rewrites.

Scope: this skill fixes the **product title** (the H1 on the product page, and what shows in collections, search and the Google/Shop feed). It doesn't write SEO titles, meta descriptions or product descriptions.

Don't ask questions first. Start from whatever the user gave you: a store domain, a `/collections/<handle>` URL (only that collection), a products.json file, or a product export CSV (Products > Export).

## Reading the store: only through the script
- **Fetch store pages only with `scripts/titles.py`.** Don't fetch them any other way: no curl or wget, no code of your own, no browser user agent and no retries under another name. The script sends an honest user agent and obeys the store's robots.txt (RFC 9309).
- **If the script prints `NOT FETCHED`** (robots.txt does not allow the page, or robots.txt itself could not be read), stop for that page. Otherwise ask the user to paste the text, and say why.
- **If the script returns an error or leaves a fact out**, say "not found by the script" and use a placeholder or ask the user to paste it. Never write a fetcher to get round it.
- **No shell at all?** Your assistant's own web-fetch tool may read the same public pages the script would (it identifies itself). Never use it for a page the script reported as not fetched, and don't use it to get round an error.

## Step 1. Load and analyse the catalog

**With a shell:**

```bash
python3 <skill-dir>/scripts/titles.py fetch <store | collection URL | products.json | export.csv> -o titles.json [--max-products N]
```

It prints an analysis: median and max length, which separators are used and how often (` - `, ` | `, `:`), vendors, product types, duplicate titles, and issue counts with examples (promo words, ALL CAPS, symbols or emoji, trailing punctuation, over 70 / 150 characters, product type missing from the title, sizes or measurements in the title, repeated brand). `titles.json` has, for each product, the handle, title, vendor, product type, options (with values) and cleaned tags.

**Without a shell:** fetch `https://<store>/products.json?limit=250` (or ask the user to paste titles, or upload the export CSV) and do the same analysis by eye.

## Step 2. Decide the pattern (from the store's own data)

Pick the pattern that **most of the catalog already follows** and that reads naturally, then write it down in one line, for example:

- Single-brand store (one vendor = the store): `[Product name] [Product type] - [Colour]`. Leave the brand out because it's everywhere already. Example: `Morrell Crew Sweater - Oatmeal`.
- Multi-brand store (many vendors): `[Brand] [Model/Product name] [Product type] - [Colour]`. Example: `Nike Air Max Dolce Women's Sneaker - Black / Sport Red`.
- Consumables: `[Product name] [Type] ([Size/Count])` when the size is fixed and not a variant. Example: `Dark Roast Whole Bean Coffee (1 lb)`.

Read `references/title-rules.md` for the full rules and edge cases. The most important ones:

1. **Variants stay out of the title.** If Size (or another option) is a Shopify option on the product, don't put it in the title. Colour stays in the title only when the store sells each colour as a **separate product** (handle per colour). Then keep it, after one consistent separator.
2. **Remove** promo words and status (`NEW`, `SALE`, `Last Call`, `Free Shipping`, `Best Seller`, `🔥`, `!!!`). Tell the owner to use a tag or collection for these instead. **But** if removing a word would make the title identical to another product's title (e.g. a "Last Call" duplicate of a full-price item), keep that word and flag the pair.
3. **Casing:** Title Case for product names (keep small words like "and", "of", "with" lowercase unless first). Keep brand styling exactly (`adidas`, `NEW BALANCE` → only if that's the brand's own style; otherwise `New Balance`), keep trademarks (™ ®), acronyms (`USB-C`, `SPF 30`, `NFL`) and model numbers (`990v3`).
4. **Product type** should be in the title if a shopper couldn't tell what it is otherwise (`The Prowls` → `The Prowls Boys' Lined Swim Trunk`). Use the words from the store's own product type, tags or existing title. Never invent materials or features. Don't add a type that pushes a title past 70 characters unless the item is genuinely unclear without it. Report how many titles are over 70 before and after; that number shouldn't go up much.
5. **One separator** across the catalog (the store's most used one, usually ` - `). Remove trailing punctuation and double spaces.
6. **Length:** aim for 25–70 characters. Hard maximum 150 (Google Shopping). Shopify's limit is 255.
7. **Skip non-merchandise products:** gift cards, internal or "Content" placeholder products, "(Copy)" duplicates, test products, warranty and shipping-protection add-ons. List them under "Skipped" and don't change them.
8. If a title is already right, **leave it unchanged.**

## Step 3. Write the new titles

Go through **every** product in `titles.json`. Write results as JSON (one file per batch of about 150 products is fine): 

```json
{"<handle>": {"title": "<new title>", "why": "removed promo 'Last Call'; title case"}, ...}
```

Include unchanged products too, with the same title and `"why": "ok"`, so nothing is missed.

## Step 4. Build the CSV

```bash
python3 <skill-dir>/scripts/titles.py csv titles.json new_*.json -o <store>-titles
```

Outputs:
- `<store>-titles-shopify-import.csv`: columns `URL handle,Title`, **changed rows only**.
- `<store>-titles-review.csv`: every product, with old title, new title, changed yes/no, length and what changed.
- Warnings: duplicates created, over 150 characters, products with no new title. When only part of the catalog is cleaned (a collection, or `--max-products`), `fetch` also reads every other title in the store, and `csv` flags any new title that would match one of them (`DUPLICATE: ... out-of-scope product`).
- **Fix every DUPLICATE warning** (usually by keeping the word you removed, e.g. `- Last Call`), then run `csv` again until there are 0 duplicate warnings. Don't hand over a file that creates duplicate titles.

Without a shell, output the import CSV as a code block with the header `URL handle,Title`.

## Step 5. Report to the user

1. The pattern in one line, and why (e.g. "92% of titles already use ' - ' before the colour").
2. Counts: products checked, changed, unchanged, skipped (with reasons), and how many titles are over 70 characters before and after.
3. A before/after table of 8–12 typical changes, covering each kind of fix.
4. Flags that need a human decision (duplicates, possible brand-styling questions, unclear product type).
5. How to import, short:
   - Back up: Products > Export > All products.
   - Products > Import > upload the CSV > tick **"Overwrite products with matching handles"**. Columns missing from the file keep their current values, so only the titles change.
   - Changing a title doesn't change the URL handle, so links and SEO URLs keep working.
   - Check 2–3 products in the admin afterwards.
   - If the store has a product feed (Google, Meta), the new titles flow through on the next sync. Apps that matched products by title (rare) may need checking.

Keep the tone neutral and factual (no comments on how messy or tidy the catalog is). Don't promise traffic or ranking gains. Consistent titles make the catalog easier to scan and search. Say only that.

## Rules
- **Unsure stays unsure.** Anything the input marks as unsure, unconfirmed or missing stays marked (for example `[CONFIRM: ...]`) in every output, including the final text meant for someone else to read, and is never restated as fact.
