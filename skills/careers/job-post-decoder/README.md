# Job Post Decoder

Paste a job post. It says in plain words what the job is, sorts the requirements into firm, wish and unclear with quotes, lists what the post leaves out (pay, location, hours, team), points out phrases worth a question, and gives you six to eight questions for the recruiter. If you add your background, it says where the fit is strong or weak and what to lead with. It never says anything about the employer beyond the post.

## Install
Any assistant that reads the open SKILL.md format works.
1. Copy the `job-post-decoder` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere). Or run `npx skills add proskillpacks/skills`. Or use your tool's own skills folder.
2. Ask in plain words, for example: "Decode this job post for me. I'm a ... who wants to move into ..."

**No install:** open `prompt.md`, copy it into ChatGPT or any chatbot and paste your material where marked.

## Works with
Any assistant that reads SKILL.md (Claude, Codex, Gemini CLI, Cursor, GitHub Copilot and others) and any chatbot via `prompt.md`. Tested on Claude Sonnet.

## Before / after
> **Before:** Reading a long ad twice and still not knowing what the role is or whether to apply.
>
> **After (skill output, from a real test run):** Test run on a real public job post for a senior product marketing role. It noticed the post was cut off mid-sentence, said the post gave no firm requirements list, listed pay, location, hours and how to apply as missing, quoted five phrases with a question for each (for example "high-performance culture"), and told a marketing coordinator that this looked like a hard first step and an associate-level role might be a better one. It invented no experience.

## Limits
- It works only from the post. It cannot tell you what the company is like.
- Phrases it flags are prompts for questions, not proof of anything.
- If the post is cut off, it says so and works with what is there.
- It does not call a post a scam.
- It does not guarantee results. You review the output before you use it.

## Tested
1 run on a real public job post (Claude Sonnet).

---

Made by Pro Skill Packs. MIT licensed: use it, change it, share it.

More skills: https://proskillpacks.github.io/ . Pairs with the paid Resume Bullet Rewriter and Interview Scorecard Builder.
