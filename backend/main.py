from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException


tasks = [
    {"id": 1, "name": "Create FastAPI endpoint", "status": "completed"},
    {"id": 2, "name": "Connect Ollama", "status": "in-progress"}
]

    
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
    
class ChatRequest(BaseModel):
    prompt: str
