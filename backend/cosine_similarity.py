from fastapi import FastAPI
import requests
import math

def get_embeddings(text: str) -> list[float]:
    response = requests.post(
        # TODO: Implement remomve hard coding .env fiel
        # Rohit - I am taking time to implement.  
            "http://localhost:11434/api/embed",
            json={
                "model": "embeddinggemma",
                "input": text,
            },
            # Rohit - Take time out value from .env file
            timeout=120,
        )
    response.raise_for_status()
    #print(response.json()["embeddings"][0])
    return response.json()["embeddings"][0]

def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float]
) -> float:
    # Rohit - So easy to implement in Python!.
    # If vector_a = [1, 2, 3] and vector_b = [4, 5, 6], then zip pairs 
    # them into: (1, 4), (2, 5), and (3, 6).
    dot_product = sum(
        value_a * value_b
        for value_a, value_b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(value * value for value in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(value * value for value in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)