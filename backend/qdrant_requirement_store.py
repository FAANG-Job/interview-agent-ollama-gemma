import json
from pydantic import BaseModel, Field, ValidationError
from fastapi import FastAPI
from qdrant_client import QdrantClient, models
from main import get_embeddings
from fastapi import APIRouter
from cosine_similarity import get_embeddings
from logging_config import configure_logging, get_logger

router = APIRouter(prefix="/api/ai", tags=["AI"])
from uuid import NAMESPACE_URL, uuid5

configure_logging()
logger = get_logger(__name__)

QDRANT_URL = "http://localhost:6333"
COLLECTION = "requirements"
qdrant = QdrantClient(url=QDRANT_URL)


class SaveRequirementRequest(BaseModel):
    requirement_id: str
    team: str
    requirement: str


class SearchRequirementRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


def get_qdrant_client():
    return QdrantClient(url=QdrantClient)


@router.post("/api/ai/requirements")
def save_requirement(request: SaveRequirementRequest):
    logger.info("save_requirement() is called...")
    logger.info("Embedding for the requirment =%s model=embeddinggemma", request.requirement )

    embedding_vector = get_embeddings(request.requirement)
    if not qdrant.collection_exists(COLLECTION):
        qdrant.create_collection(
            collection_name=COLLECTION,
            vectors_config=models.VectorParams(
                size=len(embedding_vector),  # 768 for your current model
                distance=models.Distance.COSINE,
            ),
        )
    logger.info(
        "embeddHw ing_created dimensions=%d model=embeddinggemma", len(embedding_vector)
    )

    point_id = str(uuid5(NAMESPACE_URL, request.requirement_id))
    qdrant.upsert(
        collection_name=COLLECTION,
        wait=True,
        points=[
            models.PointStruct(
                id=point_id,
                vector=embedding_vector,
                payload={
                    "requirement_id": request.requirement_id,
                    "team": request.team,
                    "requirement": request.requirement,
                },
            )
        ],
    )
    logger.info("requirement_stored requirement_id=%s", request.requirement_id)
    return {"requirement_id": request.requirement_id, "stored": True}


@router.post("/api/ai/search_requirement")
def search_requirement(request: SearchRequirementRequest):
    logger.info("search_requirement() is called...")
    logger.info("query=%s", request)

    embedding_vector = get_embeddings(request.query)
    points = qdrant.query_points(
        collection_name=COLLECTION,
        query=embedding_vector,
        with_payload=True,
        limit=request.limit,
    ).points

    matches = []
    for point in points:
        match = {
            "score": point.score,
            "requirement_id": point.payload.get("requirement_id"),
            "team": point.payload.get("team"),
            "requirement": point.payload.get("requirement"),
        }
        matches.append(match)
        logger.info("search_result=%s", json.dumps(match, ensure_ascii=False))        

    return matches
