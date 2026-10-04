# Test Gap Finder

Give it a diff and the project's tests. You get the behaviours the change adds or alters, each marked Covered, Not covered or Unknown against the tests, and proposed test cases for the gaps with inputs and expected results taken from the code. It never gives a coverage percentage and never says a test passes unless it ran.

## What it does
- Reads the diff hunk by hunk and states each behaviour in one plain sentence.
- Searches the tests for one that would fail if the behaviour were wrong.
- Marks Covered (named test), Not covered (what it searched) or Unknown.
- Ranks proposed tests by risk, with a skeleton in the project's framework for the top ones.

## Install
Any assistant that reads the open SKILL.md format works.
1. Copy the `test-gap-finder` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere). Create the folder if it is not there. Or use your tool's own skills folder (for example `.claude/skills/` for Claude Code).
2. Ask in plain words, for example: "What tests am I missing for this change? The diff is in change.diff."

**No install:** open `prompt.md`, copy it, paste it into ChatGPT or any chatbot, and add your material where marked.

Needs: nothing beyond what the skill says about git or file access. Without a shell, it asks you to paste what it needs.

## Works with
Works with any AI assistant that reads SKILL.md (Claude, OpenAI Codex, Gemini CLI, Cursor, GitHub Copilot and others). We run our release tests on Claude Sonnet and Opus. Use your assistant's strongest model: in our tests, a small, fast model added facts that were not in the source data.

## Before / after (real public data, anonymised)
A real diff in the Express repository: a freshness check extended to a new HTTP method, and a header guard in `res.send`, with the tests as they were before the change.

> **After (skill output, excerpt):**
> 1 | `req.fresh` can return true for `QUERY` (`lib/request.js:472`) | **Not covered** | `test/req.fresh.js` and `test/req.stale.js` only send GET requests.
> 4 | `res.send` skips `Content-Length` when `Transfer-Encoding` is set | **Not covered** | `res.send.js:270` and `:287` set `Transfer-Encoding`, but only with status 204 or 205.
> Whether `QUERY` freshness is intended to follow the GET semantics is not stated in the diff.

## Honest limits
- It reads tests; it does not run them. "Not covered" means it searched and found nothing, so look for tests in places it was not told about.
- Expected results come from the code. When the code does not say what should happen, it asks.
- It is not a coverage tool and gives no percentages.
- Without repo access it works from the diff and test files you paste and marks the rest Unknown.
- It does not guarantee results. You review the output before using it.

## Tested
1 real-data run on a public multi-hunk change in the Express repository (Claude Sonnet). We checked each Covered and Not covered claim by searching the tests ourselves: all matched, and the proposed test for the Transfer-Encoding case is realistic. Not yet run on other models.

---

Made by Pro Skill Packs. Free under the MIT licence.
