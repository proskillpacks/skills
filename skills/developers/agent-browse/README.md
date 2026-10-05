# Agent Browse

A skill that teaches an AI assistant to drive a real browser with the [agent-browser](https://github.com/vercel-labs/agent-browser) command line tool in as few tool calls as possible. It covers clicking, filling forms, logging in, hover menus, uploads, drag and drop, JavaScript dialogs, iframes, infinite scroll and pulling data out of rendered or paginated pages.

We did not write it by hand. It was trained against a set of scored tasks, and only the edits that measurably helped were kept. The method is a scaled-down version of Microsoft's SkillOpt paper ([arXiv 2605.23904](https://arxiv.org/abs/2605.23904)). The test harness, every candidate version and all scores are in the research repo: https://github.com/proskillpacks/skillopt-agent-browse

## Measured result
On 11 unseen tasks the trained skill was about 14% cheaper per task than no skill (29.4k versus 34.2k weighted tokens), with no change in accuracy: 22 of 22 correct in every condition. Two of the three edit sets we tried made things worse and were rejected by the validation gate.

## Limits
- One student model (Claude Opus 5.5). We did not test other models.
- A small task set: 32 tasks, mostly public practice sites plus three local pages. No logins to real services and no bot detection.
- The student already solved every task without a skill, so the gain is cost, not accuracy.
- The Setup section at the end of `SKILL.md` was added by hand from problems in our test harness. It did not go through the validation gate.
- With two runs per task, the test figure is indicative, not precise.

## Install
1. Install agent-browser from https://github.com/vercel-labs/agent-browser and check that `agent-browser --help` runs.
2. Copy the `agent-browse` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere), or into your tool's own skills folder (for example `~/.claude/skills/` for Claude Code).
3. Ask for a browser task in plain words, for example: "Open the page, find the price table and give me the rows."

Needs a shell tool that is allowed to run `agent-browser`.

## Tested
Tested with Claude Opus 5.5 through the `claude` command line tool, with the agent-browser CLI, on the task set in the research repo. Not tested with other assistants.

---

Made by Pro Skill Packs. Free under the MIT licence. agent-browser is the work of its authors at Vercel Labs.
