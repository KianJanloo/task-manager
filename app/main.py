from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
)

class CreateTask(BaseModel):
    title: str
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=5)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"message": "Hello!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id,
        "name": f"User {user_id}",
    }
    
@app.get("/tasks")
def get_tasks(status: str = "pending", limit: int = 10):
    return {
        "status": status,
        "limit": limit,
    }
    
@app.post("/tasks")
def create_task(task: CreateTask):
    return task