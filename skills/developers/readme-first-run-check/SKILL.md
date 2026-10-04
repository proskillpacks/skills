---
name: readme-first-run-check
description: Reads a project's README the way a new user would and checks, against the repository itself, every step they are told to take - the prerequisites and versions, the install and setup commands, the files, scripts, environment variables and ports the README mentions, and the run and test commands. It reports each step as OK, BROKEN, MISSING or UNVERIFIED with file evidence, then gives the first-run path a newcomer would actually experience and the README edits that fix it. It does not run installs or touch the network unless the user says so. Use when the user says "does my README work", "check the getting started steps", "first run check", "onboarding docs are out of date", or points at a repo or pastes a README.
---

# README First-Run Check

You are the new user. You follow the README line by line, but you check each claim against the repo instead of guessing. The output is a list of the places a newcomer would get stuck, with evidence.

## Input
- **Required:** a repository you can read (a path), or pasted material: the README, a file listing, and the manifests (`package.json`, `pyproject.toml`, `requirements.txt`, `Makefile`, `Dockerfile`, `.env.example`, whichever exist).
- **Optional (don't ask; use defaults):** the platform the newcomer uses (default: macOS or Linux with a recent standard toolchain), whether you may run commands (default: read-only commands only; do not install, build, start servers or use the network unless the user says so).

## Step 1: List the steps
Read the README top to bottom and write every instruction a newcomer must follow as a numbered list: prerequisites and versions, clone and install, configuration and environment variables, database or service setup, run, test, and any URL or port to open. Keep the README's own words short in quotes.

## Step 2: Check each step against the repo
Use read-only commands (list files, read files, search the code). For every step decide:
- **OK:** the evidence matches. Cite the file and line.
- **BROKEN:** the evidence contradicts the step (a script the README names is not in `package.json`, a file is missing, a version constraint conflicts with `.nvmrc` or `engines`, a command's flag is not defined, a port differs from the code's).
- **MISSING:** something a newcomer needs is not in the README (an environment variable the code reads and `.env.example` or the README never mentions, a required service, a setup step the CI runs but the README does not).
- **UNVERIFIED:** it cannot be checked without running it or without network access. Say what would verify it.
Also check relative links and referenced files exist, and that the commands appear in the order they must run.

## Step 3: Describe the real first run
In a short numbered path, what a newcomer who follows the README exactly would hit first, second, and so on, and where they would stop. Then list the README changes that fix each problem, as concrete replacement lines, in order of how soon a newcomer meets them.

## Step 4: If the user allows running
Only when asked: run the safest steps first (version checks), then install, then test or run, stopping at the first failure and quoting the real error. Never run anything that deletes, publishes, deploys or needs secrets.

## Fallback when a tool is missing
- **No shell or repo access:** work from what the user pastes. List which files you needed and did not get, and mark every step that depends on them UNVERIFIED.
- **Network blocked:** mark install and download steps UNVERIFIED and check only what is in the repo.

## Rules
- Every OK, BROKEN or MISSING carries evidence (file and line, or the README line). No evidence means UNVERIFIED.
- Do not guess versions or commands. Do not edit files; propose edits.
- Do not run commands that change the user's machine without being asked.
