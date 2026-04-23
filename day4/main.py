from fastapi import FastAPI

from routers.ask_router import router as ask_router
from exceptions.handlers import register_exception_handlers

app = FastAPI(title="LLM Ask API")

register_exception_handlers(app)

app.include_router(ask_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}