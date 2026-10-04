---
name: changelog-from-commits
description: Turns a range of git commits into a user-facing changelog in Keep a Changelog style (Added, Changed, Fixed, Removed, Security), grouped and reworded for readers, with the short hash of every commit behind each entry. It skips noise (formatting, CI, internal refactors), flags commits whose message does not say what changed, and never invents a version number, a date or a breaking change. Works with git access or with pasted log output. Use when the user says "write a changelog", "release notes from commits", "what changed since v1.2", "summarise commits for a release", or gives a commit range, tag or pasted git log.
---

# Changelog from Commits

You write the changelog section for one release from the commits in it. Readers want to know what changed for them. Every entry traces to a commit.

## Input
- **Required:** a range (for example `v1.2.0..HEAD`, `main..feature`, or "since the last tag") in a repo you can read, **or** pasted `git log` output.
- **Optional (don't ask; use defaults):** the project's audience (default: people who use the project, not its maintainers), an existing CHANGELOG to match in style (default: Keep a Changelog), the version and date (default: placeholders).

## Step 1: Get the commits
If you have a shell and the repo, run read-only git commands:
```bash
git log --no-merges --format='%h %s%n%b---' <range>
```
For the last tag, `git describe --tags --abbrev=0` gives it. If a commit message is vague, look at its change with `git show --stat <hash>`.
**Fallback.** If you have no shell, no git, or the repo is not available, ask the user to paste the output of the command above (or a GitHub compare view), and work from that. Say in one line which source you used.

**Stop condition.** If the pasted output has no commit lines, say so and stop. Do not write a changelog from the repo name or from memory.

## Step 2: Sort
For each commit decide: user-facing change or not. Keep: new features, behaviour changes, bug fixes users could notice, removals and deprecations, security fixes, performance changes with a visible effect. Skip: formatting, typos in comments, CI, tests only, dependency bumps with no visible effect (list those in one line at the end if any), internal refactors. Merge commits that belong together into one entry, citing all their hashes.

## Step 3: Write
Use these headings only where there is something to say: **Added**, **Changed**, **Fixed**, **Deprecated**, **Removed**, **Security**. One line per entry, in the reader's terms ("Fixed a crash when the config file is empty"), not the commit's ("fix npe in loader"). End each with the short hash(es) in parentheses. Start with `## [VERSION] - DATE`, both as placeholders unless the user gave them.

## Step 4: Flags
After the changelog, list:
- **Vague commits** (message does not say what changed, such as "fix", "update", "wip"): `[CHECK: <hash> "<message>"]` with what the diff shows if you read it, or what to look at.
- **Possible breaking changes:** only from evidence: the message says BREAKING or has `!`, or the diff you read removes or renames something public. Otherwise say none were evident and that you did not read every diff.
- **Skipped commits:** list each hash once, then state the count by counting the listed hashes (with your tools, `wc -l` on the list; never from memory). Skipped plus included must equal the commits in the range. A commit in a note (for example "also touched X") is not listed twice.

## Rules
- No invented version, date, release name or contributor list.
- No entry without a commit behind it. No marketing language.
- If you did not read a diff, do not describe behaviour beyond what the message says.
- Do not rewrite history, create tags or commit anything. Read only.
- **Unsure stays unsure.** Anything the input marks as unsure, unconfirmed or missing stays marked (for example `[CONFIRM: ...]`) in every output, including the final text meant for someone else to read, and is never restated as fact.
