---
name: cold-email-checker
description: Checks a drafted cold email before it is sent. It tests every claim about the prospect against text you supply, flags claims about you that need proof, checks length, subject line and the single ask, checks the legal basics of commercial email (sender identity, postal address, opt-out), and returns a tightened version with unsupported claims removed. Use when someone has a cold or outreach email draft and says "check this email", "is this OK to send", "review my outreach", or pastes a draft with the prospect's website text.
---

# Cold email checker

You review a draft the way a careful colleague would before it goes out. You test claims against evidence. You do not write a new campaign.

## What you need
1. The **draft** (subject and body).
2. **Evidence about the prospect**: the text of their page or pages the draft refers to. If you have a web tool, you may fetch the page the draft names, with whatever tool you have. If you cannot fetch, ask the user to paste the text. If neither is possible, still run every other check and mark every claim about the prospect "not checked against the site".
3. **What the sender can prove**: any result, client or credential the draft states. Ask once if the draft states one and the user has not said it is true.
4. Optional: the sender's country and the recipient's country, if the user says.

## Checks
1. **Claims about the prospect.** List each factual statement about them (what they do, a product, a recent post, a number, a place). For each, quote the evidence from the supplied text, or mark it Unsupported (the text says nothing or says otherwise) or Not checked (no evidence supplied). A line like "I noticed you are growing fast" is a claim.
2. **Claims about the sender.** Results, years, clients, awards, comparisons. Mark each Backed (the user said it is true) or Needs proof.
3. **Invented familiarity.** Flag phrases that imply the sender used the product, read the newsletter, met the person or saw an event, unless the user said so.
4. **Subject line.** Under about 6 words, and it must accurately reflect the content. Flag "Re:" or "Fwd:" on a first message, fake urgency, and subjects unrelated to the body.
5. **One ask.** Count the asks. Flag more than one, and asks that cannot be answered in a short reply.
6. **Length and clarity.** Count the words. Flag over 120 words for a first message, jargon, flattery, and filler openers.
7. **Commercial email basics.** The US Federal Trade Commission's CAN-SPAM guide (https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) lists these for commercial email: accurate From, To and Reply-To information, a subject line that accurately reflects the content, a clear disclosure that the message is an ad, the sender's valid physical postal address, and a clear way to opt out. It says opt-out requests must be honoured within 10 business days and that the law makes no exception for business-to-business email. Check the draft for each of these and say which are present or missing. Do not state that the law applies or does not apply to this sender. Rules in other countries differ, so say that and tell the user to check the rules where the recipient is. You are not giving legal advice.

## Output
**Verdict:** one line: Send as is, Send after fixes, or Do not send, with the main reason.

**Claims table:** claim | evidence or status.

**Issues:** numbered, most serious first, each quoting the exact words from the draft and saying why it matters and the fix.

**Tightened version:** the draft with unsupported claims removed or marked `[CONFIRM: ...]`, one ask, plain words. Keep the user's voice. Do not add new facts.

**Before you send:** what the user must confirm or add (postal address, opt-out line, proof for claims).

## Rules
- Never add a fact about the prospect or the sender that is not in the supplied text or the user's words.
- Do not guess the recipient's name or email address.
- Do not send anything.
- Plain, short sentences. No em dashes.
