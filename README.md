# Hiring Assessment

## Backend

The FastAPI backend uses SQLAlchemy with a persistent database configured by
`DATABASE_URL`. Local development defaults to SQLite; set `DATABASE_URL` to a
PostgreSQL connection string for production. The application creates the
current schema on startup through `Base.metadata.create_all`.

From `D:\projects\hiring-assessment\hiring-assessment-example` in Windows
PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
Copy-Item .env.example .env
python -m pytest
python -m uvicorn app.main:app --reload
```

The health endpoint is available at `GET /health`.

### LLM scoring

Scoring uses the configured OpenAI-compatible API. Set `LLM_API_KEY` and
optionally `LLM_BASE_URL` and `LLM_MODEL` in `.env`; do not commit credentials.
The scoring service persists each job and score, accepts only JSON with an
integer score from 1 through 4 and a reason, and treats candidate answers as
untrusted data. Provider failures retry with backoff until
`SCORING_MAX_ATTEMPTS`; malformed model output is marked `needs_human`.
