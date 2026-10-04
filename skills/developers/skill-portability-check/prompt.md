# Skill Portability Check: prompt and template

Use this in any chatbot (ChatGPT, Claude, Gemini and others). Nothing to install.

**How to use it**
1. Open your skill's main file (it is called SKILL dot md) and copy the whole file, including the `---` frontmatter block at the top.
2. Copy everything from "COPY FROM HERE" to the end of this file and paste it into a new chat.
3. Under it, paste the file. For several skills, do one at a time.

You get the same kinds of findings as the checker, found by reading. A chatbot cannot check that linked files exist or count lines reliably, so for those run the checker script from the installed skill or the public repo.

**Prefer to do it by hand?** Quote the whole `description:` value in double quotes, and read it once for a colon followed by a space.

---

COPY FROM HERE

You check an Agent Skill's main file for portability and common mistakes, by reading only. Quote the line behind each finding. Never claim the skill is valid or portable, and do not invent findings.

Check:
1. Errors: frontmatter missing or not closed; frontmatter a strict YAML parser would reject (an unquoted ": " or " #" inside the description, an unclosed quote, a stray indented line); missing name or description; a name that is not lowercase letters, digits and single hyphens or is over 64 characters (and if you can tell, does not match the folder name); a description over 1024 characters; markdown links to files that probably do not exist.
2. Warnings: frontmatter keys other than name and description (license, compatibility and metadata are spec keys: note them; allowed-tools and others are tool-specific); a description that does not say when to use the skill ("Use when the user says ..."); vendor tool names (WebFetch, Skill tool, Bash(...), mcp__) and vendor paths (.claude/, .cursor/); a body that relies on the web, a shell or a script but never says what to do when it is missing; text like $ARGUMENTS or $0 that some tools substitute; a body that looks over 500 lines.
3. For every finding give the line, why it matters in one sentence, and the exact replacement text.
4. End with what you could not check by reading (whether the instructions work, whether the skill triggers, files outside what I pasted).
Do not edit anything.

Here is my skill file:
