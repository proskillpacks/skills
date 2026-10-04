# Search Intent Page Brief

Give it a target keyword and the three to five pages that rank for it (URLs, or pasted headings). It records each page's structure, classifies the search intent from what ranks, builds a coverage table with counts, names the gaps as its own judgement, and drafts an outline, questions to answer and a meta description. It does not invent search volume, difficulty or rankings.

## Install
Any assistant that reads the open SKILL.md format works.
1. Copy the `search-intent-page-brief` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere). Create the folder if it is not there. Or use your tool's own skills folder (for example `.claude/skills/` for Claude Code).
2. Ask in plain words, for example: "Make a content brief for the keyword '...'. The page is for ... Top results: [URLs]"

**No install:** open `prompt.md`, copy it, paste it into ChatGPT or any chatbot, and add your material where marked. The paste-in version needs you to paste any page text, files or diffs yourself.

Needs: Reading ranking pages needs a web fetch tool, otherwise paste each page's title and headings.

## Works with
Any assistant that reads SKILL.md (Claude, Codex, Gemini CLI, Cursor, GitHub Copilot and others) and any chatbot via `prompt.md`. Tested on Claude Sonnet. Use your assistant's strongest model: weaker models are more likely to add facts that were not in your input.

## Before / after
> **Before:** A brief that says "write 2,000 words about radiators" and lists keywords with made-up volumes.
>
> **After (skill output, from a real test run):** Test run for 'how to bleed a radiator' for a small UK heating installer. Two of three pages could be fetched (one site blocked the fetch) and the run said so, then used 'both' instead of '3 or more' for table stakes. Its main gap, in its words: neither page shows how to top up boiler pressure afterwards, 'the step where homeowners get stuck'. It marked its own extra questions as 'My additions (not from the pages)' and listed volume, difficulty and rankings under Not known.

## Limits
- It cannot see live search results, so you supply the ranking URLs. It will not guess what ranks.
- Pages that block fetching are left out and flagged. Paste their headings to include them.
- Gaps are judgement, labelled as such, not data.
- It does not promise rankings, and it does not give search volume or difficulty.
- It does not guarantee results. You review the output before you use it.

## Tested
1 real-data run on three public how-to pages (Claude Sonnet). One was blocked and the run handled it honestly.

---

Made by Pro Skill Packs. MIT licensed: use it, change it, share it.

More skills: https://proskillpacks.github.io/
