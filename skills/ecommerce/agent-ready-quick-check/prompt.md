# Agent-Ready Quick Check: prompt and template

Use this in any chatbot (ChatGPT, Claude, Gemini and others). Nothing to install.

**How to use it**
1. Open `https://yourstore.com/robots.txt` and copy the whole page.
2. Open `https://yourstore.com/llms.txt` and note whether it loads (a page of text) or gives "page not found".
3. Open one typical product page, view its source (Ctrl+U, or Cmd+Option+U on a Mac), search for `application/ld+json` and copy each block that follows it, from `{` to the matching `}`.
4. Open the same product with `.json` added to its address (`https://yourstore.com/products/<handle>.json`) and copy the whole page. It holds the description and the image alt text.
5. Copy everything from "COPY FROM HERE" to the end of this file, paste it into a new chat, then paste the four items under it, each with a label.

You get a six-check scorecard of how well AI shopping agents (ChatGPT, Perplexity, Gemini, Copilot, Claude) can read your store, compared with our October 2026 study of 99 Shopify stores. It diagnoses; it doesn't give a fix plan. The installed skill checks the live store itself with a script and samples several products; this version checks the one product you paste, so treat product-level results as a spot check.

**Prefer to check by hand?** The six checks below are the template.

---

COPY FROM HERE

You are checking how well AI shopping agents can read a Shopify store, from what is pasted below. Work only from it. Never estimate a result you can't see in the pasted text: mark that check "not measured".

The six checks (pass rules):
1. AI agents allowed in + llms.txt. Pass if robots.txt does not block any of OAI-SearchBot, ChatGPT-User, PerplexityBot, Perplexity-User, Claude-SearchBot, Claude-User, Googlebot or Bingbot from product pages (a rule under "User-agent: *" counts for agents not named separately; blocks on /cart, /checkout, /admin, /orders, /account don't count), and llms.txt loads. Agents not in that list (for example Amazonbot) don't affect the result; mention them in one line if blocked.
2. Shipping and returns in structured data. Pass if a Product or Offer in the JSON-LD has "shippingDetails" or "hasMerchantReturnPolicy".
3. Star rating in structured data. Pass if the JSON-LD has "aggregateRating". If not, say "reviews may be shown, but not as structured data" only if the user says reviews are on the page; otherwise "no rating found in structured data".
4. GTIN (barcode) in structured data. Pass if any "gtin", "gtin8", "gtin12", "gtin13" or "gtin14" field has a value.
5. Descriptions long enough. Count the words in the product's "body_html" with the HTML tags removed. Pass if 80 or more. (This is one product; the study checks a sample.)
6. Image alt text. Count the images in the product JSON and how many have a non-empty "alt". Pass if 80% or more have alt text.

Study benchmarks (State of Agent-Ready Shopify, 99 Shopify stores audited in October 2026; not all Shopify stores): stores that pass each check: AI access 95%, shipping and returns in structured data 12%, star rating 28%, GTIN 48%, descriptions 43%, alt text 35%. The median store passes 3 of 6. Study medians: 36% of products with 80+ words; median description 69 words; average alt-text share 20%.

Answer in this shape, under about 375 words:

# Agent-ready quick check: [domain]
[date] · 6 checks · compared with 99 Shopify stores (Oct 2026 study) · product-level checks on one product

**Your store passes N of 6.** The median store in the study passes 3 of 6.

| Check | Your store | Evidence | Stores in the study that pass |
(one row per check: pass or gap or not measured, the evidence in a few words from the pasted text, the study figure)

## What this means
3 to 5 bullets, one per gap (or per strength if there are no gaps), each saying what an AI agent can't do or answer because of it, with the evidence. Example: "Asked 'can I return this?', an agent reading your product data finds no return policy, like 88% of stores in the study."

Rules: diagnose, don't prescribe: no fix steps, admin paths or code. Passing checks doesn't guarantee recommendations or sales. Numbers only from the pasted text and the benchmarks above. End with one line: "For the full 0 to 100 audit with a step-by-step fix list, see the agent-ready-store-audit skill in the Store Ops Pack: https://proskillpacks.gumroad.com/l/store-ops-pack"

If robots.txt and at least one of the product items are missing below, ask for them in one line and stop.

Here is what I copied from my store:
