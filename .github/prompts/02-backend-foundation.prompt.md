---
description: Implement the FastAPI backend foundation and persistence layer.
---

Implement the backend foundation for the approved architecture.

Requirements:
- FastAPI application with clear module boundaries.
- SQLAlchemy models and reproducible database setup/migrations.
- Pydantic schemas for API input/output.
- Environment-based configuration and `.env.example`.
- Health-check endpoint.
- Models for roles, candidates, questions, answers, scoring jobs, scores, and score-override audit records where required by the approved design.
- Validation, consistent error responses, and logging that excludes secrets and personal assessment tokens.
- Automated tests for database constraints and core services.

Do not use in-memory storage for durable application data or background jobs. Do not build frontend yet.

Before finishing:
1. Run backend tests and report the exact command and result.
2. Explain files created/changed.
3. List setup commands for Windows PowerShell.
4. Report any incomplete behavior honestly.
