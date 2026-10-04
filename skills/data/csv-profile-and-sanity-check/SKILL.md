---
name: csv-profile-and-sanity-check
description: Reads a CSV or spreadsheet export without changing it and reports what is in it, including row and column counts, each column's type, blanks, distinct values, numeric ranges, duplicates, mixed formats, odd outliers and case or spacing variants, then lists what to ask the data's owner before anyone uses it. Use when someone has a CSV or exported sheet and says "what is in this file", "is this data OK", "sanity check this export", "profile this CSV", or before cleaning, joining or analysing a file.
---

# CSV profile and sanity check

You describe a data file honestly before anyone builds on it. You never edit the file.

## What you need
1. The **file**: a CSV (or a sheet exported to CSV). If you can read files from the user's folder, use the path. Otherwise ask the user to paste the header and a sample of rows, and say how many rows there are in total.
2. Optional: what the file is meant to contain, and what it will be used for.

## Method
1. **If you can run Python 3**, run `scripts/profile_csv.py <file>` (standard library only; it only reads). Use its output as the facts. It reports encoding, delimiter, row and column counts, ragged rows, exact duplicate rows, and for each column its type, blanks, distinct count, numeric range, common values, and flags such as mixed types, dates in more than one format, values with stray spaces, case variants, constant columns, outliers (3 x IQR) and leading zeros.
2. **If you cannot run code**, say so. Work from what the user pasted: the header and a sample. State that the profile is from a sample of N rows and may miss problems elsewhere. Check the same things by eye and do not give counts for the whole file. Never estimate totals you cannot see.
3. **Read the output as an analyst.** For each flag, say what it could mean. For example: dates in two formats may be day and month swapped; a numeric column with a far outlier may be a typo or a unit mix; an ID column with duplicates may be a join problem; leading zeros mean the column should be read as text.
4. **Compare with the purpose**, if the user gave one: which columns matter for it, and which problems would hurt it.

## Output
**Snapshot:** rows, columns, encoding, delimiter, duplicates, ragged rows (or "from a sample of N rows" if you could not run the script).

**Column table:** column | type | blank % | distinct | range or common values | note.

**Flags, most serious first:** what you saw, why it matters, how to check it (a filter, a count, a question), never a fix applied.

**Questions for the data's owner:** five to eight, specific to this file.

**Not checked:** what a profile cannot tell you (whether values are true, whether rows are missing, where the data came from).

## Rules
- Read only. Do not write, sort, rename or "clean" the file. Suggest steps; do not perform them.
- Do not bring in outside facts about what the data describes. If something looks incomplete (for example, a total that seems low), ask the owner.
- Do not guess the meaning of a column. If a name is unclear, list it under questions.
- Report numbers from the script or from rows you can see. Do not invent counts.
- Plain, short sentences. No em dashes.
