from fastapi import FastAPI
from fastapi import HTTPException
from ollama_system_user_prompt import get_response
from pydantic import BaseModel,Field
import json
SYSTEM_PROMPT = (
    "You are a senior QA engineer. "
    "Create test scenarios for the supplied requirement. "
    "Return one valid JSON object only. Do not use Markdown or code fences."
)

tasks = [
    {"id": 1, "name": "Create FastAPI endpoint", "status": "completed"},
    {"id": 2, "name": "Connect Ollama", "status": "in-progress"}
]



class GenerationOptions(BaseModel):
    num_ctx: int = Field(default=4096, ge=512, le=8192)
    temperature: float = Field(default=0, ge=0, le=1)
    seed: int = 42
    num_predict: int = Field(default=800, ge=50, le=2000)

class TestScenarioRequest(BaseModel):
    requirement: str
    options: GenerationOptions = Field(default_factory=GenerationOptions)

app = FastAPI(title="Rohit", version="o.1Draft")
    
@app.get("/api/v1/tasks")
def get_tasks():
    return tasks
    
    
@app.get("/api/v1/tasks/{task_id}")
def get_tasks(task_id: int):
    for task in tasks :
        if(task["id"] == task_id):
            return task;
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/api/v1/tasks")
def create_task(taskName: str):
    new_task = {
    "id": len(tasks)+1, 
    "name": taskName, 
    "status": "new"
    }
    tasks.append(new_task);
    return new_task;
    
@app.put("/api/v1/tasks")
def update_task(task_id: int, status:str):
    for task in tasks:
        if(task["id"] == task_id):
            task["status"] =status;
            return task;
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
    response = get_response(messages,request.options.model_dump())
    response = response.strip()
    if response.startswith("```json"):
        response = response[len("```json"):].strip()
    elif response.startswith("```"):
        response = response[len("```"):].strip()

    if response.endswith("```"):
        response = response[:-3].strip()

    test_scenarios_json = json.loads(response)
    return test_scenarios_json

    

class ChatRequest(BaseModel):
    prompt: str
