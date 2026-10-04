# README First-Run Check: prompt and template

Use this in any chatbot (ChatGPT, Claude, Gemini and others). Nothing to install.

**How to use it**
1. Gather: the README text, a file listing (`git ls-files | head -200`), and the contents of `package.json` (or `pyproject.toml`, `requirements.txt`, `Makefile`, `Dockerfile`) and `.env.example` if they exist.
2. Copy everything from "COPY FROM HERE" to the end of this file and paste it into a new chat.
3. Under it, paste each item with a heading saying which file it is.

You get every setup step marked OK, BROKEN, MISSING or UNVERIFIED, with evidence from what you pasted, plus the README edits that fix it. The chatbot cannot see the rest of your code, so it cannot find environment variables the code reads: search the code for them yourself (for example `grep -rn "process.env\|os.environ"`).

**Prefer to do it by hand?** Follow the README in a fresh clone on a clean machine and write down every point where you had to guess.

---

COPY FROM HERE

You act as a new user following a project's README. Work only from the files I paste below. Never guess a version, command or file. Mark anything you cannot verify as UNVERIFIED and say which file you would need.

1. List every step a newcomer must follow as a numbered list: prerequisites and versions, clone and install, configuration and environment variables, services, run, test, URLs and ports. Quote the README briefly.
2. For each step say OK (evidence matches: cite the file and the line or key), BROKEN (evidence contradicts it), MISSING (a newcomer needs something the README does not say) or UNVERIFIED. Check that scripts named in the README exist in the manifest, that referenced files and links are in the file listing, that versions agree across files, and that the commands are in a workable order.
3. Describe the real first run: what a newcomer who follows the README exactly would hit first, second and so on, and where they would stop.
4. Give the README edits that fix each problem, as concrete replacement lines, ordered by how soon a newcomer meets them.
Do not run anything and do not edit anything.

Here are my files:
