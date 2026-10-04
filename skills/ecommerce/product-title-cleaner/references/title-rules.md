# Title rules and edge cases

## Anatomy

`[Brand*] [Product name / model] [Product type] [Key attribute*] - [Colour / variant*]`

`*` only when needed:
- **Brand:** include it in multi-brand stores. In single-brand stores, leave it out unless it's part of the product's name (e.g. a product line named after the brand).
- **Key attribute:** one attribute that separates this product from its neighbours (material, fit, scent, count, "Set of 2"). Not a list.
- **Colour / variant:** only when the store lists each colour as its own product.

## Casing

- Title Case: capitalise major words. Lowercase `a, an, and, as, at, but, by, for, in, of, on, or, the, to, with` unless first or after a separator.
- Keep: brand styling (`adidas`, `lululemon`, an all-caps store brand if the store writes it that way consistently), trademarks `™ ®`, acronyms (`NFL`, `USB-C`, `SPF`, `XL` if it's a product name and not a variant), model codes (`990v3`, `Air Jordan 3`), units (`oz`, `ml`, `lb`, `cm`).
- ALL CAPS words that are not acronyms or brand styling: convert them.

## Separators and punctuation

- One separator for the variant/colour part, the one the store uses most (usually ` - `). Normalise `–`, `—` and ` | ` to it.
- Keep `/` inside colour names (`Black / Sport Red`) if that's how the store writes colourways.
- Parentheses: only for fixed sizes or counts (`(1 lb)`, `(Set of 2)`), or a sole/trim colour if the store uses them consistently.
- No trailing punctuation, no `!`, `*`, `~`, emoji or decorative symbols.

## Remove (and suggest a tag or collection instead)

`New`, `NEW!`, `Sale`, `Hot`, `Best Seller`, `Limited`, `Last Call`, `Clearance`, `Free Shipping`, `X% Off`, `Gift Idea`, `Must-Have`, `BOGO`, years (`2024 Edition`) unless they're part of the product's name, SKUs and internal codes.

Exception: if removing one makes two products' titles identical, keep the original word (normalised, e.g. `- Last Call`) and flag the pair for the owner to decide.

## Sizes and measurements

- Size is a Shopify option → remove it from the title.
- Size is fixed (one variant, e.g. a 12 oz bag, a 20 oz bottle) → keep it, in one consistent format: `(12 oz)`.
- Pack counts: `Set of 2`, `3-Pack`. Pick one style per catalog.

## Don't

- Don't invent material, fit, fabric, scent, or features. Use only words in the title, product type, options, tags or vendor.
- Don't translate titles or change the language.
- Don't rewrite brand-new names for products ("The Prowls" stays "The Prowls"). Add the product type around the name if it's missing.
- Don't touch skipped products (gift cards, content or placeholder products, `(Copy)` items, add-ons such as warranty or shipping protection).
- Don't change titles that are already fine just to make them look different.

## Examples (illustrative, not from a real store)

| Before | After | Why |
|---|---|---|
| `NEW!! Linen Duvet Cover QUEEN - white` | `Linen Duvet Cover - White` | promo removed; size is an option; casing |
| `organic cotton tee` | `Organic Cotton T-Shirt` | casing; type as written in product type |
| `The Ranger \| Waxed Canvas Backpack \| Olive` | `The Ranger Waxed Canvas Backpack - Olive` | one separator |
| `Cold Brew Coffee 12oz Bag - BEST SELLER` | `Cold Brew Coffee (12 oz)` | promo removed; fixed size formatted |
| `Classic Hoodie - LAST CALL` (and `Classic Hoodie` exists) | `Classic Hoodie - Last Call` + flag | removing it would duplicate another title |
