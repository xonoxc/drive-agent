# Drive Agent

A conversational AI agent that lets you search Google Drive using natural language. Powered by Groq (Llama 3.3 70B) for intent extraction, Google Drive v3 API for file search, and Streamlit for the chat UI.

## Architecture

```
User → Streamlit Frontend → FastAPI Backend → DriveAgent → Groq LLM
                                                         → Google Drive API
```

- **Frontend** — Streamlit chat UI (`frontend/`)
- **Backend** — FastAPI server with 3 routers (`api/`)
- **Agent** — LangChain agent that extracts search filters via LLM, queries Drive, and summarizes results (`agents/`)
- **Services** — Google Drive API wrapper + query builder (`services/`)
- **Schemas** — Pydantic models for files, search filters, and chat (`schemas/`)

## Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/) (package manager)
- A Google Cloud service account with Drive API enabled and access to target Drive files/folders
- A [Groq API key](https://console.groq.com)

## Setup

```bash
# Clone and enter the project
git clone <repo-url> && cd drive-agent

# Create environment config
cp env.sample .env
# Add your GROQ_API_KEY to .env

# Place your Google service account credentials
# credentials.json (gitignored)

# Install dependencies
uv sync
```

### Run locally

```bash
# Terminal 1: Backend
uv run uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
uv run streamlit run frontend/app.py --server.address=0.0.0.0 --server.port=8501
```

### Run with Docker

```bash
docker compose up --build
```

Backend at `http://localhost:8000`, frontend at `http://localhost:8501`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/chat` | Conversational file search |
| GET | `/search` | Direct file search with filters |
| GET | `/files/{id}/download` | Download a file |

## How it works

1. You type a query like *"find my pdf invoices from last week"*
2. The structured LLM extracts search filters (mime type, name, date range)
3. Drive Service queries Google Drive via the service account
4. The main LLM summarizes the matching files naturally
5. Results appear in the chat with clickable Drive links

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Groq API key for LLM access |
| `credentials.json` | Yes | Google service account key file |
| `API_BASE_URL` | No | Backend URL for frontend (default: `http://localhost:8000`) |

## Deployment

This project can be deployed on **Render** as two separate web services:

- **Backend** — Docker runtime using `Dockerfile`, with `GROQ_API_KEY` env var and `credentials.json` as a secret file
- **Frontend** — Docker runtime using `Dockerfile.frontend`, with `API_BASE_URL` pointing to the backend
