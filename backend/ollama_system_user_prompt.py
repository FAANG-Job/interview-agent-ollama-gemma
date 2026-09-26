"""
Local LLM Chat Client with Ollama and Gemma 3.

This program sends role-based system and user prompts to a locally running
Gemma model through Ollama's Chat API. It configures response generation,
handles HTTP errors, and returns the model's generated answer.
"""
import requests

def get_response(messages):
    """
    Send role-based chat messages to the local Gemma model through Ollama.

    Generation settings:
    - temperature=0: reduces randomness for more consistent responses.
    - seed=42: uses a fixed random seed to improve repeatability.
    - num_predict=10: limits the response to a maximum of 10 generated tokens.

    Args:
        messages (list): System, user, and optional assistant chat messages.

    Returns:
        str: The generated response from Gemma.
    """
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "gemma3:1b",
            "messages": messages,
            "stream": False,
            "options": {
                "num_ctx": 4096,       # Context-window capacity
                "temperature": 0,
                "seed": 42,
                "num_predict": 150,
            },
        },
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["message"]["content"]

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a math assistant."},
        {"role": "user", "content": "Divide 5 by 5 and add 1 to resuts?"}
    ]
    print("Gemma:", get_response(messages))


