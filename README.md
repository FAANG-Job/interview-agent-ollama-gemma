# Interview Agent — Ollama + Gemma

A local LLM chatbot foundation for an AI-powered interview-preparation application.

This project uses Python, Ollama, and the `gemma3:1b` model to send role-based chat prompts to a locally running LLM. It is the first building block toward an interview-preparation agent that can later analyse job descriptions, ask tailored questions, evaluate answers, and create preparation plans.

## What I built

- A Python client for Ollama's local Chat API
- Role-based prompting using `system` and `user` messages
- Support for passing an ordered `messages` history as conversation context
- Configurable generation behaviour with `temperature`, `seed`, and `num_predict`
- HTTP error handling with `response.raise_for_status()`
- Unit-testable API code by mocking the Ollama HTTP request

## AI concepts demonstrated

| Concept | How this project uses it |
| --- | --- |
| Local LLM | Runs Gemma locally through Ollama instead of a cloud API |
| System prompt | Defines the assistant's role and expected behaviour |
| User prompt | Supplies the request or interview answer to process |
| Conversation context | Can send prior messages again so the model can respond using recent chat history |
| Context window | Limits how much combined prompt and response content the model can process at once |
| Temperature | Controls randomness; lower values produce more consistent responses |
| Seed | Uses a fixed starting value to improve repeatability for the same prompt |
| Token limit | `num_predict` caps the length of a generated response |

## Current scope

This is currently a **local LLM chatbot**, not yet a fully autonomous AI agent.

The current demo sends a predefined system and user prompt to Gemma and returns the model's response. The next stages will add an interactive chat experience that preserves message history, an API layer, Angular UI integration, and interview-specific tools.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/)
- The Gemma model

```powershell
ollama pull gemma3:1b
py -m pip install requests
```

## Run the demo

Save the Python client as `ollama_system_user_prompt.py` and run:

```powershell
py .\ollama_system_user_prompt.py
```

The program sends a predefined system and user prompt to Ollama and prints Gemma's answer.

## Example request flow

```text
Python application
→ Ollama local Chat API
→ Gemma 3 model
→ Generated response returned to Python
```

## Testing

The API client can be tested without calling Ollama by mocking `requests.post`:

```powershell
py -m unittest -v test_ollama_system_user_prompt.py
```

## Roadmap

- [ ] Add an interactive multi-turn console chatbot
- [ ] Build a FastAPI backend endpoint
- [ ] Connect the backend to an Angular interview-practice UI
- [ ] Analyse job descriptions and extract required skills
- [ ] Generate role-specific interview questions
- [ ] Evaluate candidate answers and provide feedback
- [ ] Add persistent conversation history and relevant long-term memory
- [ ] Add tool-driven workflows to evolve the chatbot into an interview-preparation agent

## Why local LLMs?

Running Gemma through Ollama makes it possible to experiment with LLM application development locally, keeps development data on the machine, and avoids depending on a cloud model API during early development.
