# Local LLM Engineering Agent

A local AI-assisted engineering foundation built with Python, Ollama, Gemma, and FastAPI.

This project demonstrates how a local large language model can be accessed through Python and exposed through REST APIs. It includes a controlled AI-assisted QA workflow that generates structured test-scenario drafts from software requirements.

## Current capabilities

* Python client for Ollama's local Chat API
* Local Gemma 3 integration through Ollama
* Role-based prompting with fixed `system` instructions and user-provided requirements
* Conversation-history support using ordered messages
* Configurable LLM generation settings: context window, temperature, seed, and token limit
* HTTP error handling for Ollama API calls
* FastAPI server with REST endpoints
* Interactive API documentation through FastAPI Swagger UI
* AI endpoint that generates test scenarios from a software requirement
* Request validation using Pydantic models
* Optional generation settings supplied through the API request
* Markdown code-fence cleanup and JSON parsing for local model responses

## Technology stack

* Python
* FastAPI
* Uvicorn
* Ollama
* Gemma 3
* Requests
* Pydantic

## Architecture

```text
REST API client or future Angular UI
                |
                v
          FastAPI application
                |
                v
   Fixed QA system prompt + user requirement
                |
                v
       Python LLM client
                |
                v
      Ollama local Chat API
                |
                v
          Gemma local model
                |
                v
   Structured test-scenario JSON response
```

## Prerequisites

* Python 3.10 or later
* [Ollama](https://ollama.com/)
* Gemma model installed locally

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

| Method | Endpoint                          | Purpose                                             |
| ------ | --------------------------------- | --------------------------------------------------- |
| GET    | `/health`                         | Confirms that the FastAPI application is running    |
| GET    | `/api/v1/tasks`                   | Returns all sample tasks                            |
| GET    | `/api/v1/tasks/{task_id}`         | Returns one task by ID                              |
| POST   | `/api/v1/tasks`                   | Creates a sample task                               |
| PUT    | `/api/v1/tasks/{task_id}`         | Updates a task status                               |
| DELETE | `/api/v1/tasks/{task_id}`         | Deletes a sample task                               |
| POST   | `/api/ai/generate-test-scenarios` | Generates QA test-scenario drafts using local Gemma |

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
    },
    {
      "scenario_id": "3",
      "scenario_name": "Unregistered Email - Login Failure",
      "description": "Verify login is rejected for an unregistered email address.",
      "steps": [
        "Enter an unregistered email address.",
        "Enter any password.",
        "Click the Login button."
      ],
      "expected_result": "Login is rejected and a generic invalid-credentials message is displayed."
    },
    {
      "scenario_id": "4",
      "scenario_name": "Invalid Email Format",
      "description": "Verify email-format validation before login is submitted.",
      "steps": [
        "Enter an invalid email address format.",
        "Enter any password.",
        "Click the Login button."
      ],
      "expected_result": "The application displays an email-format validation message."
    },
    {
      "scenario_id": "5",
      "scenario_name": "Empty Required Fields",
      "description": "Verify validation when email and password fields are empty.",
      "steps": [
        "Leave the email field empty.",
        "Leave the password field empty.",
        "Click the Login button."
      ],
      "expected_result": "The application displays required-field validation messages."
    }
  ]
}
```

## Run the local Ollama chat client

Ensure Ollama is running. From the `backend` folder, run:

```powershell
py .\interactive_ollama_system_user_prompt.py
```

The client sends role-based messages to the local Gemma model and prints the generated response.

## Current scope

This project is a local LLM and FastAPI REST API foundation with an initial AI-assisted QA capability. It is not yet a fully autonomous AI agent or a production-ready service.

Generated test scenarios are drafts intended for human review. The project provides a base for connecting controlled AI-assisted engineering workflows to a UI or other services.

## Planned enhancements

* [ ] Add Pydantic response models for generated test scenarios
* [ ] Add controlled error responses for malformed model output
* [ ] Generate requirement specifications and other AI-assisted engineering drafts
* [ ] Add an Angular user interface
* [ ] Add unit and API tests
* [ ] Add structured logging and health/readiness checks
* [ ] Store tasks and reviewed AI outputs in a database
* [ ] Add Docker support
* [ ] Add Kubernetes deployment configuration
* [ ] Add controlled context retrieval and human-review workflows

## Why local LLMs?

Running Gemma locally through Ollama supports private experimentation with LLM application development and avoids reliance on external model APIs during early development. It also provides a practical foundation for evaluating local model-integration patterns, prompt handling, structured outputs, and controlled AI-assisted engineering workflows.
