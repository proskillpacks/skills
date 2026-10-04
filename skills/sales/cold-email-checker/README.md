# Cold Email Checker

Give it a cold email draft and the text of the prospect's page. It tests every claim about the prospect against that text, flags claims about you that need proof, checks the subject line, the single ask and the length, and lists the commercial email basics from the US FTC's CAN-SPAM guide that the draft is missing. You get a verdict, a claims table, quoted issues and a tightened version with unsupported claims removed.

## Install
Any assistant that reads the open SKILL.md format works.
1. Copy the `cold-email-checker` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere). Or run `npx skills add proskillpacks/skills`. Or use your tool's own skills folder.
2. Ask in plain words, for example: "Check my cold email draft before I send it. Here is the draft and the prospect's page text."

**No install:** open `prompt.md`, copy it into ChatGPT or any chatbot and paste your material where marked.

## Works with
Any assistant that reads SKILL.md (Claude, Codex, Gemini CLI, Cursor, GitHub Copilot and others) and any chatbot via `prompt.md`. Tested on Claude Sonnet.

## Before / after
> **Before:** Draft opening: "Subject: Re: quick question about your growth ... I saw you just launched Hemingway Editor Plus last week and it looks amazing. I've helped 40 software companies double their signups ..."
>
> **After (skill output, from a real test run):** Test run on a draft we wrote with common flaws, against text from a real public software homepage. Verdict, unedited: "Do not send. The email claims results you can't prove, says the prospect launched something last week when their page doesn't say so, and makes four asks." It marked the launch claim Unsupported, the results claim Needs proof, flagged "Re:" on a first message, listed the missing postal address, opt-out and ad disclosure, and returned a tightened version with [CONFIRM] markers.

## Limits
- It checks claims against the text you give it. Without the page text it marks them "not checked".
- The legal list comes from one US guide and is not legal advice. It does not say whether a law applies to you. Rules in other countries differ.
- It does not find addresses, check deliverability or send anything.
- It cannot know whether your proof is true. You confirm it.
- It does not guarantee results. You review the output before you use it.

## Tested
1 run on a flawed draft we wrote and text from a real public homepage (Claude Sonnet). The draft is ours, the page text is real.

---

Made by Pro Skill Packs. MIT licensed: use it, change it, share it.

More skills: https://proskillpacks.github.io/ . Pairs with the paid Cold Email from a Website and Follow-Up Ladder.
