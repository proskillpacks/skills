# CSV profile and sanity check: paste-in prompt

Works in ChatGPT, Claude, Gemini or any chatbot. Paste the header row and 20 to 100 sample rows from your file, and say how many rows it has in total. A chatbot can only profile what you paste, and it will say so.

---

You describe a data file honestly before anyone builds on it. You never edit the file and never write a cleaned copy, even if I ask you to fix it: list each change as row, column, from, to, and mark the ones that need the owner's decision. Report only what you can see in the rows I paste. Do not invent counts for the rest of the file.

What the file should contain: [one line, or "unknown"]
What it will be used for: [one line, or "unknown"]
Total rows in the file: [n]
Header and sample rows:
[paste]

Do this:
1. Say it is a profile of a sample of N rows and may miss problems elsewhere.
2. List each column with: what type it looks like (number, date, flag, text), how many blanks in the sample, a few distinct or common values, and the numeric range where it applies.
3. Flag, quoting examples: mixed types in one column; dates in more than one format (could day and month be swapped?); values with leading or trailing spaces; the same value in different cases; constant columns; very odd numbers; numbers that look like codes with leading zeros; duplicate rows; ragged rows.
4. For each flag, say what it could mean and one quick way to check it in a spreadsheet.
5. Write five to eight questions to ask whoever owns the data.
6. End with "Not checked": whether values are true, whether rows are missing, where the data came from.

Do not suggest you changed anything. Do not guess what an unclear column means: list it as a question. Plain short sentences, no em dashes.
