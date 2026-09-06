from fastapi import FastAPI
from app.routers import tasks, auth

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(tasks.router)

