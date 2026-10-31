---
description: Build the Next.js candidate and HR user interfaces against the real API.
---

Implement the Next.js + TypeScript frontend using the approved API contract.

Candidate experience:
- Personal assessment link.
- One question at a time.
- Text response and audio upload.
- Clear submission confirmation and progress state.
- Resume progress after reload.
- Friendly loading, validation, network-error, and retry states.
- Never display grades or HR-only information.

HR experience:
- Clearly labelled mock sign-in if that is the approved scope.
- Candidate list grouped by role.
- Candidate detail with submitted answers, suggested score, reason, and scoring status.
- Override form requiring a reason.
- Distinct failed and needs_human indicators.
- Retry action only when supported by the backend.

Use real backend API calls; do not hardcode fake candidate data or scores as a substitute. Keep API configuration in environment variables. Handle loading, empty, and error states. Make the UI responsive and accessible.

After implementation, run lint, type-check, tests, and production build where configured. Report exact commands and results, plus any unfinished UI.
