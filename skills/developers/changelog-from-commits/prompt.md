# Changelog from Commits: prompt and template

Use this in any chatbot (ChatGPT, Claude, Gemini and others). Nothing to install.

**How to use it**
1. In your repo, run `git log --no-merges --format='%h %s%n%b---' v1.2.0..HEAD` (use your own tag or range) and copy the output.
2. Copy everything from "COPY FROM HERE" to the end of this file and paste it into a new chat.
3. Under it, paste the log.

You get a changelog section grouped under Added, Changed, Fixed and so on, with the commit hash behind each line, and a list of commits it could not understand. The chatbot sees only commit messages, not the code, so it will not know what a vague commit did: check the flagged ones.

**Prefer to do it by hand?** Walk the log once and put each user-facing commit under one heading; skip formatting, CI and refactors.

---

COPY FROM HERE

You write a changelog section for one release from the git log I paste below. Readers are people who use the project, not its maintainers. Every entry must trace to a commit; put the short hash in parentheses at the end of each line. Never invent a version number, date or breaking change. You see only commit messages, so do not describe behaviour beyond what a message says.

Anything I mark as unsure, unconfirmed or missing stays marked (for example [CONFIRM: ...]) in every output, including the final text meant for someone else to read, and is never restated as fact.

1. Decide for each commit whether it is user-facing. Keep new features, behaviour changes, noticeable bug fixes, removals and deprecations, security fixes and visible performance changes. Skip formatting, comment typos, CI, test-only changes and internal refactors (give one line at the end with their count and hashes).
2. Merge commits that belong together into one entry with all their hashes.
3. Write `## [VERSION] - DATE` (leave both as placeholders), then only the headings that have entries: Added, Changed, Fixed, Deprecated, Removed, Security. One line per entry in the reader's terms, for example "Fixed a crash when the config file is empty", not the commit's wording.
4. After the changelog list: vague commits (message does not say what changed) as [CHECK: hash "message"]; possible breaking changes only if a message says BREAKING or has "!" (otherwise say none were evident and that you saw only messages); skipped commits.
No marketing language.

Here is the git log:
