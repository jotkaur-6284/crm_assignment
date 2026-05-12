# AI CRM Backend

This backend scaffold uses FastAPI with SQLAlchemy and a Groq AI extraction helper.

## Setup

1. Open a terminal in `backend/`
2. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy environment config:
   ```bash
   copy .env.example .env
   ```
5. Update `.env` with your database URL and Groq API key.

## Run

```bash
uvicorn main:app --reload
```

## API Endpoints

- `POST /api/parse-chat` - parse chat text into interaction fields
- `POST /api/log-interaction` - save structured HCP interaction
- `GET /api/interactions` - list saved interactions
- `POST /api/ai-suggest` - AI-powered follow-up suggestion

## Notes

- Keep API keys in `.env` only.
- Frontend should call `/api/parse-chat` and `/api/log-interaction`.
- If `GROQ_API_KEY` is missing, the AI service uses a simple fallback parser.
