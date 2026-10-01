from fastapi import FastAPI
from fastapi import HTTPException
from ollama_system_user_prompt import get_response
from pydantic import BaseModel, Field, ValidationError
import json
from cosine_similarity import get_embeddings, cosine_similarity
from qdrant_requirement_store import router as requirements_router
from logging_config import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

SYSTEM_PROMPT = (
    "You are a senior QA engineer. "
    "Create exactly 5 distinct test scenarios for the supplied requirement. "
    "Each scenario must contain: scenario_id, scenario_name, description, "
    "steps, and expected_result. "
    "The steps field must be a list of one or more short strings. "
    "Return one valid JSON object with a test_scenarios array only. "
    "Do not use Markdown, code fences, or explanatory text."
)

tasks = [
    {"id": 1, "name": "Create FastAPI endpoint", "status": "completed"},
    {"id": 2, "name": "Connect Ollama", "status": "in-progress"},
]


class GenerationOptions(BaseModel):
    num_ctx: int = Field(default=4096, ge=512, le=8192)
    temperature: float = Field(default=0, ge=0, le=1)
    seed: int = 42
    num_predict: int = Field(default=800, ge=50, le=2000)


class TestScenarioRequest(BaseModel):
    requirement: str
    options: GenerationOptions = Field(default_factory=GenerationOptions)


class TestScenario(BaseModel):
    scenario_id: str
    scenario_name: str
    description: str
    steps: list[str] = Field(min_length=1)
    expected_result: str


class TestScenarioResponse(BaseModel):
    test_scenarios: list[TestScenario] = Field(min_length=5, max_length=5)


app = FastAPI(title="Rohit", version="o.1Draft")
app.include_router(requirements_router)


@app.get("/api/v1/tasks")
def get_tasks():
    logger.info(
        "endpoint=%s() path=%s",
        get_tasks.__name__,
        app.url_path_for(get_tasks.__name__),
    )
    for task in tasks:
        logger.info("Task to be returned=%s", task)
    return tasks


@app.get("/api/v1/tasks/{task_id}")
def get_tasks(task_id: int):
    logger.info(
        "endpoint=%s() path=%s",
        get_tasks.__name__,
        app.url_path_for(get_tasks.__name__),
    )
    for task in tasks:
        if task["id"] == task_id:
            logger.info("Task to be returned=%s", task)
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/api/v1/tasks")
def create_task(taskName: str):
    new_task = {"id": len(tasks) + 1, "name": taskName, "status": "new"}
    tasks.append(new_task)
    return new_task


@app.put("/api/v1/tasks")
def update_task(task_id: int, status: str):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            return task
    raise HTTPException(status_code=404, detail="Recrod not found")


@app.delete("/api/v1/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/api/ai/generate-test-scenarios")
def generate_test_scenario(request: TestScenarioRequest):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": request.requirement,
        },
    ]
    response = get_response(messages, request.options.model_dump())
    response = response.strip()
    if response.startswith("```json"):
        response = response[len("```json") :].strip()
    elif response.startswith("```"):
        response = response[len("```") :].strip()

    if response.endswith("```"):
        response = response[:-3].strip()

    try:
        print(response)
        test_scenarios_json = json.loads(response)

        return TestScenarioResponse.model_validate(test_scenarios_json)
    except json.JSONDecodeError as error:
        raise HTTPException(
            status_code=502,
            detail=(
                f"Local LLM returned invalid JSON: {error.msg}. "
                f"Line {error.lineno}, column {error.colno}."
            ),
        )

    except ValidationError:
        raise HTTPException(
            status_code=502,
            detail="The local LLM response does not match the required test-scenario format.",
        )


class Embeddings(BaseModel):
    requirement_a: str
    requirement_b: str


@app.post("/api/ai/compare_requirement")
def get_requirement(requirement_a: str, requirement_b: str):
    embedding_a = get_embeddings(requirement_a)
    embedding_b = get_embeddings(requirement_b)
    return cosine_similarity(embedding_a, embedding_b)


class ChatRequest(BaseModel):
    prompt: str
