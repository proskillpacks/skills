# Angry Customer Reply Check

Give it the customer's message, your draft reply and your policy. It lists what the customer raised and whether the draft answers it, tests every promise against your policy, checks the facts, flags blame, defensive phrases and empty apologies with your exact words, checks there is a next step, and returns a repaired draft. Open decisions are marked [DECIDE]. It never adds a refund or timeline you did not give it.

## Install
Any assistant that reads the open SKILL.md format works.
1. Copy the `angry-customer-reply-check` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere). Or run `npx skills add proskillpacks/skills`. Or use your tool's own skills folder.
2. Ask in plain words, for example: "Check my draft reply to this customer complaint. My policy is below."

**No install:** open `prompt.md`, copy it into ChatGPT or any chatbot and paste your material where marked.

## Works with
Any assistant that reads SKILL.md (Claude, Codex, Gemini CLI, Cursor, GitHub Copilot and others) and any chatbot via `prompt.md`. Tested on Claude Sonnet.

## Before / after
> **Before:** Draft: "Unfortunately we regret any inconvenience. As per our policy, delivery times are estimates and not guaranteed, so you should have allowed more time. We will send you a full refund and a free replacement kettle within 24 hours."
>
> **After (skill output, from a real test run):** Test run on a complaint and a draft we wrote, with a short policy. Verdict, unedited: "Hold and decide first. The draft promises a full refund and a free replacement, and the policy lets a support agent offer neither." It found the one thing the policy did allow, the 7.99 express refund, which the draft left out, quoted the blame phrases, and wrote a repaired reply with [DECIDE] markers for the refund timing and the team lead's approval.

## Limits
- It checks the draft against the policy you give it. With no policy it marks promises "not checked".
- It does not decide refunds or know your approvals.
- It does not give legal advice. If a customer mentions harm, legal action or a regulator, get advice.
- It repairs wording. It will not make a bad outcome a good one.
- It does not guarantee results. You review the output before you use it.

## Tested
1 run on a complaint, draft and policy we wrote (Claude Sonnet). All three inputs are ours.

---

Made by Pro Skill Packs. MIT licensed: use it, change it, share it.

More skills: https://proskillpacks.github.io/ . Pairs with the paid Support Macro and Escalation Writer.

Wording you can copy without the skill: [replies and emails for store owners](https://proskillpacks.github.io/stores/)
