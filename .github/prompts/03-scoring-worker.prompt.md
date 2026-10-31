---
description: Implement and test real LLM answer scoring and background jobs.
---

Implement the scoring service and database-backed worker according to the approved design.

Requirements:
- Use a real provider-backed LLM client in the production path, configured by environment variables.
- Keep the provider client behind an interface so tests can use a fake client.
- Score each answer from 1 to 4 against the question's grading guide.
- Request structured output containing a score and concise reason; validate it strictly.
- Treat candidate answers as untrusted data, not instructions. The grading guide and system rules must remain authoritative.
- Persist job state and result. Support queued, scored, failed, and needs_human states.
- Make processing idempotent and retries safe.
- Record useful failure information without exposing secrets.
- Never convert a provider error, malformed response, timeout, or exception into a numeric low score.
- Do not hardcode a fixed production score or canned production response.

Add tests for valid output, invalid score, malformed JSON, provider timeout/error, retry, duplicate job processing, and prompt-injection-like candidate text. Tests may use a fake client; clearly distinguish tests from production integration.

Run tests and report exact results. Explain how to configure the real provider without placing an API key in the repository.
