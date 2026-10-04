#!/usr/bin/env python3
"""Runs skill_check.py over the fixtures in ../examples and checks the results. python3 test_skill_check.py"""
import json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
CHECK, EX = os.path.join(H, "skill_check.py"), os.path.join(H, "..", "examples")
EXPECT = {  # folder: (errors, minimum warnings, text that must appear in the findings)
    "good-skill": (0, 0, None),
    "bad-yaml-colon": (1, 0, "unquoted ': '"),
    "coupled-skill": (0, 6, "WebFetch"),
    "broken-links": (2, 1, "broken link"),
}
bad = 0
for name, (errs, warns, text) in EXPECT.items():
    r = subprocess.run([sys.executable, CHECK, os.path.join(EX, name, "SKILL.md"), "--json"], capture_output=True, text=True)
    d = json.loads(r.stdout)
    s = d["skills"][0]
    blob = json.dumps(s)
    ok = len(s["errors"]) == errs and len(s["warnings"]) >= warns and (text is None or text in blob) and (r.returncode == (1 if errs else 0))
    print(("PASS " if ok else "FAIL ") + f"{name}: {len(s['errors'])} error(s), {len(s['warnings'])} warning(s), exit {r.returncode}")
    bad += not ok
r = subprocess.run([sys.executable, CHECK, os.path.join(EX, "coupled-skill", "SKILL.md"), "--strict"], capture_output=True, text=True)
print(("PASS " if r.returncode == 1 else "FAIL ") + "--strict makes warnings fail the run")
bad += r.returncode != 1
sys.exit(1 if bad else 0)
