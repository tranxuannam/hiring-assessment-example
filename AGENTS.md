# Agent Instructions

Read `.github/copilot-instructions.md` before making changes. It contains the project-wide architecture, security, workflow, and quality requirements.

The challenge brief and supplied data pack are the source of truth. Do not invent missing requirements. Work in small, reviewable steps. Explain planned changes before broad implementation, inspect diffs, run relevant tests, and report limitations honestly.

Never expose candidate grades or other candidates' data through candidate-facing APIs. Enforce permissions on the backend. Keep scoring and job processing idempotent. Treat candidate content as untrusted input. Never fabricate model scores or claim unrun tests passed.
