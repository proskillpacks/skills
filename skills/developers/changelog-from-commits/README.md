# Changelog from Commits

Give it a commit range in a repo, or paste `git log` output. You get a changelog section in Keep a Changelog style, written for the people who use the project, with the commit hash behind every line. Vague commits and possible breaking changes are flagged instead of guessed.

## What it does
- Reads the log (or the pasted output) and decides which commits a user would notice.
- Groups related commits and rewrites them in the reader's terms under Added, Changed, Fixed, Removed, Security.
- Leaves the version and date as placeholders, and never invents a breaking change.
- Lists vague commits as [CHECK] and the commits it skipped, with their hashes.

## Install
Any assistant that reads the open SKILL.md format works.
1. Copy the `changelog-from-commits` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere). Create the folder if it is not there. Or use your tool's own skills folder (for example `.claude/skills/` for Claude Code).
2. Ask in plain words, for example: "Write the changelog for everything since the last tag."

**No install:** open `prompt.md`, copy it, paste it into ChatGPT or any chatbot, and add your material where marked.

Needs: nothing beyond what the skill says about git or file access. Without a shell, it asks you to paste what it needs.

## Works with
Works with any AI assistant that reads SKILL.md (Claude, OpenAI Codex, Gemini CLI, Cursor, GitHub Copilot and others). We run our release tests on Claude Sonnet and Opus. Use your assistant's strongest model: in our tests, a small, fast model added facts that were not in the source data.

## Before / after (real public data, anonymised)
The Express repository, last 15 commits: dependency bumps with CVE notes in the commit bodies, CI updates, a docs fix and one bug fix.

> **After (skill output, excerpt):**
> ### Security
> - Raised the minimum `qs` version to 6.16.0, which patches CVE-2026-82417 (GHSA-4mjr-xmp4-gh2g) and CVE-2026-82562 (GHSA-x5fp-wj9c-mxmx). (3b7e39f)
> ### Fixed
> - `res.send` now still generates an ETag when a `Transfer-Encoding` header is set. (9a34acf)
> [CHECK: 98bd4cd "deps: proxy-addr@^2.0.8 (#7474)"] The message gives no reason for the bump.
> Skipped commits: 11

## Honest limits
- It sees commit messages, and reads a diff only when it can. A vague message stays vague: it flags it.
- Breaking changes are reported only from evidence (a BREAKING note, a `!`, or a removed public name in a diff it read).
- It writes the text. It does not tag, commit or publish anything.
- If it has no git access, it asks you to paste the log and says so.
- It does not guarantee results. You review the output before using it.

## Tested
1 real-data run on the public Express repository (Claude Sonnet, 15 commits). We checked each entry against the commit bodies: the CVE ids and the body-parser behaviour change are in the messages, nothing was invented, and the one vague commit was flagged.

---

Made by Pro Skill Packs. Free under the MIT licence.
