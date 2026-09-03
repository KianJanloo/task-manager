from fastapi import FastAPI
from app.routers import auth

app = FastAPI(
    title="Task Manager",
    version="1.0.0"
)


@app.get('/health')
def health_check():
    return {"status": "healthy"}


app.include_router(auth.router)