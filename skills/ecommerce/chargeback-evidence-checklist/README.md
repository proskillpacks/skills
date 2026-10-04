# Chargeback Evidence Checklist (free)

Got a chargeback on Shopify Payments? Before you write anything, find out what to collect. Tell this skill the dispute reason and what happened, in your own words. It gives you:

- **Five first checks:** chargeback or inquiry, due date, already refunded, Shopify Protect, and whether the customer is right.
- **The evidence for your dispute reason**, in the order Shopify recommends (direct proof, customer acknowledgment, policy, supporting context). Each item is marked **Have**, **Get**, **Check** or **Not available** from what you told it.
- **Where to find each piece:** the place in your Shopify admin, or outside it (your inbox, the carrier's site, your saved listing).
- **What Shopify already adds automatically**, so you don't upload it twice.
- **What to leave out**, because evidence for the wrong question weakens a case.
- **The file rules:** PDF, JPEG or PNG, 2 MB per file, 4 MB in total, one file per evidence type.
- **When accepting is cheaper**, with the money in one line. No win-rate guesses.

It's built not to invent evidence: if you say "she told me it was an accident" without saying how, it lists her statement as something to **get** in writing, not as something you have. If you don't know the dispute reason yet, it tells you where to find it and says which reason your facts point to.

Covers Fraudulent, Unrecognized, Product not received, Product unacceptable, Credit not processed, Subscription canceled, Duplicate and General. Built from Shopify Help Center pages on chargebacks (read October 2026). If your dispute page says something different, follow your dispute page.

## Example (real case, from test 02)

A UK merchant posted this on the Shopify Community forum (details removed): a £284 order couldn't be delivered on the date the customer asked for, so the merchant started a refund and emailed her about it. A few days later a chargeback arrived with a £10 fee, and Shopify then said the refund couldn't be processed.

**Before:** "What evidence do I need to send?"

**After** (from the release-version test run of this case):

> I've used **Credit not processed** because you started a refund and told her it was on its way.
>
> | Already refunded? | The order's **timeline** | Check: whether the refund was completed or only started. Shopify's "cannot be processed" message suggests it never completed. Shopify can't refund once a chargeback is open, so don't try again. |
>
> If the timeline shows no completed refund, your facts match "a refund is owed and wasn't paid", and the reference says to accept. If the timeline shows the refund went through before 2 August, you can fight it as credit already processed.

Then the checklist: your email about the refund is **Have** (you emailed it), the refund record is **Check** on the order timeline, with "upload your own screenshot too if you're not sure it's there", and return tracking is ruled out because nothing was delivered.

## Install
**No install? Paste it.** `prompts/chargeback-evidence-checklist.md` in the download (also as a PDF) is a paste-in version for ChatGPT, Claude, Gemini or any other chatbot: copy it into a new chat and add your dispute underneath. It carries the key rules; the installed skill has the longer reference notes. The paste-in version was tested in Claude.

**Install it as a skill:**


Works with any AI assistant that reads SKILL.md (Claude, OpenAI Codex, Gemini CLI, Cursor, GitHub Copilot and others). We tested this skill on Claude Sonnet and Opus. Use your assistant's strongest model: in our tests of other skills, small, fast models added facts that were not in the source data.

<!-- install:begin SKILL {"FOLDER": "chargeback-evidence-checklist"} -->
Any assistant that reads the open SKILL.md format works. Copy the `chargeback-evidence-checklist/` folder into `.agents/skills/` (one project) or `~/.agents/skills/` (all projects).

| Tool | Skills folder |
|---|---|
| Claude Code | `~/.claude/skills/` (project: `.claude/skills/`) |
| Codex | `~/.agents/skills/` (project: `.agents/skills/`) |
| Gemini CLI | `~/.gemini/skills/` or `~/.agents/skills/` |
| claude.ai (web and desktop apps) | zip the folder, then Settings > Capabilities > Skills > Upload skill |
| Cursor, Copilot, others | see your tool's docs: https://agentskills.io/clients |

**No skills support?** Paste the prompt version (`prompts/chargeback-evidence-checklist.md` in the download) into ChatGPT or any chatbot.
<!-- install:end -->

Then describe the dispute in plain words, for example: "I got a chargeback for item not received, what do I need?"

No scripts, no app in your store, no Shopify login. Nothing is submitted anywhere: you upload the files yourself.

## Want the response written too?

This skill stops at the checklist. The **Chargeback Response Writer** ($5) drafts the response from the evidence you mark Have, matched to the dispute reason, and leaves gaps as gaps: https://proskillpacks.gumroad.com/l/chargeback-response-writer

Not legal advice. Not affiliated with or endorsed by Shopify Inc.

Made by Pro Skill Packs.
