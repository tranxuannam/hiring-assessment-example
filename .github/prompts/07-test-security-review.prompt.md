---
description: Run a focused functional, reliability, and security review against the challenge.
---

Review the implementation against the challenge brief and repository instructions.

Inspect code and run available tests. Verify, with tests where practical:
1. Candidate cannot access HR pages/APIs or HR-only data.
2. Candidate cannot read another candidate's answers.
3. Candidate cannot access scores, scoring reasons, or HR notes.
4. Duplicate answer submission does not create duplicate scoring jobs or scores.
5. Scoring job processing and retries are idempotent.
6. Failed jobs remain failed and are never represented as low scores.
7. Score overrides require a reason and create an audit record.
8. Candidate content cannot override grading instructions.
9. Typed answers in the data pack can be imported and scored.
10. Audio files are actually stored and visible to HR.
11. Data survives application/backend restart.
12. README setup works from a clean checkout.

For each item, report PASS, FAIL, NOT TESTED, or NOT IMPLEMENTED with evidence (file/test/command). Fix only issues you can verify. Do not weaken tests or authorization to get a passing result. Never claim a command passed unless you ran it.
