# Agent Browse for local models (Qwen)

A variant of [Agent Browse](../agent-browse) for Qwen3.8-27B and similar local models that tend to guess selectors and URLs. It teaches an assistant to drive a real browser with the [agent-browser](https://github.com/vercel-labs/agent-browser) command line tool: clicking, filling forms, logging in, hover menus, uploads, JavaScript dialogs, paginated data.

It was trained the same way as Agent Browse: scored tasks, and only edits that measurably helped were kept. It starts from the skill trained for Claude Opus and adds what the Qwen runs showed: never invent a URL or selector you have not seen, use the CLI's own selector syntax, pass longer JavaScript on stdin, check a list against the page's own total before calling it complete, and do not close the browser early.

The test harness, every candidate version (accepted and rejected) and the run data are in the research repo: https://github.com/proskillpacks/skillopt-agent-browse (Part 2 of the write-up).

## Example result: selection split only, held-out test pending
Qwen3.8-27B, driven by the `pi` coding agent, 8 selection tasks with 6 runs each (48 rollouts per skill). The held-out test is pending: those runs were still in progress when this was written, so there is no unseen-task result yet.

| Skill | Edits | Correct | Score | Tokens per task | Turns | Decision |
|---|---|---|---|---|---|---|
| No skill (24 rollouts) | | 21/24 | 0.7887 | 68.7k | 13.9 | |
| `s1` (Opus-trained) | | 47/48 | 0.9177 | 42.3k | 9.2 | start |
| `q1` | 4 | 43/48 | 0.8367 | 42.0k | 8.3 | rejected |
| `q2` | `q1` with one edit swapped | 48/48 | **0.9454** | **36.4k** | 8.5 | **accepted** |
| `q3` | 4 more | 47/48 | 0.9215 | 39.4k | 8.1 | rejected |
| `q4` | 2 of the `q3` edits | 44/48 | 0.8542 | 47.0k | 9.1 | see note |

`q4` note: three of its four failures were 15-minute timeouts on the 50-page catalogue crawl, after the practice site began answering 403 under four concurrent crawls. That is the benchmark throttling, not the skill.

This folder holds `q2` plus the same hand-added Setup section as Agent Browse.

## Limits
- Held-out test pending. The figures above are on the selection split, which the gate used to choose the skill, so they are optimistic.
- The cross-check was not run: this skill on Opus.
- On the train split `q2` and `s1` were level (0.9436 vs 0.9484, both 39/39), so the selection gain is not confirmed there.
- One local model, one quantisation, one harness (pi). Thinking was left at pi's default.
- The selection runs were measured under four-way concurrency and site throttling.
- The Setup section at the end of `SKILL.md` was added by hand and did not go through the validation gate.

## Install
1. Install agent-browser from https://github.com/vercel-labs/agent-browser and check that `agent-browser --help` runs.
2. Copy the `agent-browse-qwen` folder into `.agents/skills/` in your project (or `~/.agents/skills/` for everywhere), or into your tool's own skills folder.
3. Ask for a browser task in plain words, for example: "Open the page, find the price table and give me the rows."

Needs a shell tool that is allowed to run `agent-browser`.
## Tested
Tested with Qwen3.8-27B on a local OpenAI-compatible server, driven by the `pi` coding agent, with the agent-browser CLI, on the task set in the research repo. Not tested with other models or assistants.

---

Made by Pro Skill Packs. Free under the MIT licence. agent-browser is the work of its authors at Vercel Labs.
