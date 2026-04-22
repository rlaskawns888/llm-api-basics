from fastapi import FastAPI

from routers.emtion import router as analyze_router
from routers.category import router as category_router

app = FastAPI(title="프롬프트 테스트")

app.include_router(analyze_router)
app.include_router(category_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}