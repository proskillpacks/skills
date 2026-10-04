# Accessibility Quick Audit

Give it a URL, pasted HTML or component files. It checks text alternatives, form labels, link and button names, headings and landmarks, keyboard and focus, ARIA, contrast where the colours are visible, media and zoom. You get issues ranked by impact with the WCAG criterion, the quoted code, who it affects and a fix, plus what needs a human check. It never says a page is accessible.

## Install
Any assistant that reads the open SKILL.md format works.
1. Copy the `accessibility-quick-audit` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere). Create the folder if it is not there. Or use your tool's own skills folder (for example `.claude/skills/` for Claude Code).
2. Ask in plain words, for example: "Audit this page for accessibility, WCAG 2.2 AA: [URL or pasted HTML]"

**No install:** open `prompt.md`, copy it, paste it into ChatGPT or any chatbot, and add your material where marked. The paste-in version needs you to paste any page text, files or diffs yourself.

Needs: Reading a URL needs a web fetch tool, otherwise paste the HTML.

## Works with
Any assistant that reads SKILL.md (Claude, Codex, Gemini CLI, Cursor, GitHub Copilot and others) and any chatbot via `prompt.md`. Tested on Claude Sonnet. Use your assistant's strongest model: weaker models are more likely to add facts that were not in your input.

## Before / after
> **Before:** A generic "add alt text and check contrast" checklist that does not point at your code.
>
> **After (skill output, from a real test run):** Test run on the W3C's public inaccessible demo page. Opening line, unedited: "Found 12 high-impact, 9 medium and 5 low issues in the markup I read." Issue 1: `onFocus="blur();"` on 20+ links, first at line 248, which removes keyboard focus, with the fix. It also noticed the page was the W3C demo and not a small organisation's site, said so, and audited what was there.

## Limits
- It reads markup. It does not run a browser, so content added by JavaScript and real focus order are not checked.
- It is not a legal accessibility audit or a conformance statement.
- Alt text quality, reading order and caption accuracy need a human. It lists them with a one-line test for each.
- It computes contrast only where colour values are visible in the code.
- It does not guarantee results. You review the output before you use it.

## Tested
1 real-data run on a public demo page built with known accessibility faults (Claude Sonnet). Issues traced to quoted lines.

---

Made by Pro Skill Packs. MIT licensed: use it, change it, share it.

More skills: https://proskillpacks.github.io/
