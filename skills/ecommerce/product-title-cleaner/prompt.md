# Product Title Cleaner: prompt and template

Use this in any chatbot (ChatGPT, Claude, Gemini and others). Nothing to install.

**How to use it**
1. In Shopify admin, go to Products > Export and export your products as CSV. Open it and copy these columns for up to about 150 products: URL handle (or Handle), Title, Vendor, Type, and the option names and values (Option1 name, Option1 value and so on). Pasting the header row and the rows is enough.
2. Copy everything from "COPY FROM HERE" to the end of this file and paste it into a new chat.
3. Under it, paste the rows.

You get one naming pattern for the catalog, new titles only where they help, and a two-column CSV (URL handle, Title) to import. The installed skill reads the whole store and checks every new title for duplicates with a script; in this version the chatbot checks duplicates within what you paste, so paste the whole catalog in batches if you can.

**Prefer to do it by hand?** The pattern rules below are the template.

---

COPY FROM HERE

You are cleaning up Shopify product titles so the catalog follows one consistent pattern. Work only from the rows pasted below. Change a title only where it helps; a title that is already right stays unchanged. Never invent materials, features, sizes or brands.

Anything I mark as unsure, unconfirmed or missing stays marked (for example [CONFIRM: ...]) in every output, including the final text meant for someone else to read, and is never restated as fact.

Step 1. Analyse: number of products, median and longest title length, which separators are used (" - ", " | ", ":") and how often, vendors, product types, duplicate titles, and issues (promo words, ALL CAPS, symbols or emoji, trailing punctuation, over 70 or 150 characters, product type missing from the title, sizes in the title, repeated brand).

Step 2. Pick the pattern most of the catalog already follows, in one line:
- Single-brand store: [Product name] [Product type] - [Colour]; leave the brand out.
- Multi-brand store: [Brand] [Model/Product name] [Product type] - [Colour].
- Consumables: [Product name] [Type] ([Size/Count]) when the size is fixed and not a variant.

Rules:
1. Variants stay out of the title: if Size (or another option) is a product option, don't put it in the title. Colour stays only when each colour is a separate product.
2. Remove promo and status words (NEW, SALE, Last Call, Free Shipping, Best Seller, emoji, "!!!"); suggest a tag or collection instead. If removing a word would make two titles identical, keep it and flag the pair.
3. Title Case for product names (small words like "and", "of", "with" lowercase unless first). Keep the brand's own styling, trademarks (™ ®), acronyms and model numbers.
4. Add the product type only if a shopper couldn't tell what the item is, using words from the store's own Type or title, and not past 70 characters unless the item is unclear without it.
5. One separator across the catalog (the store's most used). No trailing punctuation or double spaces.
6. Aim for 25 to 70 characters; never over 150.
7. Skip non-merchandise: gift cards, placeholder or "(Copy)" products, tests, shipping protection. List them as skipped.

Step 3. Write the new title for every product. Then check: no two products end up with the same title; nothing over 150 characters.

Answer in this shape:
1. The pattern in one line, and why (with a count from the data).
2. Counts: products checked, changed, unchanged, skipped (with reasons), titles over 70 characters before and after.
3. A before/after table of 8 to 12 typical changes, covering each kind of fix.
4. Flags that need a person: duplicates, brand-styling questions, unclear product types.
5. The import CSV in a code block, header "URL handle,Title", changed rows only. Quote any title that contains a comma.
6. How to import: back up first (Products > Export > All products); Products > Import, tick "Overwrite products with matching handles"; columns not in the file keep their values; URL handles don't change; check two or three products afterwards.
Keep the tone neutral. Don't promise traffic or ranking gains.

If no product rows are pasted below, ask for them in one line and stop.

Here are my products:
