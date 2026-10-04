# PR Description and Review Prep

Run it in your repository, or paste a diff. It reads the commits and the diff and gives you a ready-to-paste PR: title, summary, changes grouped by purpose, risk and review focus, how it was tested (only what is stated), up to five likely reviewer questions and a list of facts it could not get from the diff. It will not invent a reason, a ticket or a test result.

## Install
Any assistant that reads the open SKILL.md format works.
1. Copy the `pr-description-and-review-prep` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere). Create the folder if it is not there. Or use your tool's own skills folder (for example `.claude/skills/` for Claude Code).
2. Ask in plain words, for example: "I am about to open a PR from this branch into main. Write the PR description."

**No install:** open `prompt.md`, copy it, paste it into ChatGPT or any chatbot, and add your material where marked. The paste-in version needs you to paste any page text, files or diffs yourself.

Needs: Inside a git repository it runs git itself. Otherwise paste a diff.

## Works with
Any assistant that reads SKILL.md (Claude, Codex, Gemini CLI, Cursor, GitHub Copilot and others) and any chatbot via `prompt.md`. Tested on Claude Sonnet. Use your assistant's strongest model: weaker models are more likely to add facts that were not in your input.

## Before / after
> **Before:** A commit-list dump: "fix res.send / bump qs / bump proxy-addr / bump morgan"
>
> **After (skill output, from a real test run):** Test run on four real commits from a public web framework. Output, unedited: "Title: Preserve ETag with Transfer-Encoding in res.send; bump deps". It grouped the fix and the three dependency bumps separately, noted which bumps were runtime vs dev, said the diff showed no lockfile change, wrote "Why: not stated in the diff", and caught that the branch it was asked to diff against was behind another branch.

## Limits
- It only knows the diff and commit messages. The reason for the change comes from you.
- It does not run tests. "How it was tested" says Not stated unless you tell it.
- It does not open the PR. You paste the text.
- Very large diffs: it reads the stat first and then the key files, and says what it skipped.
- It does not guarantee results. You review the output before you use it.

## Tested
1 real-data run on four public commits (Claude Sonnet).

---

Made by Pro Skill Packs. MIT licensed: use it, change it, share it.

More skills: https://proskillpacks.github.io/
