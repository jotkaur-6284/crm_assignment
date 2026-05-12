# AI-First CRM Frontend & Backend

A full-stack AI-first CRM application for logging Healthcare Professional (HCP) interactions.

The project includes:
- a **React + Vite frontend** for both form-based and conversational logging,
- a **FastAPI backend** with AI extraction and persistent database storage,
- a **Groq-powered AI service** plus a fallback parser,
- a **local SQLite database** by default.

## Project Structure

```
ai-crm-frontend/
├── index.html                 # Vite entry point
├── package.json               # Frontend dependencies and scripts
├── vite.config.js             # Vite configuration
├── src/
│   ├── App.jsx                # Main app component
│   ├── main.jsx               # React entry point
│   ├── styles.css             # Global styles
│   ├── components/
│   │   ├── InteractionForm.jsx # Form for logging HCP interactions
│   │   └── ChatAssistant.jsx   # AI chat interface
│   └── store/
│       ├── store.js           # Redux store setup
│       └── interactionSlice.js# Interaction state slice
├── backend/
│   ├── main.py                # FastAPI app entrypoint
│   ├── database.py            # SQLAlchemy setup
│   ├── models.py              # DB models
│   ├── schemas.py             # Pydantic schemas
│   ├── services/
│   │   └── ai_service.py      # AI extraction service
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variables template
│   └── .env                   # Local environment file
└── README.md                  # This file
```

## Features

### Frontend
- Structured HCP interaction form
- Chat assistant for conversational data entry
- Automatic form population from AI output
- Sentiment selection buttons
- Save interaction data to the backend

### Backend
- FastAPI REST API
- AI extraction service using Groq model
- Local SQLite persistence by default
- CORS enabled for frontend communication
- Fallback extraction when Groq key is missing

### LangGraph Agent
- Uses a LangGraph AI agent to manage HCP interaction workflows
- Implements `StateGraph` with nodes and edges to define parse and summarize steps
- Supports tool routing via agent tools for:
  - `Log Interaction`
  - `Edit Interaction`
  - `Summarize Interaction`
  - `Follow Up Suggestion`
  - `Search HCP Profile`
- `Log Interaction` captures chat text, extracts entities, and converts data into saved interaction records
- `Edit Interaction` allows existing logged records to be updated through the agent tool interface
- `Summarize Interaction` distills notes into a compact summary
- `Follow Up Suggestion` recommends next sales actions
- `Search HCP Profile` is a metadata lookup stub for HCP history and sample status
- Exposes tool metadata and runtime execution endpoints for agent-driven workflows

### Architecture Flow
- Frontend (React + Redux) captures chat input and form state
- Frontend calls FastAPI endpoints for parsing, logging, and agent tools
- FastAPI routes requests to the LangGraph agent and AI service
- LangGraph uses `StateGraph` nodes, edges, and tool routing to process interactions
- Groq is used for structured JSON extraction from text
- Extracted interaction data is saved into the database

### AI Prompt Design
- The backend builds an extraction prompt for the Groq model to return structured JSON
- The prompt asks for valid keys such as `hcp_name`, `interaction_type`, `date`, `time`, `topics`, `materials_shared`, `sample_distributed`, `sentiment`, `outcomes`, and `summary`
- Example prompt pattern:
  ```text
  Extract HCP interaction details from the following note and return valid JSON with the keys: hcp_name, interaction_type, date, time, topics, materials_shared, sample_distributed, sentiment, outcomes, summary.

  Note:
  Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure.
  ```
- The backend parses the returned JSON and maps it into the frontend form

### Chat Auto Form Fill
- User types a conversation-style interaction into the chat panel
- The frontend sends chat text to `/api/parse-chat`
- The backend uses LangGraph and Groq extraction to generate structured fields
- The extracted fields are dispatched into Redux with `setInteraction(...)`
- The interaction form is populated automatically from the chat response

### Redux Flow
- The app stores a single `currentInteraction` and `messages` in Redux state
- `ChatAssistant` dispatches `setInteraction(...)` after AI extraction
- `InteractionForm` reads `data` from Redux and updates fields with `updateField(...)`
- Form save uses backend `POST /api/log-interaction` and updates Redux with saved record fields
- This creates a consistent React state flow from chat input to form save

### AI Integration
- Uses Groq `gemma2-9b-it` model for structured extraction
- Chat-based input is converted into HCP interaction fields
- Fallback regex parser available if API key is absent

## Tech Stack

- Frontend: React 18, Vite, Redux Toolkit
- Backend: Python 3.8+, FastAPI, SQLAlchemy, Pydantic
- Database: SQLite (default), optional PostgreSQL/MySQL
- AI: Groq API

## Setup

### Prerequisites
- Node.js 16+ installed
- Python 3.8+ installed
- Git installed

### Frontend Installation

