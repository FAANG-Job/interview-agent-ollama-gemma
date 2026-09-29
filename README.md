# Local LLM Engineering Agent

A local AI-assisted engineering foundation built with Python, Ollama, Gemma, and FastAPI.

This project demonstrates how a local large language model can be accessed through Python and exposed through REST APIs. It is a foundation for future AI-assisted engineering capabilities, including specification generation, test-scenario drafting, and implementation guidance.

## Current capabilities

- Python client for Ollama's local Chat API
- Local Gemma model integration through Ollama
- Role-based prompting with `system` and `user` messages
- Conversation-history support using ordered messages
- Configurable LLM generation settings: context window, temperature, seed, and token limit
- HTTP error handling for Ollama API calls
- FastAPI server with basic REST endpoints
- Interactive API documentation through FastAPI Swagger UI

## Technology stack

- Python
- FastAPI
- Uvicorn
- Ollama
- Gemma 3
- Requests

## Architecture

```text
REST API client or future Angular UI
                |
                v
          FastAPI application
                |
                v
       Python LLM client
                |
                v
      Ollama local Chat API
                |
                v
          Gemma local model
```

## Prerequisites

- Python 3.10 or later
- [Ollama](https://ollama.com/)
- Gemma model installed locally

Install the required Python packages:

```powershell
py -m pip install requests
py -m pip install "fastapi[standard]"
```

Download the local model:

```powershell
ollama pull gemma3:1b
```

## Run the FastAPI application

From the `backend` folder, run:

```powershell
py -m uvicorn main:app --reload
```

The application starts locally at `http://127.0.0.1:8000`.

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Current REST endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | Confirms that the FastAPI application is running |
| GET | `/api/v1/tasks` | Returns all sample tasks |
| GET | `/api/v1/tasks/{task_id}` | Returns one task by ID |
| POST | `/api/v1/tasks` | Creates a sample task |
| PUT | `/api/v1/tasks/{task_id}` | Updates a task status |
| DELETE | `/api/v1/tasks/{task_id}` | Deletes a sample task |

The task endpoints currently use in-memory sample data. The data resets whenever the server restarts.

## Run the local Ollama chat client

Ensure Ollama is running. From the `backend` folder, run:

```powershell
py .\ollama_system_user_prompt.py
```

The client sends role-based messages to the local Gemma model and prints the generated response.

## Current scope

This project is currently a local LLM and FastAPI REST API foundation. It is not yet a fully autonomous AI agent or a production-ready service.

The current REST endpoints demonstrate FastAPI development and provide a base for connecting controlled AI-assisted workflows to a UI or other services.

## Planned enhancements

- [ ] Add a FastAPI endpoint that calls the local Ollama/Gemma model
- [ ] Add request and response models for AI-assisted engineering use cases
- [ ] Generate requirement specifications and test-scenario drafts
- [ ] Add an Angular user interface
- [ ] Add unit and API tests
- [ ] Add structured logging and health/readiness checks
- [ ] Add Docker support
- [ ] Add Kubernetes deployment configuration
- [ ] Add controlled context retrieval and human-review workflows

## Why local LLMs?

Running Gemma locally through Ollama supports private experimentation with LLM application development and avoids reliance on external model APIs during early development. It also provides a practical foundation for evaluating local model-integration patterns, prompt handling, and controlled AI-assisted engineering workflows.
