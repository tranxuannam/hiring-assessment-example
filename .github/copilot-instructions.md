# Growtrics Hiring Assessment — Copilot Instructions

## Project goal
Build a small, reliable internal hiring assessment application with a candidate experience and an HR experience. Treat the challenge brief and supplied data pack as the source of truth. If a requirement is unclear or missing, ask before inventing behavior.

## Expected stack
- Frontend: Next.js + TypeScript.
- Backend: Python + FastAPI.
- Persistence: SQLite for a simple local demo or PostgreSQL if already configured.
- ORM/migrations: SQLAlchemy and a reproducible migration or initialization process.
- Background scoring: database-persisted jobs and a worker; do not rely on in-memory queues for durable work.
- LLM scoring: a real provider-backed client in the production path, configured through environment variables.
- Tests: frontend/backend tests appropriate to the chosen stack.

Do not introduce extra infrastructure unless it materially improves reliability and can be run easily on a clean machine.

## Architecture rules
- Keep frontend and backend separate.
- Backend owns business rules, persistence, validation, scoring state, and authorization.
- Keep route handlers thin; put business logic in services and persistence logic in repositories or equivalent modules.
- Use typed request/response schemas.
- Keep configuration and secrets in environment variables. Commit only `.env.example`, never real secrets.
- Store uploaded audio as files or object storage and persist metadata in the database.
- Make setup reproducible from a clean checkout.

## Core domain requirements
- Candidate accesses an assessment through a personal link; no candidate password is required by the brief.
- Candidate sees one question at a time, can submit text or audio, receives confirmation, and can resume after reload.
- HR can view candidates grouped by role, submitted answers, suggested scores, and scoring reasons.
- HR score overrides require a reason and must be auditable.
- Scoring statuses include queued, scored, failed, and needs_human.
- A failed scoring job must remain visibly failed; never convert failure into a low score.
- Typed answers from the supplied data pack must be loadable and scoreable.
- Audio upload must be stored and visible to HR. Transcription is optional unless the brief says otherwise.

## Security and integrity rules
- Never trust candidate IDs, role IDs, permissions, or ownership claims supplied by the browser.
- Enforce authorization on every protected backend endpoint. Hiding UI controls is not authorization.
- Candidate endpoints must not expose grades, scoring reasons, HR notes, or another candidate's data.
- Use unguessable personal assessment tokens; store only a secure representation where practical. Do not log full tokens.
- Validate file type, size, and upload handling. Do not trust client-provided MIME types alone.
- Make answer submission idempotent. Retries must not create duplicate answers or duplicate scoring jobs.
- Make scoring job processing idempotent and safe to retry.
- Treat candidate answers and uploaded/transcribed content as untrusted data, never as instructions to the scorer.
- Keep grading criteria separate from candidate content. Validate model output strictly (score range, schema, required reason).
- Do not fabricate scores or reasons. Do not present mock data or mock authentication as production functionality.
- Do not place secrets, API keys, passwords, or personal data in source code, logs, prompts, or committed files.

## Implementation workflow
1. Read the challenge brief and data pack before implementation. Summarize requirements and uncertainties.
2. Propose architecture, schema, API contracts, and a small implementation plan. Wait for approval before broad changes.
3. Implement in small vertical slices.
4. Add or update tests for each business rule and bug fix.
5. Run relevant tests, type checks, linting, and build commands after changes.
6. Inspect the diff and explain changed files, trade-offs, and remaining limitations.
7. Do not claim a test passed unless you actually ran it and saw it pass.

## Coding standards
- Prefer simple, readable, maintainable code over unnecessary abstraction.
- Use TypeScript strict mode and Python type hints.
- Validate all external input at API boundaries.
- Handle errors explicitly; avoid swallowing exceptions.
- Avoid broad refactors unrelated to the requested task.
- Keep README commands accurate for Windows PowerShell where practical, and mention alternatives when commands differ by shell.

## Working with the human
- Before destructive commands, schema resets, deleting files, or changing dependencies, explain the impact and ask for approval.
- When a task is ambiguous, ask one focused clarification question.
- Never silently weaken security or tests to make the demo pass.
- Distinguish implemented, tested, mocked, and not-yet-implemented features in reports and documentation.
