from fastapi import APIRouter, HTTPException

from schemas.emtion_schema import EmotionRequest, EmotionResponse
from services.gpt_service import call_gpt_json

router = APIRouter(prefix="/emotion", tags=["Emotion"])

# {
#     "content": "나는 AI 서비스 개발자가 되었다!"
# }
@router.post("/analyze", response_model=EmotionResponse)
def analyze(request: EmotionRequest):
    system_prompt = """
        너는 사용자 문장의 감정을 분류하는 시스템이다.

        규칙:
        - 감정은 "긍정", "부정", "중립" 중 하나만 반환한다.
        - 반드시 JSON 객체로만 응답한다.l
        - 설명, 코드블록, 부가 문장은 포함하지 않는다.

        출력 형식:
        {
        "emotion": "긍정",
        "content": "사용자 입력 문장"
        }
    """

    user_prompt = f"""
        아래 문장의 감정을 분류해라.

        입력:
        {request.content}
    """

    parsed = call_gpt_json(system_prompt, user_prompt)

    if parsed.get("emotion") not in ["긍정", "부정", "중립"]:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "허용되지 않은 emotion 값",
                "parsed_response": parsed
            }
        )

    if parsed.get("content") != request.content:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "응답 content가 요청 원문과 다름",
                "parsed_response": parsed
            }
        )

    return parsed