# Changelog

What changed in this repository, newest first. New skills, fixes and changes that came from feedback. Dates are UTC.

## 2026-10-04 (later)

### Changed (from our own tests)
- Skills that write text for other people to read now carry one standard rule: anything the input marks as unsure, unconfirmed or missing stays marked (for example `[CONFIRM: ...]`) in every output, including the final text, and is never restated as fact. It is in each skill's `SKILL.md` rules and in its `prompt.md`. In our second test runs, three of four defects were an unsure fact restated as fact in text meant for a customer.
- `skill-portability-check`: the checker is now v1.1.0 and adds warning SC017 for a skill that says it writes text for others but has no rule about unsure input. The same version is in https://github.com/proskillpacks/skill-check .
- `fact-claim-checker`: the summary counts must now match the claims table. `csv-profile-and-sanity-check`: it never writes a cleaned copy, even when asked, and lists each change as row, column, from, to instead.
- `changelog-from-commits`: the count of skipped commits must now be counted from the listed hashes, and skipped plus included must equal the commits in the range.
- `ai-search-readiness-check`: the helper now reports a response it cannot decode (for example Brotli) instead of reading garbage.

## 2026-10-04

### Changed (from feedback)
- Six skills now state a stop condition before their fallback: what to do when the input is missing, instead of guessing. `changelog-from-commits`, `test-gap-finder`, `skill-portability-check`, `job-post-decoder`, `csv-profile-and-sanity-check`, `cold-email-checker`. The idea came from other agents who read our fallback checklist.
- `skill-portability-check`: the checker now matches skill-check v1 (rule IDs such as SC001, and an `--ignore` option). Detection is unchanged.
- Skills that send web requests no longer use a user agent ending in `; python-urllib`. One firewall answered 406 to it.

### Added
- Demo animations from real runs, shortened, in `docs/demos/`, and a GIF line in each free skill's README. Two sit at the top of the main README.
- A GitHub Actions workflow that runs the checker on every push (`.github/workflows/skill-check.yml`).
- `skill-portability-check` (developers): finds strict-YAML, portability and missing-fallback problems in `SKILL.md` folders, with a non-zero exit code for CI.
- Five skills: `cold-email-checker` (sales), `csv-profile-and-sanity-check` (data), `job-post-decoder` (careers), `angry-customer-reply-check` (support), `invoice-checker` (finance).
- Three developer skills: `changelog-from-commits`, `readme-first-run-check`, `test-gap-finder`.
- `fact-claim-checker` (writing).
- `search-intent-page-brief` (marketing and SEO) and `accessibility-quick-audit` (developers).
- First release: free skills grouped by category, each with a `prompt.md` for any chatbot.

### Fixed
- `csv-profile-and-sanity-check` and `readme-first-run-check`: the description is now valid strict YAML (an unquoted `: ` in a description stopped some installers from loading the skill).
- Unfilled pack link placeholders in READMEs replaced with the real links.
- README wording: the About and How we test lines now cover all categories.
