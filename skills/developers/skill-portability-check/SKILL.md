---
name: skill-portability-check
description: Checks Agent Skills (SKILL.md folders) for portability and common mistakes with a standard-library Python script, then explains each finding and the fix. It catches frontmatter that strict YAML parsers reject (such as an unquoted colon in the description, which makes tools like npx skills skip the skill), keys other than name and description, bad name format, a description that does not say when to use the skill, vendor tool names and paths, missing fallbacks when a tool or the network is absent, long bodies, and broken links. Use when the user says "check my skill", "lint SKILL.md", "is this skill portable", "why is my skill not found", "validate my skills repo", or points at a skill folder or a repository of skills.
---

# Skill Portability Check

You run a checker over one or more skills and explain what to fix. The script does the finding. You do not guess about files you did not check.

## Input
- **Required:** a path to a skill folder (one with `SKILL.md`), or to a repository or folder that holds many.
- **Optional (don't ask; use defaults):** whether warnings should fail the check (default: only errors fail).

## Step 1: Run the checker
```bash
python3 <this-skill-dir>/scripts/skill_check.py <path> [<path> ...]
```
Add `--json` for machine-readable output, `--strict` to make warnings fail the run, `--quiet` for findings only. It reads files and changes nothing. A folder that contains a file named `.skill-check-ignore` is skipped (for test fixtures).
**Fallback.** If you have no shell or no Python, ask the user to paste the `SKILL.md` (the whole file, including the frontmatter), and check it by reading against the rules in Step 2. Say that you checked by reading, not with the script, and that the script may find more.

## Step 2: What the checks mean
**Errors (the script exits 1):**
- Frontmatter missing, not closed, or rejected by strict YAML. The usual cause is an unquoted `: ` or ` #` in the description. Fix: reword it, or wrap the whole value in double quotes and escape inner double quotes.
- Missing `name` or `description`; a `name` that is not lowercase letters, digits and single hyphens, is over 64 characters, or differs from the folder name; a description over 1024 characters.
- A markdown link to a file that does not exist next to `SKILL.md`.
**Warnings:**
- Frontmatter keys other than `name` and `description` (the portable core). `license`, `compatibility` and `metadata` are in the public spec and only noted; `allowed-tools` and anything else is tool-specific.
- A description that does not say when to use the skill: add "Use when the user says ...".
- Vendor tool names (the names of one product's web, shell, skill or connector tools) and vendor skill folders (a product's hidden config folder): say the action in plain words, and name `.agents/skills/` or "your tool's skills folder".
- No fallback when the text relies on the web, a shell or a script: add one sentence such as "if you have no shell, ask the user to paste it".
- Text that some tools substitute with the user's arguments (a dollar sign followed by ARGUMENTS or by a digit): write amounts as "15 USD".
- A body over 500 lines: move detail into `references/` files.
- A `scripts/` or `references/` file that the text mentions but that is not in the folder.

## Step 3: Report
1. The table the script printed (skill, errors, warnings, lines, script languages), unchanged.
2. For each error and warning, in order of severity: the finding, why it matters in one sentence, and the exact fix (the replacement line when it is a single line).
3. What it did not check: whether the instructions actually work, whether the skill triggers, and anything outside the folder.
4. If the user wants a CI check, give them the workflow in the README.

## Rules
- Never claim a skill is "portable" or "valid". Say what the checks found and what they do not cover.
- Do not edit the user's files unless asked. Propose the exact replacement text.
- Quote findings from the output. Do not invent findings the script did not print.