1. Open a terminal in the project root:
   ```bash
   cd c:\Users\jotka\Downloads\ai-crm-frontend\ai-crm-frontend
   ```
2. Install frontend dependencies:
   ```bash
   npm install
   ```

### Backend Installation

1. Open a terminal in the backend folder:
   ```bash
   cd c:\Users\jotka\Downloads\ai-crm-frontend\ai-crm-frontend\backend
   ```
2. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the environment:
   - Windows PowerShell: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` then `.\.venv\Scripts\Activate.ps1`
   - Windows CMD: `.\.venv\Scripts\activate.bat`
   - macOS/Linux: `source .venv/bin/activate`
4. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create `.env` from `.env.example`:
   ```bash
   copy .env.example .env
   ```
6. Edit `backend/.env` with your values:
   ```env
   DATABASE_URL=sqlite:///./dev.db
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
   ```

> If you do not set `GROQ_API_KEY`, the app will still work using fallback extraction.

## Running the Application

### Start Backend

1. Ensure you are in `backend/` with `.venv` activated.
2. Run the backend server:
   ```bash
   python main.py
   ```
3. The backend will start on:
   - `http://127.0.0.1:8001`
4. Access API docs at:
   - `http://127.0.0.1:8001/docs`

### Start Frontend

1. Open a new terminal at the project root:
   ```bash
   cd c:\Users\jotka\Downloads\ai-crm-frontend\ai-crm-frontend
   ```
2. Run the Vite dev server:
   ```bash
   npm run dev
   ```
3. Open the app at:
   - `http://localhost:5173`

## Application Flow

- Frontend chat sends text to `POST /api/parse-chat`.
- Backend AI parses text into interaction fields.
- Frontend populates the form with extracted values.
- User edits values if necessary.
- Frontend sends full interaction to `POST /api/log-interaction`.
- Backend saves the record to the SQLite database.

## API Endpoints

### `POST /api/parse-chat`
- Request: `{"text": "string"}`
- Response: structured interaction fields
- Purpose: extract HCP interaction details from chat text

### `POST /api/log-interaction`
- Request: full interaction object
- Response: saved interaction with `id` and `created_at`
- Purpose: persist interaction to the database

### `GET /api/interactions`
- Response: list of saved interactions
- Purpose: retrieve stored records

### `GET /api/agent/tools`
- Response: available LangGraph agent tools and role description
- Purpose: discover the agent's toolset for HCP interactions

### `POST /api/agent/execute`
- Request: `{"tool_name": "Log Interaction", "text": "interaction text"}`
- Response: tool execution result
- Purpose: run a LangGraph AI tool by name

### `POST /api/agent/log-interaction`
- Request: `{"text": "string"}`
- Response: saved interaction object with `id` and `created_at`
- Purpose: log a new interaction via the LangGraph agent's extraction tool

### `PUT /api/agent/edit-interaction/{interaction_id}`
- Request: `{"updates": {"topics": "updated topics"}}`
- Response: updated interaction object
- Purpose: edit an existing logged interaction using the agent tool

### `POST /api/ai-suggest`
- Request: `{"text": "string"}`
- Response: suggestion and extracted interaction
- Purpose: provide follow-up guidance

## Video Demo Checklist
- Frontend walkthrough showing the chat UI and form UI
- Demonstrate all 5 LangGraph tools: Log Interaction, Edit Interaction, Summarize Interaction, Follow Up Suggestion, Search HCP Profile
- Explain LangGraph architecture: `StateGraph`, nodes, edges, and tool routing
- Explain AI flow: chat input, backend parsing, Groq JSON extraction, Redux state update, and DB save
- Show the auto-form-fill experience from chat to interaction form

## Database Schema

### `hcp_interactions`
- `id`
- `hcp_name`
- `interaction_type`
- `date`
- `time`
- `topics`
- `materials_shared`
- `sample_distributed`
- `sentiment`
- `outcomes`
- `created_at`

### `chat_logs`
- `id`
- `user_input`
- `ai_response`
- `extracted_hcp_name`
- `extracted_sentiment`
- `created_at`

## Notes

- Backend and frontend use separate terminals.
- Backend direct run is currently configured to listen on port `8001`.
- Frontend sends backend requests to `http://127.0.0.1:8001`.
- Saved data lives in `backend/dev.db` by default.

## Troubleshooting

- Backend startup failure: verify `.venv` activation and installed dependencies.
- Frontend loading issues: run `npm install` and retry `npm run dev`.
- AI extraction issues: make sure `GROQ_API_KEY` is set in `backend/.env`.
- Backend connection issues: confirm backend port and frontend backend URL match.

## Contribution

1. Fork the repository.
2. Create a feature branch.
3. Make changes and test locally.
4. Submit a pull request.

## License

This repository is provided for learning and demonstration.
Use the code responsibly.

