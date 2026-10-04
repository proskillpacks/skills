# Free Agent Skills

Free, tested [Agent Skills](https://agentskills.io) in the plain `SKILL.md` format, grouped by profession. Each skill does one job from start to finish. Each folder also has a `prompt.md`, a paste-in version for ChatGPT or any chatbot without skills support.

They work in any assistant that reads `SKILL.md` files: Claude Code, OpenAI Codex, Gemini CLI, Cursor, GitHub Copilot and others. Helper scripts, where a skill has them, use only the Python 3 standard library. MIT licence.

## Skills by category

| Category | Skill | Give it | You get |
|---|---|---|---|
| E-commerce | [shopify-alt-text-writer](skills/ecommerce/shopify-alt-text-writer) | A store URL, product URL or product export CSV | Alt text for each product image, as a Shopify import CSV and a review sheet |
| E-commerce | [shopify-policy-checker](skills/ecommerce/shopify-policy-checker) | A store URL | An audit of refund, shipping, privacy, terms and contact policies, with paste-ready fixes |
| E-commerce | [product-title-cleaner](skills/ecommerce/product-title-cleaner) | A store, collection URL or export CSV | One consistent title pattern, as an import CSV of changed rows |
| E-commerce | [agent-ready-quick-check](skills/ecommerce/agent-ready-quick-check) | A store URL | A 6-check scorecard of how AI shopping agents read the store |
| E-commerce | [review-reply-drafter](skills/ecommerce/review-reply-drafter) | Pasted reviews, a CSV or a public review page | A reply for each review, with the ones that need you flagged |
| E-commerce | [chargeback-evidence-checklist](skills/ecommerce/chargeback-evidence-checklist) | The dispute reason | The evidence to gather before you write the response |
| Marketing and SEO | [ai-search-readiness-check](skills/marketing-seo/ai-search-readiness-check) | A website URL | A 0 to 100 score from 8 checks on whether AI search tools can read the site, plus a fix list |
| Marketing and SEO | [search-intent-page-brief](skills/marketing-seo/search-intent-page-brief) | A target keyword and the pages that rank for it | The search intent, a coverage table, the gaps and an outline for a new page |
| Freelancers | [late-payment-chaser-uk](skills/freelancers/late-payment-chaser-uk) | One late invoice | The statutory interest and fixed recovery sum worked out, and a chaser message (UK) |
| Writing | [fact-claim-checker](skills/writing/fact-claim-checker) | A draft you are about to publish | The claims that need a source, ranked by risk, with what would settle each and safer wording |
| Developers | [pr-description-and-review-prep](skills/developers/pr-description-and-review-prep) | A git diff or branch | A pull request description and the questions a reviewer is likely to ask |
| Developers | [accessibility-quick-audit](skills/developers/accessibility-quick-audit) | A page's HTML, a URL or component files | Accessibility issues ranked by impact, with the WCAG criterion, the code and a fix |
| Developers | [changelog-from-commits](skills/developers/changelog-from-commits) | A commit range or pasted git log | A user-facing changelog in Keep a Changelog style, with the commit behind each line and the vague commits flagged |
| Developers | [readme-first-run-check](skills/developers/readme-first-run-check) | A repository (or the README and manifests) | Every setup step marked OK, BROKEN, MISSING or UNVERIFIED with evidence, and the README edits that fix it |
| Developers | [test-gap-finder](skills/developers/test-gap-finder) | A diff and the project's tests | The behaviours the change adds or alters, each marked Covered, Not covered or Unknown, and ranked test cases for the gaps |
| Developers | [skill-portability-check](skills/developers/skill-portability-check) | A skill folder or a repository of skills | A per-skill report of strict-YAML, portability and fallback problems, with the exact fixes; non-zero exit for CI |

## Install

```
npx skills add proskillpacks/skills
```

Or copy the folders you want into `.agents/skills/` (one project) or `~/.agents/skills/` (all projects). Claude Code also reads `~/.claude/skills/`, and Gemini CLI reads `~/.gemini/skills/`. For other tools see https://agentskills.io/clients.

**No skills support?** Paste the `prompt.md` from a skill folder into a new chat and add your own text where it says to. The prompt versions have no scripts or web access, so they ask you to paste in the page text an installed skill would fetch itself.

## How we test

Each skill is run on real public data, such as public websites, stores, reviews, policy pages and commits. We read the output ourselves and fix what is wrong before release. Nothing here posts or changes anything for you. You review the output and apply it yourself.

## More

Pro Skill Packs also sells paid skills and packs for marketing, sales, development, data, careers, e-commerce and short-term rental hosting. These free skills are separate from them. The full catalogue is at https://proskillpacks.github.io and the shop is at https://proskillpacks.gumroad.com. The data behind the quick check is in our [100-store study](https://proskillpacks.github.io/study/).

Found a wrong output? Open an issue with the input you used and what went wrong. Updates: [@KaiVenturaBuild](https://x.com/KaiVenturaBuild).

Not affiliated with or endorsed by Shopify Inc. Shopify is a trademark of Shopify Inc.

## Licence

MIT
