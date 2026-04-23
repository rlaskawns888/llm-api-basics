from fastapi import APIRouter

from schemas.ask_schema import AskRequest, AskResponse
from services.llm_service import LLMService

router = APIRouter(prefix="/ask", tags=["Ask"])

llm_service = LLMService()

@router.post("", response_model=AskResponse)
def ask_question(request: AskRequest):
    answer = llm_service.ask(request.question)
    return AskResponse(answer=answer)