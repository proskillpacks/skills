# Test Gap Finder: prompt and template

Use this in any chatbot (ChatGPT, Claude, Gemini and others). Nothing to install.

**How to use it**
1. Copy the diff (`git diff main...HEAD`) and the test file(s) closest to the changed code.
2. Copy everything from "COPY FROM HERE" to the end of this file and paste it into a new chat.
3. Under it, paste the diff, then each test file with a heading saying which file it is.

You get the behaviours the change adds or alters, each marked Covered, Not covered or Unknown against the tests you pasted, and proposed test cases for the gaps. The chatbot sees only what you paste, so a test in another file shows as Unknown: search for the changed names yourself before you trust "Not covered".

**Prefer to do it by hand?** For each hunk ask: what input would make this line run, and which test supplies it?

---

COPY FROM HERE

You find the test gaps in a code change. Work only from the diff and test files I paste below. You are not a coverage tool: never state a percentage and never say a test passes.

1. State in one line what the change does, as you understand it.
2. Go hunk by hunk and list each behaviour the change adds or alters in one plain sentence: new or changed branches, error paths, boundaries (empty, zero, one, maximum, off by one), new parameters and defaults, removed guards, changed return values or side effects, changed public interfaces.
3. For each behaviour search the tests I pasted for a test that would fail if the behaviour were wrong. Mark it Covered (name the test), Not covered (say what you searched) or Unknown (the test that would cover it was not pasted, or a test calls the code without asserting on this behaviour).
4. For each Not covered or Unknown behaviour that matters, propose one test: name, setup, input, expected result with the diff line you took it from, and why it matters. Rank by risk: data loss, security, money and public interfaces first. If the framework is clear, give a skeleton for the top three. If the code does not say what should happen, say so and ask.
5. Finish with what you could not see.
Do not edit anything.

Here are my diff and tests:
