# Shopify Alt Text Writer: prompt and template

Use this in any chatbot (ChatGPT, Claude, Gemini and others). Nothing to install.

**How to use it**
1. For each product, open `https://yourstore.com/products/<product-handle>.json` in your browser (the handle is the last part of the product's address) and copy the whole page. Or paste the product's title, options, and for each image its position, file address and current alt text.
2. If your chatbot accepts images, also upload the product photos, in the same order. It writes better alt text when it can see them.
3. Copy everything from "COPY FROM HERE" to the end of this file, paste it into a new chat, then paste the product data under it.

You get alt text for every image (under 125 characters, each one different), a CSV in Shopify's import format, and the steps to import it safely. The installed skill fetches products and photos itself with a script; in this version you paste the data, and without photos the alt text is written from the product data and file names, and it says so.

**Prefer to write it yourself?** The pattern and rules below are the template.

---

COPY FROM HERE

You are writing alt text for a Shopify store's product images. Good alt text tells a screen-reader user what the photo shows and names the product the way a shopper would search for it. Work only from the product data and photos given below.

Anything I mark as unsure, unconfirmed or missing stays marked (for example [CONFIRM: ...]) in every output, including the final text meant for someone else to read, and is never restated as fact.

Rules:
- Pattern: what the photo shows, with the product name worked in once, naturally. Example: "Women's Classic Flip Flop in Dusty Pink, seen from the left side on a white background".
- 60 to 125 characters; never over 125.
- Name the product as the title does, plus the variant colour or material if the image is linked to one or clearly shows one.
- Say what is specific to each photo: angle (side, back, sole, top-down), a close-up of a feature, worn by a model, in use, packaging, or a size chart (with its key facts if short). Every image of a product gets a different alt text; no "alternate view 3".
- If you can't see a photo, use the file name and position as hints (LEFT, BACK, SOLE, TD for top-down, 3Q for three-quarter view, DETAIL) and say in your summary that the text was not checked against the photos. Never describe colours, backgrounds or details you can't know.
- Don't start with "Image of", "Photo of" or "Picture of". No keyword stuffing, prices, promo text, emoji or straight double quotes (use ' if needed).
- Keep existing alt text that is already specific, accurate and under 125 characters. Replace it if it is empty, a file name, just the product title repeated, or wrong.
- Don't claim SEO ranking gains or legal compliance; alt text helps accessibility and image search.

Answer in this shape:
1. One line: "N images across M products: X written from the photos, Y from product data only, Z existing kept."
2. A table: image (handle and position), old alt text, new alt text, character count.
3. The import CSV in a code block, with exactly this header: URL handle,Title,Product image URL,Image position,Image alt text. One row per image, every image of each product in its current order; Title only on each product's first row.
4. How to apply it safely:
   - Back up first: Products > Export > All products (CSV).
   - Test on one product: keep only its rows, then Products > Import with "Overwrite products with matching handles", and check its images and alt text in the admin.
   - Then import the full file. Shopify re-downloads image addresses during an import, so don't run it twice by mistake.
   - Products where photos are linked to variants (for example one photo per colour): an import may reset which photo shows for each colour, so for those, paste the alt text by hand (Products > open the product > click the image > Add alt text).

If no product data is pasted below, ask for it in one line and stop.

Here is my product data:
