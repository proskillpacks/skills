---
name: shopify-alt-text-writer
description: Writes accessible, SEO-aware alt text for Shopify product images and outputs a CSV you can import into Shopify (plus a review sheet). Works from a store domain, a product URL, or a Shopify product export CSV (works offline, e.g. in a chat with no web access). It reads the product title, variant and image position, looks at the actual photos when it can, keeps good existing alt text, and flags products where a CSV import is risky. Use when someone asks to "write alt text for my Shopify images", "fix missing alt text", "add image alt tags to my products", "accessibility for product photos", "image SEO for my store", or pastes a myshopify / store URL and mentions alt text or images.
---

# Shopify alt text writer

Goal: every product image in the store gets alt text that (1) tells a screen-reader user what the photo shows, (2) names the product the way a shopper would search for it, and (3) can go into Shopify without edits.

Default behaviour: don't ask questions first. If the user gave a store URL, a product URL or an export CSV, start. Ask only if you have no store, product URL or file at all.

## Reading the store: only through the script
- **Fetch store pages only with `scripts/alt_text.py`.** Don't fetch them any other way: no curl or wget, no code of your own, no browser user agent and no retries under another name. The script sends an honest user agent and obeys the store's robots.txt (RFC 9309).
- **If the script prints `NOT FETCHED`** (robots.txt does not allow the page, or robots.txt itself could not be read), stop for that page. Otherwise ask the user to paste the text, and say why.
- **If the script returns an error or leaves a fact out**, say "not found by the script" and use a placeholder or ask the user to paste it. Never write a fetcher to get round it.
- **No shell at all?** Your assistant's own web-fetch tool may read the same public pages the script would (it identifies itself). Never use it for a page the script reported as not fetched, and don't use it to get round an error.

## Step 1. Get the image list

**If you can run Python** (any agent with a shell or code execution), use the helper. It needs only the standard library:

```bash
python3 <skill-dir>/scripts/alt_text.py fetch <store-domain | product-URL | products_export.csv | products.json> -o work.json [--max-products N] [--handles h1,h2]
```

**If the user uploaded a product export CSV** (Shopify admin > Products > Export), use that file. It's the best input: it already contains every image URL, its position, the existing alt text, and which variant uses which image. Both the older headers (`Handle`, `Image Src`, `Image Alt Text`, `Variant Image`) and the current ones (`URL handle`, `Product image URL`, `Image alt text`, `Variant image URL`) work. In a hosted chat sandbox the code environment often has no internet, so the `thumbs` step can't download photos (it prints `NO-IMAGE`). In that case, write from the product data (title, variant, filename, position, and any useful facts in the existing alt text). Say clearly that these weren't checked against the photos, and offer to look at a few key photos if the user uploads them. Don't stop to ask first.

- It pages through `/products.json`. That endpoint does **not** include existing alt text. For 60 products or fewer, `fetch` reads `/products/<handle>.json` for each product to get it. For bigger catalogs, **don't** use `--check-existing`, which is slow. The `thumbs` step checks existing alt text product by product, only for the batch you're working on. Never assume images have no alt text just because `/products.json` doesn't show any.
- Each image in `work.json` has: handle, title, vendor, type, options, position, src, a `thumb` URL (400px), `variant_label` (the colour or style the image is linked to), `view_hint` (taken from the filename, e.g. LEFT, SOLE, DETAIL), `existing_alt` and a rule-based `draft_alt`.
- The script prints counts. Report them: products, images, how many already have alt text, how many are missing it.

**If you can't run code, or a shell command is denied or fails:** switch to this path straight away. Don't stop to ask for permission.
1. Web-fetch `https://<store>/products/<handle>.json` for each product the user named (up to about 10 products). Ask the fetch tool to return, verbatim, `title`, `product_type`, `options`, `variants` (id, option1–3) and every `images[]` entry (`position`, `src`, `alt`, `variant_ids`). For a whole store, fetch `https://<store>/products.json?limit=10` and use the first 10 products, then say how to do the rest.
2. To look at a photo, web-fetch its `src` with `&width=400` added (or `?width=400` if there's no `?`). The fetch tool usually can't describe an image itself, but it **saves the image to a local file and gives you the path**. Open that path with your file-reading tool to see the photo.
3. Write the alt text (step 3), then output the CSV as a code block (step 4).

If you can't fetch at all, ask the user to open `https://<their-store>/products.json` in a browser, save the page, and upload it.

## Step 2. Look at the photos (this is what makes the alt text accurate)

Metadata alone can't tell you whether photo 3 is the sole, a lifestyle shot or a size chart. So look:

```bash
python3 <skill-dir>/scripts/alt_text.py thumbs work.json -d thumbs --batch 1 --size 40
```

This picks the next batch of images that need work, downloads 400px thumbnails, and prints `key  path  title  variant  view_hint  existing_alt` for each. Images need work if they have **no alt text, or weak alt text**: just the product title, a filename or slug (`Oatmeal-Highline-Nep-Crew-Sweater`), under 15 characters, or the same text on several images of one product. Use `--mode missing` to do only empty ones, or `--mode all` to redo everything. Open each thumbnail with your file/image reading tool and write the alt text while looking at it. If an existing alt has a useful fact that you can't see in the photo (e.g. "Model is 5'10", wearing size S"), keep that fact.

Batch size: one run covers about 40 images, rounded up to whole products. The last line says whether more batches remain. For up to about 120 images, do every batch. For a bigger catalog, do the first 120 images (or the products the user cares about most: best sellers, a collection, or new arrivals) by looking, and let the rest fall back to the rule-based draft. Say clearly how many were written from the photo and how many are drafts, and how to run the next batch (`--batch 4`, and so on).

If you can't view images, write from metadata (title, variant, view_hint, filename, position) and say in the summary that the text wasn't checked against the photos.

## Step 3. Write the alt text

Follow `references/alt-text-rules.md`. The short version:

- **Pattern:** `<what you see> ` with the product name worked in once, naturally. Example: `Women's Classic Flip Flop in Dusty Pink, seen from the left side on a white background`.
- **Length:** aim for 60–125 characters. Never over 125.
- Name the **product the way the title does** (brand if it's in the title, product type, key attribute), plus the **variant colour/material** if the image is linked to a variant or obviously shows one.
- Then say **what's specific to this photo**: angle (side, back, sole, top-down), close-up of a feature (stitching, texture, label, clasp), worn by a model (describe briefly: "worn with jeans"), in use / lifestyle (what's happening), packaging, size chart or infographic (state the key facts it shows if short).
- **Every image of a product gets a different alt text.** No "alternate view 3".
- Don't start with "Image of", "Photo of" or "Picture of". No keyword stuffing, no prices, no "buy now", no promo text, no emoji, no straight double quotes (they break CSVs; use ' if needed).
- Text in the image (e.g. "50% off", a size chart): include the key words if they carry meaning.
- Keep existing alt text that is already good (specific, accurate, under 125 chars). Replace it only if it's empty, just the filename, just the product title repeated on every image, or wrong. If the user says "overwrite all", use `--overwrite` in step 4.

Save what you write as JSON, one file per batch: `{"<key>": "<alt text>", ...}`, e.g. `alts_01.json`. The key is the `key` field from work.json (`handle#position`).

## Step 4. Build the CSV

```bash
python3 <skill-dir>/scripts/alt_text.py csv work.json alts_*.json -o <store>-alt-text
```

This writes:
- `<store>-alt-text-shopify-import.csv` with Shopify's current column names: `URL handle, Title, Product image URL, Image position, Image alt text`. One row per image; Title only on each product's first row.
- `<store>-alt-text-review.csv`: key, old alt, new alt, character count, and source (written from the photo / rule-based draft / kept existing).
- Products whose existing alt text was never checked (no batch reached them) and that have no new alt text are **left out of the CSV**, so nothing gets overwritten blindly. The script reports them as `skipped_products_not_checked`.
- Warnings: over 125 characters, duplicates within a product, "image of" openings. Fix any warning in the alt text you wrote, and run it again. Warnings on kept existing alt text are fine; mention them as "weak alt text to redo in a later batch".

Without a shell, output the same columns as a CSV code block (always, even for one product, in addition to the paste table). Keep the header exactly as above.

## Step 5. Tell the user how to apply it safely

Always include these points in your summary (short, plain English):

1. **Back up first:** Products > Export > All products (CSV).
2. **Test on one product:** delete every row except one product's rows, import with **Products > Import > "Overwrite products with matching handles"**, then check that product's images and alt text in the admin.
3. Then import the full file. The CSV lists **all** images for each product in their current order, because an overwrite import uses the image list in the file.
4. **Products with variant images** (`products_with_variant_images`): a CSV import may reset which photo shows for each colour. For those products the script writes `<store>-alt-text-paste-by-hand.csv` (product, image position, image URL, alt text to paste), so the owner can paste each one in the admin (Products > open product > click the image > "Add alt text") or hand it to a bulk-edit app. If every product has variant images, lead with the paste-by-hand file and say the import CSV is for stores without variant images.
5. Shopify re-downloads image URLs during an import. Don't run the import twice by mistake.

## Output to the user

1. One-line result: `N images across M products: X written from the photos, Y rule-based drafts, Z existing kept.`
2. A table of 5–8 before/after examples (image, old alt, new alt).
3. File paths (or the CSV block), including the paste-by-hand file if there is one.
4. The "apply safely" steps above, plus any products that need hand-pasting.
5. If drafts remain: the exact command for the next batch.

Don't claim SEO ranking gains or legal compliance. Alt text helps accessibility and image search; say only that.

## Rules
- **Unsure stays unsure.** Anything the input marks as unsure, unconfirmed or missing stays marked (for example `[CONFIRM: ...]`) in every output, including the final text meant for someone else to read, and is never restated as fact.
