# Local LLM Application Engineering Agent

A local AI-assisted engineering application built with Python, FastAPI, Ollama, Gemma, and embedding models.

This project demonstrates how local AI models can be accessed through Python and exposed through REST APIs. It provides two controlled AI-assisted engineering capabilities:

* Structured QA test-scenario generation from software requirements
* Semantic requirement comparison using embeddings and cosine similarity

## Current capabilities

* Python client for Ollama's local APIs
* Local `gemma3:1b` integration for text generation
* Local `embeddinggemma` integration for semantic similarity
* Role-based prompting with fixed `system` instructions and user-provided requirements
* Conversation-history support using ordered messages
* Configurable LLM generation settings: context window, temperature, seed, and token limit
* HTTP error handling for Ollama API calls
* FastAPI server with REST endpoints
* Interactive API documentation through FastAPI Swagger UI
* AI endpoint that generates test scenarios from a software requirement
* Semantic-similarity endpoint that compares two requirements
* Request and response validation using Pydantic models
* Markdown code-fence cleanup, trailing-comma cleanup, JSON parsing, and response validation for local model responses
* Controlled `502` error responses for malformed local-model output

## Technology stack

* Python
* FastAPI
* Uvicorn
* Ollama
* Gemma 3
* EmbeddingGemma
* Requests
* Pydantic

## Local models and responsibilities

The FastAPI backend selects the appropriate local model for each endpoint. API clients do not select models directly.

| Model            | Purpose                                                                   | Endpoint                               |
| ---------------- | ------------------------------------------------------------------------- | -------------------------------------- |
| `gemma3:1b`      | Generates structured QA test-scenario drafts                              | `POST /api/ai/generate-test-scenarios` |
| `embeddinggemma` | Converts requirement text into vectors for semantic similarity comparison | `POST /api/ai/compare-requirements`    |

## Architecture

```text
REST API client or future Angular UI
                |
                v
          FastAPI application
                |
        ┌───────┴────────┐
        v                v
QA test scenarios   Requirement similarity
        |                |
        v                v
   gemma3:1b       embeddinggemma
        |                |
        v                v
Structured JSON    Vectors + cosine similarity
```

## Prerequisites

* Python 3.10 or later
* [Ollama](https://ollama.com/)
* Local Gemma and embedding models

Install the required Python packages:

```powershell
py -m pip install requests
py -m pip install "fastapi[standard]"
```

Download the local models:

```powershell
ollama pull gemma3:1b
ollama pull embeddinggemma
```

## Run the FastAPI application

Ensure Ollama is running. From the `backend` folder, run:

```powershell
py -m uvicorn main:app --reload
```

The application starts locally at:

```text
http://127.0.0.1:8000
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Current REST endpoints

| Method | Endpoint                          | Purpose                                                          |
| ------ | --------------------------------- | ---------------------------------------------------------------- |
| GET    | `/health`                         | Confirms that the FastAPI application is running                 |
| GET    | `/api/v1/tasks`                   | Returns all sample tasks                                         |
| GET    | `/api/v1/tasks/{task_id}`         | Returns one task by ID                                           |
| POST   | `/api/v1/tasks`                   | Creates a sample task                                            |
| PUT    | `/api/v1/tasks/{task_id}`         | Updates a task status                                            |
| DELETE | `/api/v1/tasks/{task_id}`         | Deletes a sample task                                            |
| POST   | `/api/ai/generate-test-scenarios` | Generates QA test-scenario drafts using local Gemma              |
| POST   | `/api/ai/compare-requirements`    | Compares two requirements using embeddings and cosine similarity |

The task endpoints currently use in-memory sample data. The data resets whenever the server restarts.

## Generate test scenarios with the local LLM

Send a `POST` request to:

```text
/api/ai/generate-test-scenarios
```

The API applies a fixed QA system prompt in the backend. The client supplies only the business requirement and optional generation settings.

Example request:

```json
{
  "requirement": "Users can log in using a registered email address and correct password.",
  "options": {
    "num_ctx": 4096,
    "temperature": 0,
    "seed": 42,
    "num_predict": 800
  }
}
```

The `requirement` field is required. The `options` field is optional; backend defaults are used when it is omitted.

The endpoint returns exactly five validated test scenarios. If the local model returns malformed JSON or an invalid test-scenario structure, the API returns a controlled `502` error response.

Example response:

```json
{
  "test_scenarios": [
    {
      "scenario_id": "1",
      "scenario_name": "Valid Login - Successful Access",
      "description": "Verify a registered user can log in with a valid email address and correct password.",
      "steps": [
        "Enter a registered email address.",
        "Enter the correct password.",
        "Click the Login button."
      ],
      "expected_result": "The user is authenticated and redirected to the dashboard."
    },
    {
      "scenario_id": "2",
      "scenario_name": "Incorrect Password - Login Failure",
      "description": "Verify login is rejected when an incorrect password is entered.",
      "steps": [
        "Enter a registered email address.",
        "Enter an incorrect password.",
        "Click the Login button."
      ],
      "expected_result": "Login is rejected and a generic invalid-credentials message is displayed."
    }
  ]
}
```

## Compare requirements with semantic similarity

Send a `POST` request to:

```text
/api/ai/compare-requirements
```

The endpoint uses `embeddinggemma` to convert both requirements into numerical vectors. It then calculates their cosine similarity score.

Cosine similarity compares the semantic meaning of the two texts. A higher score generally indicates more similar requirements. Scores are most useful when comparing complete requirements rather than very short words or names.

Example request with related requirements:

```json
{
  "requirement_a": "Users can reset a forgotten password using an email link.",
  "requirement_b": "Allow customers to change their password through email verification."
}
```

Example response:

```json
{
  "similarity_score": 0.53,
  "interpretation": "Moderately similar requirements"
}
```

Example request with unrelated requirements:

```json
{
  "requirement_a": "Users can reset a forgotten password using an email link.",
  "requirement_b": "Administrators can export monthly sales reports to CSV."
}
```

Example response:

```json
{
  "similarity_score": 0.28,
  "interpretation": "Low similarity"
}
```

Similarity scores may vary slightly based on the local embedding model and the supplied text.

## Run the local Ollama chat client

Ensure Ollama is running. From the `backend` folder, run:

```powershell
py .\interactive_ollama_system_user_prompt.py
```

The client sends role-based messages to the local Gemma model and prints the generated response.

## Current scope

This project is a local LLM and FastAPI REST API foundation with initial AI-assisted QA and semantic-similarity capabilities. It is not yet a fully autonomous AI agent or a production-ready service.

Generated test scenarios are drafts intended for human review. Semantic-similarity scores are intended to help identify potentially related requirements; they do not replace engineering review.

## Planned enhancements

* [ ] Add unit and API tests
* [ ] Generate requirement specifications and other AI-assisted engineering drafts
* [ ] Add an Angular user interface
* [ ] Add structured logging and health/readiness checks
* [ ] Store tasks and reviewed AI outputs in a database
* [ ] Add semantic search across a stored requirement collection
* [ ] Add controlled context retrieval and human-review workflows
* [ ] Add Docker support
* [ ] Add Kubernetes deployment configuration

## Why local AI models?

Running Gemma and embedding models locally through Ollama supports private experimentation with AI application development and avoids reliance on external model APIs during early development.

The project provides a practical foundation for evaluating local model integration, prompt handling, structured outputs, semantic similarity, and controlled AI-assisted engineering workflows.
