from fastapi import FastAPI, HTTPException
import requests
import math
from logging_config import configure_logging, get_logger
from settings import settings

configure_logging()
logger = get_logger(__name__)


def get_embeddings(text: str) -> list[float]:
    logger.info("get_embeddings() text =%s", text)
    try:
        response = requests.post(
            f"{settings.OLLAMA_URL.rstrip('/')}/api/embed",
            json={
                "model": settings.OLLAMA_EMBED_MODEL,
                "input": text,
            },
            # Rohit - Take time out value from .env file
            timeout=settings.OLLAMA_TIMEOUT_SECONDS,
        )
    except requests.exceptions.Timeout as exc:
        logger.error("Ollama timeout: operation=embedding error=%s", exc)
        raise HTTPException(
            status_code=504,
            detail="Embedding generation timed out. Please try again.",
        ) from exc
    except requests.exceptions.ConnectionError as exc:
        logger.error("Ollama unavailable: operation=embedding error=%s", exc)
        raise HTTPException(
            status_code=503,
            detail="AI service is unavailable. Please try again later.",
        ) from exc

    response.raise_for_status()
    # print(response.json()["embeddings"][0])
    return response.json()["embeddings"][0]


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    # Rohit - So easy to implement in Python!.
    # If vector_a = [1, 2, 3] and vector_b = [4, 5, 6], then zip pairs
    # them into: (1, 4), (2, 5), and (3, 6).
    dot_product = sum(value_a * value_b for value_a, value_b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(value * value for value in vector_a))

    magnitude_b = math.sqrt(sum(value * value for value in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)
