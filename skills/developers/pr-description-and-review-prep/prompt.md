# PR description and review prep: paste-in prompt

Works in ChatGPT, Claude, Gemini or any chatbot. Get your diff with `git diff main...HEAD` (use your base branch) and paste it where marked. For very large diffs, paste `git diff --stat` plus the files that matter most.

---

Write the pull request text from the diff below. Use only what the diff and my notes show.

Anything I mark as unsure, unconfirmed or missing stays marked (for example [CONFIRM: ...]) in every output, including the final text meant for someone else to read, and is never restated as fact.

Why this change (if you know): [reason, ticket link, or "not sure"]
Tests I ran (if any): [or "none yet"]
Diff: [paste here]

Output, ready to paste:
- Title: under 70 characters, imperative.
- Summary: 2 to 4 sentences, what and why. If the reason is not in my notes, write "Why: not stated" instead of guessing.
- Changes: bullets grouped by purpose, naming the files. Separate behaviour changes from refactors, renames, formatting and generated files.
- Risk and review focus: where to look hard and why. Call out breaking changes, migrations, new env vars, dependency changes, auth code touched, deleted code, and logic changed with no tests.
- How it was tested: only what I told you or what the diff shows. Never claim tests passed. If unknown, write "Not stated" and give a suggested test plan.
- Rollout and rollback: only if a migration, flag, config or deploy step is involved.
- Questions a reviewer is likely to ask: up to 5, tied to a specific hunk, with your best answer or "Needs author input".
- Needs your input: the facts you could not get from the diff.

Rules: do not invent a motivation, ticket number, benchmark or test result. Do not describe changes you did not see. Plain short sentences, no hype words, no emojis, no em dashes.
