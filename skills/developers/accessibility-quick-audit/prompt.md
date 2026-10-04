# Accessibility quick audit: paste-in prompt

Works in ChatGPT, Claude, Gemini or any chatbot. Paste the page's HTML (in your browser: View source, copy) or the component code. Large pages: paste the main part and say what you left out.

---

You do a fast code-level accessibility review. Report only what the markup shows. Never say a page "is accessible" or "passes WCAG".

Target: WCAG 2.2 AA (change if needed). Key flows: [e.g. checkout, sign-up, or "none"]
Code: [paste]

Check: images with no alt, meaningless alt, icon-only controls with no name; form fields with no label, placeholder as the only label, missing autocomplete; empty or vague links and buttons, duplicate ids; heading order, missing h1, missing lang or title, missing landmarks, tables without headers; keyboard problems (tabindex above 0, click handlers on div or span with no role, outline removed, no skip link); ARIA misuse (conflicting roles, aria-hidden on focusable items, missing aria-expanded); text and background contrast where the colour values are visible (compute the ratio, show the numbers, 4.5:1 for normal text and 3:1 for large text and UI, else say "not checked"); media with no captions, autoplay, carousels with no pause; user-scalable=no in the viewport tag.

Output: a first line "Found N high-impact, M medium and K low issues in the code I read." Then each issue with what is wrong, the WCAG criterion (only if you are sure), a short quote of the offending code, who it affects in one sentence, and a fixed snippet. Group repeats. Label best practices as "good practice", not failures. Then "Needs a human check" (alt quality, reading order, focus order, screen reader announcements, caption accuracy) with a one-line test for each, and "Not checked" (JavaScript-added content, other pages, PDFs, third-party widgets). Quote real code only. This is not a legal audit. No em dashes.
