#!/usr/bin/env python3
"""skill_check.py: check Agent Skills (SKILL.md folders) for portability and common mistakes.
Python 3, standard library only. Read-only. MIT licence, Pro Skill Packs.

    python3 skill_check.py <skill-folder-or-repo> [more paths] [--json] [--strict] [--quiet]

Finds every SKILL.md under the paths and reports, per skill:
  ERRORS (exit code 1): no or unclosed frontmatter; frontmatter that strict YAML parsers reject (for example an
    unquoted ': ' or ' #' in the description); missing name or description; name not lowercase-hyphens, over 64
    characters, or different from the folder name; description over 1024 characters; broken relative markdown links.
  WARNINGS: keys other than name and description (not portable; license, compatibility and metadata are spec keys and
    only noted); allowed-tools; description that does not say when to use the skill, or is very short; vendor tool names
    (WebFetch, Skill tool, Bash(...), mcp__ ...) and vendor paths (.claude/, .cursor/ ...); no fallback when the text
    relies on the web, a shell or a script; body over 500 lines; $ARGUMENTS or $0-style text some tools substitute;
    referenced scripts/ or references/ files that do not exist.
  INFO: bundled script languages, agent product names mentioned, line counts.
A folder containing a file named .skill-check-ignore is skipped (use it for test fixtures).
--strict turns warnings into errors (for CI that should block on warnings). --json prints machine-readable output.
Patterns for vendor tools, products, paths and fallback phrases are the ones used in our portability study.
"""
import json
import os
import re
import sys

