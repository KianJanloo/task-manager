from fastapi import FastAPI
from app.routers import tasks, auth, notes, user

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}}
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(tasks.router)
app.include_router(notes.router)