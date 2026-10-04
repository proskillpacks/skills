# shopify-policy-checker

A free Agent Skill that checks a Shopify store's refund, shipping, privacy, terms and contact policies. It compares them with your FAQ, returns page and homepage banners, then tells you:
- what's **missing**,
- what **contradicts** itself,
- what will **confuse** customers.

Each finding comes with fixed wording you can paste into **Settings > Policies**.

Give it a store URL. That's all it needs.

> Not legal advice. It flags common gaps; have a lawyer review anything high-stakes.

## What you get

- A score out of 100, split across refund, shipping, privacy, terms and contact, and consistency.
- "Fix these first": the 3–5 riskiest issues, each with the exact quote, why it matters and paste-ready replacement text.
- A contradictions table that quotes both sources (for example, "30 days" in the policy and "60 days" in the FAQ).
- Missing must-haves, checked against a 38-item checklist (`references/checklist.md`).
- Region checks, only for places you plausibly sell to: EU/UK 14-day withdrawal, the US FTC shipping rule, Australian consumer guarantees.
- Unknown facts are left as `[X] business days` blanks. It never makes up your numbers.

## Example (real test, paraphrased so the store can't be identified)

From one run on a public men's grooming store on 2026-10-03. In the real report, every finding quotes the store's own text word for word. Here they're paraphrased:

| Found | Where |
|---|---|
| Another company's name left in the class-action waiver (copied from a template) | Terms of service |
| The return window "usually" applies, and depends on the payment processor | Refund policy |
| "No questions asked" on product pages, but the policy excludes items not in original condition | Product page vs refund policy |
| Prepaid return label promised for exchanges in the policy, but for returns too in the FAQ | Refund policy vs FAQ |

**Before** (paraphrased): refunds are offered "as long as" a third party allows it, "usually" within a set number of days.

**After** (suggested, paste-ready): "You can return any order for a full refund within [N] days of the purchase date. After [N] days, we can offer store credit instead. Store credit [does / does not] expire."


## Install
<!-- install:begin SKILL {"FOLDER": "shopify-policy-checker"} -->
Any assistant that reads the open SKILL.md format works. Copy the `shopify-policy-checker/` folder into `.agents/skills/` (one project) or `~/.agents/skills/` (all projects).

| Tool | Skills folder |
|---|---|
| Claude Code | `~/.claude/skills/` (project: `.claude/skills/`) |
| Codex | `~/.agents/skills/` (project: `.agents/skills/`) |
| Gemini CLI | `~/.gemini/skills/` or `~/.agents/skills/` |
| claude.ai (web and desktop apps) | zip the folder, then Settings > Capabilities > Skills > Upload skill |
| Cursor, Copilot, others | see your tool's docs: https://agentskills.io/clients |

**No skills support?** Paste `prompts/shopify-policy-checker.md` from the repo into ChatGPT or any chatbot.
<!-- install:end -->

Then ask: *"Check the store policies on mystore.com"*

- Works best where the agent can run Python 3 (standard library only). Without a shell, it falls back to fetching each policy page.

## How it works

1. `scripts/fetch_policies.py` downloads the store's policies:
   - `/policies/*.json` for refund, shipping, privacy, terms, contact, legal notice and subscription;
   - common pages such as `/pages/faq` and `/pages/returns`;
   - the shipping and returns claims on the homepage and a product page.
2. The agent checks everything against `references/checklist.md` and writes the report.

---

Made by Pro Skill Packs. We tested this skill on real public Shopify stores before release.

The paid **Store Ops Pack** for Shopify store owners (AI-agent readiness audit for your store, product description rewriter, SEO fixer with collection pages, support macros, chargeback responses, BFCM campaign kit) is here: https://proskillpacks.gumroad.com/l/store-ops-pack

Not affiliated with or endorsed by Shopify Inc.

More skills: https://proskillpacks.github.io/
