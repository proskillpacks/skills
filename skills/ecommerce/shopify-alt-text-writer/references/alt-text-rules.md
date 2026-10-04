# Alt text rules for product images

Sources this follows: W3C WAI images tutorial (informative images: describe the content that matters), Shopify Help Center "Adding alt text to media" (alt text describes the image for screen readers and search engines), and Google Search Central image SEO guidance (useful, information-rich alt text, no keyword stuffing).

## What good looks like (illustrative examples)

| Image | Bad | Good |
|---|---|---|
| Hero shot, white background | `IMG_4471` | `Men's canvas running sneaker in navy with a white sole, side view` |
| Same product, photo 4 | `Men's canvas running sneaker` (same as photo 1) | `Sole of the men's canvas running sneaker, showing the white rubber tread pattern` |
| Lifestyle | `Image of happy woman` | `Woman wearing the cable-knit crew sweater in oatmeal, walking on a forest trail` |
| Detail | `detail` | `Close-up of the ribbed cuff and chunky knit on the oatmeal crew sweater` |
| Packaging | `box` | `Dark roast whole bean coffee, front of the 1 lb bag` |
| Size chart | `size chart` | `Size chart for the boys swim trunk listing sizes with waist measurements in inches` |
| Bundle | `bundle` | `Ground coffee bundle: three bags side by side, dark, medium and espresso roasts` |

## Rules

1. **Describe what the photo shows.** Write it for someone who can't see the image and is deciding whether to buy.
2. **Name the product once**, the way the title does (brand + product type + key attribute). Don't repeat the name twice in one alt.
3. **Variant:** if the image is linked to a variant (`variant_label`) or clearly shows one colour or material, name it.
4. **What's specific to this photo:** the angle, the feature shown, the setting or the person. This is what makes alt texts in a gallery different from each other.
5. **Length:** 60–125 characters. Shorter is fine for simple swatches (`Dusty pink colour swatch for the flip flop`).
6. **Never:** "image of", "photo of", "picture of", file names, SKUs, prices, discounts (unless printed in the image and important), calls to action, emoji, hashtags, keyword lists, ALL CAPS.
7. **People:** describe the clothing and action, not the person's body or assumed traits. "Model wearing…" is fine.
8. **Don't invent:** if you can't see it and the metadata doesn't say it, don't claim a material, a feature or a colour. Without the photo, an infographic or collection shot gets only what its filename and the product data say (e.g. "Infographic for the …"), never a guess at its contents.
9. **Language:** write in the store's language (look at the product titles). Use the store's spelling (colour/color).
10. **Purely decorative images** (spacers, repeated brand backgrounds) are rare on product pages. If you find one, flag it in the summary instead of inventing a description.

## Rule-based draft (fallback)

When an image hasn't been looked at, the script's draft is: `<title> [in <variant>], <view from filename | "alternate view N">`. It's better than empty, but "alternate view N" is a placeholder. Report how many drafts contain it and recommend the next batch.
