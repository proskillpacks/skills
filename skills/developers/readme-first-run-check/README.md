# README First-Run Check

Point it at a repository. It follows the README like a new user would and checks every step against the repo: versions, scripts, files, environment variables, ports and links. You get each step marked OK, BROKEN, MISSING or UNVERIFIED with evidence, the first-run path a newcomer would actually take, and the README edits that fix it.

## What it does
- Lists every instruction in the README in order.
- Checks each one against the manifests, the lockfile, config files and the code.
- Reports where a newcomer would get stuck, with file and line.
- Gives replacement lines for the README, ordered by how soon a newcomer meets the problem.

## Install
Any assistant that reads the open SKILL.md format works.
1. Copy the `readme-first-run-check` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere). Create the folder if it is not there. Or use your tool's own skills folder (for example `.claude/skills/` for Claude Code).
2. Ask in plain words, for example: "Check the getting started steps in the README. Don't install anything."

**No install:** open `prompt.md`, copy it, paste it into ChatGPT or any chatbot, and add your material where marked.

Needs: nothing beyond what the skill says about git or file access. Without a shell, it asks you to paste what it needs.

## Works with
Works with any AI assistant that reads SKILL.md (Claude, OpenAI Codex, Gemini CLI, Cursor, GitHub Copilot and others). We run our release tests on Claude Sonnet and Opus. Use your assistant's strongest model: in our tests, a small, fast model added facts that were not in the source data.

## Before / after (real public data, anonymised)
The README of a small public React tutorial app says to run `yarn && yarn start`.

> **After (skill output, excerpt):**
> **Short answer: no.** The one command the README gives, `yarn && yarn start`, stops at the second half, because the project has no `start` script.
> 4 | `yarn start` | **BROKEN** | `package.json` scripts are only `dev`, `build`, `lint` and `preview`. There is no `start`.
> 1 | Install Node.js | **MISSING** version | `.nvmrc` says `v24`. The README gives no version.
> Run command: yarn / yarn dev

## Honest limits
- By default it only reads. It does not install, build or start anything unless you say so, so some steps stay UNVERIFIED.
- It cannot see what is not in the repo (a service you run elsewhere, a secret you were told by email).
- It proposes README edits. It does not make them.
- Without repo access it works from the files you paste and marks the rest UNVERIFIED.
- It does not guarantee results. You review the output before using it.

## Tested
1 real-data run on a public MDN tutorial repository (Claude Sonnet). We checked each finding against the repo: the missing `start` script, the `.nvmrc` version and the stale Create React App text are all real. Not yet run on other models.

---

Made by Pro Skill Packs. Free under the MIT licence.
