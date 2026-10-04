# late-payment-chaser-uk

A free skill for UK freelancers, consultants and small suppliers. Not legal advice.

Give it one unpaid business invoice (amount, invoice date, and the due date if you agreed one). It works out what you can claim for late payment under UK law, shows the working with links to the official sources, and writes three reminder emails you can send after filling in the names.

## What it does
- **Works out the claim with a script, not by guesswork:** statutory interest at 8% over the Bank of England base rate, the fixed £40 / £70 / £100 recovery sum, the date interest starts, the total today and the amount added each day.
- **Uses the right base rate.** The law fixes the rate at the base rate in force on the previous 30 June or 31 December, not today's rate. The script carries the Bank of England's rate history (read 4 October 2026), tries the live page first with its own honest user agent, and warns you if your dates are later than the table.
- **Handles the cases that trip people up:** no agreed payment date (the 30-day rule), public-authority customers, payment terms longer than 60 days, invoices that are not late yet, consumer clients (the Act doesn't apply), and contracts with their own late-interest clause (it uses your contract rate, shows the statutory figure beside it, and leaves the question of which one applies to a solicitor).
- **Writes three staged emails:** a friendly reminder with no mention of interest, a firm reminder that states your statutory position with the figures, and a final reminder before formal action. No threats.
- **Quotes its sources:** GOV.UK, the Late Payment of Commercial Debts (Interest) Act 1998 and the 2002 rate order, word for word, in `references/sources.md`.

## Install
<!-- install:begin SKILL {"FOLDER": "late-payment-chaser-uk"} -->
Any assistant that reads the open SKILL.md format works. Copy the `late-payment-chaser-uk/` folder into `.agents/skills/` (one project) or `~/.agents/skills/` (all projects).

| Tool | Skills folder |
|---|---|
| Claude Code | `~/.claude/skills/` (project: `.claude/skills/`) |
| Codex | `~/.agents/skills/` (project: `.agents/skills/`) |
| Gemini CLI | `~/.gemini/skills/` or `~/.agents/skills/` |
| claude.ai (web and desktop apps) | zip the folder, then Settings > Capabilities > Skills > Upload skill |
| Cursor, Copilot, others | see your tool's docs: https://agentskills.io/clients |

**No skills support?** Paste the prompt version (`prompts/late-payment-chaser-uk.md` in the download) into ChatGPT or any chatbot.
<!-- install:end -->

- The helper script needs `python3`, with no extra packages.
- In claude.ai: The calculation needs code execution switched on.

Then ask: *"My client hasn't paid my £1,800 invoice from 2 June. We agreed 30 days. What can I charge and what should I send?"*

## Works with
Works with any AI assistant that reads SKILL.md (Claude, OpenAI Codex, Gemini CLI, Cursor, GitHub Copilot and others). We run our release tests on Claude Sonnet and Opus. Use your assistant's strongest model: in our tests, a small, fast model added facts that were not in the source data.

## Before / after (real case, from a published court judgment)
The facts come from a published UK judgment: a contractor was owed £3,256.58 excluding VAT, due on 28 August 2022, and the adjudicator later awarded interest from 29 August 2022 plus £70 compensation. The case was a construction payment application; the skill applies only the general late-payment rules, which give the same start date and fixed sum here.

> **Before:** "A client owes my firm £3,256.58. We sent them the payment application on 31 July 2022 and the final date for payment was 28 August 2022. Today is 30 September 2022 and they still haven't paid. What can I charge them for paying late?"
>
> **After (skill output, unedited extract):**
>
> **Position on 30 September 2022:** The last day to pay on time was 28 August 2022; interest runs from 29 August 2022 (33 days). Assumes the customer is a business.
>
> | Item | Amount | Basis |
> |---|---|---|
> | Unpaid invoice | £3,256.58 | your figure |
> | Interest to 30 Sep 2022 (33 days at 9.25%) | £27.23 | 8% + Bank Rate of 1.25% on 30 June 2022 (Rate of Interest (No. 3) Order 2002, art. 4) |
> | Fixed sum | £70.00 | Late Payment of Commercial Debts (Interest) Act 1998, s.5A |
> | **Total today** | **£3,353.81** | interest adds £0.83 a day |

The start date and the £70 match what the adjudicator awarded in the real case. The three emails follow in the same answer.

## Honest limits
- UK only, and business-to-business debts only. It does not apply statutory interest to consumer clients.
- One invoice at a time, simple interest on a 365-day year, no part payments. GOV.UK's own worked example rounds the daily figure to the penny before multiplying, so its totals can differ from the script's by a few pence.
- It works from the facts you give it. If the due date or the amount is wrong, the figures are wrong.
- It does not cover construction-contract payment rules, disputed debts, insolvent customers, court procedure or fees. It says so when it sees one of these and stops there.
- If your contract has its own late-payment clause, it uses your contract rate and shows the statutory figure beside it. A clause displaces statutory interest only if it is a "substantial remedy"; the skill flags this and does not decide it.
- With no agreed payment date, the 30 days run from when your client received the invoice. The skill assumes the invoice date unless you tell it otherwise, and says so.
- It doesn't guarantee you will be paid. You review the output before sending anything.

## Tested
3 real tests, each built on the facts of a published UK court judgment (an agreed-date invoice of about £3,000; a £23,250 invoice with no agreed terms; a £138,000 subcontract debt with its own interest clause and no stated due date). Each run was scored against a written rubric and every figure was checked by hand against the script and the judgment. Final scores: 9.5, 9 and 9.5 out of 10. After an independent review (which also checked every figure against legislation.gov.uk and GOV.UK), the no-terms case and the contract-clause case were re-run on the current version. On a second model the three cases scored 9.5, 8.5 and 8, with every figure matching the script.

---

Made by Pro Skill Packs. We tested this skill on real public data before release.

The paid **Client-Winning Pack** for UK freelancers and solo consultants is here: https://proskillpacks.github.io/
