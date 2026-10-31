---
description: Implement candidate and HR APIs with backend-enforced authorization.
---

Implement the candidate and HR API flows from the approved API contract.

Candidate flow:
- Access the assessment using its personal link/token.
- Retrieve one question at a time.
- Submit text answers and upload audio.
- Return an immediate submission acknowledgement.
- Resume progress after reload.
- Prevent duplicate submissions and duplicate scoring jobs.
- Never return scores, grading reasons, HR notes, or another candidate's records.

HR flow:
- Implement only the authentication approach approved for this challenge. If it is a mock, label it clearly and document its limitations.
- List candidates grouped by role.
- View answers, suggested scores, reasons, and scoring status.
- Allow score override only with a mandatory reason.
- Persist an audit trail for overrides.
- Show failed and needs_human states distinctly; provide a safe retry operation for failed jobs if required.

Enforce authorization on every protected backend route. Never rely on frontend hiding. Add tests for missing/invalid tokens, candidate-to-candidate access, candidate access to HR endpoints, candidate access to grades, and unauthorized overrides.

Run tests and report exact commands/results. Do not claim security is complete without tests.
