# Invoice Checker

Give it an invoice, yours or one you received. A small script (Python 3 standard library, exact decimal arithmetic) recomputes every line, the subtotal, the discount, the tax and the total, and lists every difference. It lists common fields that are missing and flags date, currency and rounding problems. It gives no tax advice.

## Install
Any assistant that reads the open SKILL.md format works.
1. Copy the `invoice-checker` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere). Or run `npx skills add proskillpacks/skills`. Or use your tool's own skills folder.
2. Ask in plain words, for example: "Check this invoice before I send it: [invoice text]."

**No install:** open `prompt.md`, copy it into ChatGPT or any chatbot and paste your material where marked.

## Works with
Any assistant that reads SKILL.md (Claude, Codex, Gemini CLI, Cursor, GitHub Copilot and others) and any chatbot via `prompt.md`. Tested on Claude Sonnet.

## Before / after
> **Before:** Re-adding an invoice by eye with a calculator, and sending it with the due date before the invoice date.
>
> **After (skill output, from a real test run):** Test run on a sample invoice we wrote with planted errors. Result, unedited: "2 differences found. Line 2's total is wrong, and that error carries into every total below it." It showed 3 x 18.25 is 54.75 not 55.75, the corrected chain of subtotal, discount, VAT and total, the due date a month before the invoice date, and the missing invoice number, customer address, payment details and VAT number. It changed nothing and said which tax questions to ask an accountant.

## Limits
- No tax advice. It does not say what rate applies or what a field requires in your country.
- Without code execution it shows the sums by hand and says they need checking.
- It cannot read an image or a scanned PDF. Give it the text or type in the figures.
- It checks arithmetic and completeness, not whether the work was done or the price is fair.
- It does not guarantee results. You review the output before you use it.

## Tested
1 run on a sample invoice we wrote with planted errors (Claude Sonnet). The invoice is ours.

---

Made by Pro Skill Packs. MIT licensed: use it, change it, share it.

More skills: https://proskillpacks.github.io/ . Pairs with the paid Expense Categoriser.
