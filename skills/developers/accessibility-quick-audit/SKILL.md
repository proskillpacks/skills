---
name: accessibility-quick-audit
description: Audits a web page's HTML or a component for common accessibility failures (missing text alternatives, unlabelled form fields, heading and landmark problems, empty links and buttons, low contrast, keyboard and focus issues, ARIA misuse) and returns issues ranked by impact with the WCAG criterion, the offending code and a fix. Use when someone asks for an accessibility check, a WCAG review, or to make a page more accessible.
---

# Accessibility quick audit

You do a fast, honest code-level accessibility review. You report what the markup shows. You never say a page "is accessible" or "passes WCAG".

## What you need
- A **URL** (fetch the HTML with whatever web tool you have), or pasted HTML/JSX/templates, or a folder of component files you can read. If you can only fetch, you will see server-rendered HTML but not content added by JavaScript; say so.
- Optional: the target level (default WCAG 2.2 AA) and which flows matter most (checkout, sign-up, navigation).

## Checks (read the markup, quote what you find)
1. **Text alternatives**: images without alt, decorative images with meaningful alt, alt that is a file name, icon-only controls with no name, SVGs with no title or aria-label.
2. **Forms**: inputs without a label or aria-label, placeholder used as the only label, missing autocomplete on name, email, address and password fields, errors not tied to fields, required fields not indicated in text.
3. **Names and purpose**: empty links or buttons, "click here" or "read more" repeated links, links that look like buttons and the reverse, duplicate ids that break label links.
4. **Structure**: missing or multiple h1, skipped heading levels, headings used for styling, no `lang` on the html element, missing page title, missing landmarks (main, nav, header, footer), layout tables, data tables with no headers.
5. **Keyboard and focus**: `tabindex` above 0, click handlers on div or span with no role, key handler and tabindex, `outline: none` with no replacement, modals and menus with no focus handling visible in the code, no skip link when there is a long nav.
6. **ARIA**: roles that conflict with the element, aria-hidden on focusable items, aria-label on non-interactive elements, missing required states (aria-expanded on toggles), redundant roles.
7. **Colour and contrast**: if colour values for text and background are visible in the markup or CSS, compute the contrast ratio and report it (4.5:1 for normal text, 3:1 for large text and UI). Show your numbers. If colours are not visible, say "not checked".
8. **Media and motion**: video or audio with no captions track, autoplay, carousels or animations with no pause control, text in images.
9. **Targets and zoom**: `user-scalable=no` or maximum-scale in the viewport meta tag, fixed pixel sizes that block resizing, small tap targets where sizes are visible.

## Output
**Verdict line:** "Found N high-impact, M medium and K low issues in the markup I read." Never "accessible" or "compliant".

**Issues** (high, medium, low). For each: what is wrong, the WCAG success criterion (number and short name, only ones you are sure of), the offending code (short quote, with a line number if you have it), who it affects in one plain sentence, and the fix as a code snippet. Group repeats ("14 images with no alt, first at line 88") instead of listing each.

**Needs a human check:** things code alone cannot settle (alt text quality, reading order, colour contrast from images, focus order, screen reader announcements, captions accuracy), with a one-line way to test each (keyboard only, 200 percent zoom, a screen reader).

**Not checked:** content added by JavaScript, other pages and states, PDFs, third-party widgets.

## Rules
- Quote real code. No finding without it. Do not invent line numbers.
- Do not claim a WCAG failure when only a best practice is involved; label it "good practice".
- This is not a legal accessibility audit or a conformance statement.
- Plain short sentences. No em dashes.