VENDOR_TOOLS = {
    "WebFetch": r"\bWebFetch\b", "WebSearch": r"\bWebSearch\b", "TodoWrite": r"\bTodoWrite\b", "AskUserQuestion": r"\bAskUserQuestion\b",
    "NotebookEdit": r"\bNotebookEdit\b", "ExitPlanMode": r"\bExitPlanMode\b", "Bash(...)": r"\bBash\(", "Task tool": r"\bTask tool\b|\bTask\(",
    "Skill tool": r"\bSkill tool\b", "mcp__ tool": r"\bmcp__\w+", "named tool (Read/Write/Edit/Glob/Grep tool)": r"\b(?:Read|Write|Edit|Glob|Grep) tool\b",
}
PRODUCTS = {
    "Claude Code": r"\bClaude Code\b", "claude.ai": r"\bclaude\.ai\b", "Cursor": r"\bCursor\b", "Codex": r"\bCodex\b",
    "Gemini CLI": r"\bGemini CLI\b", "Copilot": r"\bCopilot\b", "CLAUDE.md/GEMINI.md": r"\b(?:CLAUDE|GEMINI)\.md\b",
}
PATHS = {
    "~/.claude or .claude/": r"(?:~/|\./|\b)\.claude/", "~/.cursor or .cursor/": r"\.cursor/", "~/.codex or .codex/": r"\.codex/",
    "~/.gemini or .gemini/": r"\.gemini/", "$CLAUDE_* variable": r"\$\{?CLAUDE_\w+",
}
FALLBACK = re.compile(r"(?:if|when)\s+(?:\w+\s+){0,3}?(?:can ?not|can't|cannot|don't have|do not have|have no|are unable|aren't able|unable to|is not available|isn't available|are not available|is unavailable|no access)|fall ?back|otherwise,?\s+(?:ask|use|paste)|ask the user to (?:paste|provide|supply)|if you only have\b|or (?:the user )?pastes?\b|\bpasted (?:text|html|content|the|it)\b|no (?:shell|web|network|python)|if .{0,40}(?:isn't|is not|not) installed", re.I)
NEEDS_TOOLS = re.compile(r"\b(?:curl|wget|fetch(?:es|ing)?\b|web (?:page|search|tool)|network|internet|python3?\b|bash\b|shell|run the script|git (?:log|diff|show))", re.I)
WHEN = re.compile(r"\b(?:use when|use this (?:skill )?when|when the user|when someone|when you|trigger|use for|use if|invoke when|if the user)\b", re.I)
SPEC_KEYS = {"license", "compatibility", "metadata"}
SCRIPT_EXT = {".py": "Python", ".sh": "shell", ".bash": "shell", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript", ".ts": "TypeScript", ".rb": "Ruby", ".go": "Go", ".ps1": "PowerShell"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def split_frontmatter(text):
    if not text.startswith("---"):
        return None, text, 0
    lines = text.split("\n")
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            return lines[1:i], "\n".join(lines[i + 1:]), i + 1
    return "UNCLOSED", text, 0


def strict_yaml(fm_lines):
    """Parse the small subset of YAML used in SKILL.md frontmatter the way a strict parser would.
    Returns (dict of key -> string value, list of problems)."""
    data, problems = {}, []
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if "\t" in line[: len(line) - len(line.lstrip())]:
            problems.append(f"line {i + 2}: tab used for indentation")
        if line[0] in " -":
            # continuation of the previous key, handled below; a stray indented line here is a mapping error
            problems.append(f"line {i + 2}: unexpected indentation or list item: {line.strip()[:50]!r}")
            i += 1
            continue
        m = re.match(r"^([^\s:#][^:]*?)\s*:(?:\s+(.*))?$", line)
        if not m:
            problems.append(f"line {i + 2}: not a 'key: value' line: {line[:50]!r}")
            i += 1
            continue
        key, val = m.group(1), (m.group(2) or "").rstrip()
        if key in data:
            problems.append(f"line {i + 2}: duplicate key {key!r}")
        # gather continuation lines (indented)
        cont = []
        j = i + 1
        while j < len(fm_lines) and (fm_lines[j].startswith((" ", "\t")) or not fm_lines[j].strip()):
            cont.append(fm_lines[j])
            j += 1
        if val[:1] in ("|", ">"):
            data[key] = " ".join(c.strip() for c in cont if c.strip())
        elif val[:1] in ('"', "'"):
            q = val[0]
            full = " ".join([val] + [c.strip() for c in cont if c.strip()])
            end = -1
            k = 1
            while k < len(full):
                if q == '"' and full[k] == "\\":
                    k += 2
                    continue
                if full[k] == q:
                    if q == "'" and full[k + 1:k + 2] == "'":
                        k += 2
                        continue
                    end = k
                    break
                k += 1
            if end < 0:
                problems.append(f"line {i + 2}: {key}: quoted string is never closed")
                data[key] = full[1:]
            else:
                rest = full[end + 1:].strip()
                if rest and not rest.startswith("#"):
                    problems.append(f"line {i + 2}: {key}: text after the closing quote: {rest[:40]!r}")
                data[key] = full[1:end]
        else:
            full = " ".join([val] + [c.strip() for c in cont if c.strip()]).strip()
            if val[:1] in ("[", "{"):
                data[key] = full
            else:
                if val[:1] in ("*", "&", "!", "%", "@", "`", "?") and val[:2] != "? ":
                    problems.append(f"line {i + 2}: {key}: a plain value cannot start with {val[0]!r}; quote it")
                if ": " in full or full.endswith(":"):
                    problems.append(f"line {i + 2}: {key}: unquoted ': ' inside the value (strict YAML reads it as a nested mapping). Quote the value or reword")
                if " #" in full:
                    problems.append(f"line {i + 2}: {key}: ' #' starts a comment in YAML and cuts the value short. Quote the value or reword")
                data[key] = full
        i = j
    return data, problems


def check_skill(path):
    d = os.path.dirname(path)
    folder = os.path.basename(d) or "."
    text = open(path, encoding="utf-8", errors="replace").read()
    res = {"path": path, "name": None, "errors": [], "warnings": [], "info": []}
    E, W, I = res["errors"].append, res["warnings"].append, res["info"].append
    fm, body, fm_lines = split_frontmatter(text)
    if fm is None:
        E("no frontmatter: SKILL.md must start with a --- block holding name and description")
        fm = []
    elif fm == "UNCLOSED":
        E("frontmatter is never closed (no second --- line)")
        fm = []
    data, probs = strict_yaml(fm)
    for p in probs:
        E("frontmatter: " + p)
    name, desc = data.get("name", ""), data.get("description", "")
    res["name"] = name or folder
    if not name:
        E("missing name")
    else:
        if not NAME_RE.match(name) or len(name) > 64:
            E(f"name {name!r} must be lowercase letters, digits and single hyphens, at most 64 characters")
        if name != folder and folder not in ("", "."):
            E(f"name {name!r} does not match its folder {folder!r}")
    if not desc:
        E("missing description")
    else:
        if len(desc) > 1024:
            E(f"description is {len(desc)} characters (limit 1024)")
        if len(desc) < 40:
            W(f"description is only {len(desc)} characters; say what the skill does and when to use it")
        if not WHEN.search(desc):
            W("description does not say when to use the skill (for example 'Use when the user says ...'); agents pick skills from it")
    extra = [k for k in data if k not in ("name", "description")]
    for k in extra:
        if k in SPEC_KEYS:
            I(f"frontmatter key {k!r} is in the public spec but not every tool reads it")
        elif k in ("allowed-tools", "allowed_tools", "tools"):
            W(f"frontmatter key {k!r} is tool-specific (one agent's tool names); other agents ignore it")
        else:
            W(f"frontmatter key {k!r} is not in the public spec; portable skills use only name and description")
    for label, table, tip in (("vendor tool", VENDOR_TOOLS, "say the action in plain words (for example 'fetch the page with whatever web tool you have')"),
                              ("vendor path", PATHS, "name the generic folder (.agents/skills/) or say 'your tool's skills folder'")):
        for n, rx in table.items():
            hits = len(re.findall(rx, text))
            if hits:
                W(f"{label} {n}: {hits} mention(s); {tip}")
    pr = {n: len(re.findall(rx, body)) for n, rx in PRODUCTS.items()}
    pr = {n: c for n, c in pr.items() if c}
    if pr:
        I("agent products named: " + ", ".join(f"{n} x{c}" for n, c in pr.items()) + " (fine in a list of supported tools; a problem if the skill only works in one)")
    if re.search(r"\$ARGUMENTS|\$\{?ARGUMENTS|(?<![\w$])\$[0-9](?![\w.,])", body):
        W("text like $ARGUMENTS or $0 may be replaced by some tools with the user's arguments; write amounts as '15 USD' and avoid $ before a digit")
    needs = NEEDS_TOOLS.search(body)
    if needs and not FALLBACK.search(body):
        W(f"the text relies on a tool or the network ('{needs.group(0)}') but never says what to do when it is missing (for example 'if you have no shell, ask the user to paste it')")
    lines = body.count("\n") + 1
    res["lines"] = lines + fm_lines
    if lines > 500:
        W(f"body is {lines} lines; move detail into references/ files loaded only when needed (under 500 is the usual guidance)")
    elif lines > 200:
        I(f"body is {lines} lines")
    langs = sorted({SCRIPT_EXT[os.path.splitext(f)[1].lower()] for dp, dns, fns in os.walk(d) for f in fns if os.path.splitext(f)[1].lower() in SCRIPT_EXT and not set(dp.split(os.sep)) & SKIP_DIRS})
    res["scripts"] = langs
    if langs:
        I("bundled scripts: " + ", ".join(langs))
    for m in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", body):
        t = m.group(1).split("#")[0]
        if t and not re.match(r"^[a-z][a-z0-9+.-]*:", t, re.I) and not t.startswith("/") and not os.path.exists(os.path.join(d, t)):
            E(f"broken link: {m.group(1)} (no such file next to SKILL.md)")
    for m in set(re.findall(r"`((?:\./)?(?:scripts|references|assets)/[\w./-]+)`", body)):
        if not os.path.exists(os.path.join(d, m)) and not re.search(r"[<>*{]", m):
            W(f"mentions {m} but the file is not in the skill folder")
    return res


def find_skills(paths):
    out = []
    for p in paths:
        if os.path.isfile(p) and os.path.basename(p) == "SKILL.md":
            out.append(p)
            continue
        for dp, dns, fns in os.walk(p):
            dns[:] = sorted(x for x in dns if x not in SKIP_DIRS)
            if ".skill-check-ignore" in fns:   # a folder of test fixtures: skip it and everything below it
                dns[:] = []
                continue
            if "SKILL.md" in fns:
                out.append(os.path.join(dp, "SKILL.md"))
    return out


def main():
    a = [x for x in sys.argv[1:]]
    flags = {x for x in a if x.startswith("--")}
    paths = [x for x in a if not x.startswith("--")]
    if not paths or "--help" in flags:
        print(__doc__)
        sys.exit(2)
    skills = find_skills(paths)
    if not skills:
        print("no SKILL.md found under: " + " ".join(paths))
        sys.exit(2)
    results = [check_skill(s) for s in skills]
    strict = "--strict" in flags
    n_err = sum(len(r["errors"]) + (len(r["warnings"]) if strict else 0) for r in results)
    if "--json" in flags:
        print(json.dumps({"skills": results, "errors": sum(len(r["errors"]) for r in results), "warnings": sum(len(r["warnings"]) for r in results)}, indent=2))
    else:
        w = max(len(r["name"]) for r in results)
        print(f"{'skill':<{w}}  errors  warnings  lines  scripts")
        for r in results:
            print(f"{r['name']:<{w}}  {len(r['errors']):>6}  {len(r['warnings']):>8}  {r.get('lines', 0):>5}  {','.join(r.get('scripts', [])) or '-'}")
        print()
        for r in results:
            if not (r["errors"] or r["warnings"]) and "--quiet" in flags:
                continue
            if not (r["errors"] or r["warnings"] or r["info"]):
                continue
            rp = os.path.relpath(r['path'])
            print(f"{r['name']}  ({r['path'] if rp.startswith('..') else rp})")
            for e in r["errors"]:
                print(f"  ERROR  {e}")
            for x in r["warnings"]:
                print(f"  warn   {x}")
            if "--quiet" not in flags:
                for x in r["info"]:
                    print(f"  info   {x}")
        print(f"\n{len(results)} skill(s): {sum(len(r['errors']) for r in results)} error(s), {sum(len(r['warnings']) for r in results)} warning(s)")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
