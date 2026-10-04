---
name: pr-description-and-review-prep
description: Turns a git diff or branch into a ready-to-paste pull request description (title, summary, changes, risk notes, test plan) plus questions a reviewer is likely to ask, using only what the diff shows. Use when someone is about to open a pull request or asks for a PR description or a self-review.
---

# PR description and review prep

You write the pull request text a reviewer wishes they got, from the diff, and you say what the diff does not tell you.

## What you need
- A diff. If you are inside a git repository, get it yourself: find the base branch (main or master, or ask), then read `git log --oneline <base>..HEAD` and `git diff <base>...HEAD`. If the diff is huge (over about 1500 lines), read `git diff --stat` first and then the files that matter most. If you are not in a repository, ask the user to paste the diff.
- Optional: the issue or ticket text, and why the change is being made. Do not guess the reason: take it from commit messages, the ticket, or the user; if none, write "Why: not stated in the diff" and ask one question at the end.
- Optional: the team's PR template. If one exists in the repo (`.github/pull_request_template.md`), use its headings.

## Method
1. Read the commit messages and the diff. Group changes by purpose, not by file order.
2. Separate **behaviour changes** from refactors, renames, formatting and generated files. Say when a file is generated or a lockfile.
3. Look for what a reviewer would care about: public API or schema changes, config or env var changes, migrations, dependency adds or bumps, auth or permission code touched, deleted code, new error paths, performance-sensitive loops or queries, tests added or removed.
4. Check whether tests changed with the code. If the diff touches logic but no tests, say so.

## Output (ready to paste)
**Title:** under 70 characters, imperative, says what changed.

**Summary:** 2 to 4 sentences. What and why.

**Changes:** bullets grouped by purpose, each naming the files.

**Risk and review focus:** where to look hard and why, one line each. Mark breaking changes, migrations, new env vars and dependency changes explicitly. If none, write "No breaking changes seen in the diff".

**How it was tested:** only what the user told you or what you can see (test files in the diff, commands in commit messages). Do not claim tests passed. If unknown, write "Not stated" and add a **Suggested test plan** of concrete steps based on the changes.

**Rollout and rollback:** only if the diff involves a migration, flag, config or deploy step. Otherwise leave out.

**Questions a reviewer is likely to ask:** up to 5, each tied to a specific hunk, with your best answer from the diff or "Needs author input".

**Needs your input:** the facts you could not get from the diff (reason for the change, test results, linked issue).

## Rules
- Do not invent a motivation, ticket number, benchmark or test result.
- Do not describe changes you did not see. If you skipped files, say which.
- Plain words, short sentences, no hype ("robust", "seamless"), no emojis, no em dashes.
- Do not run the code, push, or open the PR. Output text only.
