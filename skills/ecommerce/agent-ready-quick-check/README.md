# agent-ready-quick-check

A free Agent Skill that checks, in about 30 seconds, how well AI shopping agents (ChatGPT, Perplexity, Gemini and Google AI Mode, Copilot, Claude) can read your Shopify store, and compares your store with 99 other Shopify stores.

Give it your store URL. That's all it needs.

## What it checks
1. **Access:** are AI search and shopping agents allowed in by robots.txt, and is there an `llms.txt`?
2. **Shipping and returns in structured data:** can an agent answer "how much is shipping?" or "can I return this?" from your product data?
3. **Star rating in structured data:** can an agent read your rating, or does it load only by JavaScript?
4. **GTIN (barcode) in structured data:** can a catalogue match your product to "this exact item"?
5. **Description length:** what share of your products have 80+ words?
6. **Image alt text:** how much of it is filled in?

Each result is shown next to the share of stores in our October 2026 study that pass the same check. In that study, the median store passed 3 of 6.

It's a diagnosis: what's missing and why it matters to an agent. It doesn't give a fix plan.

## Install
<!-- install:begin SKILL {"FOLDER": "agent-ready-quick-check"} -->
Any assistant that reads the open SKILL.md format works. Copy the `agent-ready-quick-check/` folder into `.agents/skills/` (one project) or `~/.agents/skills/` (all projects).

| Tool | Skills folder |
|---|---|
| Claude Code | `~/.claude/skills/` (project: `.claude/skills/`) |
| Codex | `~/.agents/skills/` (project: `.agents/skills/`) |
| Gemini CLI | `~/.gemini/skills/` or `~/.agents/skills/` |
| claude.ai (web and desktop apps) | zip the folder, then Settings > Capabilities > Skills > Upload skill |
| Cursor, Copilot, others | see your tool's docs: https://agentskills.io/clients |

**No skills support?** Paste `prompts/agent-ready-quick-check.md` from the repo into ChatGPT or any chatbot.
<!-- install:end -->

- It needs `python3`, with no extra packages.
- In claude.ai: Code execution must be on.

Then ask: *"Is my store ready for AI shopping agents? mystore.com"*

## Example (real public store, anonymised)

An outdoor-apparel brand's store looks fine in a browser. The quick check says:

> **Your store passes 2 of 6.** The median store in the study passes 3 of 6.
> Shipping & returns in structured data: ⚠️ gap, 0 of 5 product pages (12% of study stores pass).
> Star rating: ⚠️ gap. The rating loads only via JavaScript, so agents reading the page don't see it.
> Descriptions: ⚠️ gap. 0% of 250 products reach 80 words; median 30 words (study median: 69).

## How it works
A small Python script (standard library only) reads public pages only: robots.txt, llms.txt, `/products.json` and up to 5 product pages. It obeys robots.txt, waits 1 second between requests and never touches the cart or checkout.

The benchmark (`references/study-benchmarks.json`) holds aggregate figures from our audit of 99 Shopify stores on 3 October 2026. It isn't a random sample of all Shopify stores. Passing these checks doesn't guarantee recommendations or sales.

---

Made by Pro Skill Packs. We tested this skill on real public Shopify stores before release.

The paid **Store Ops Pack** for Shopify store owners (AI-agent readiness audit for your store, product description rewriter, SEO fixer with collection pages, support macros, chargeback responses, BFCM campaign kit) is here: https://proskillpacks.gumroad.com/l/store-ops-pack

Not affiliated with or endorsed by Shopify Inc.
