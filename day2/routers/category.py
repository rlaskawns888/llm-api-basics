from fastapi import APIRouter, HTTPException

from schemas.category_schema import CategoryRequest, CategoryResponse
from services.gpt_service import call_gpt_json

router = APIRouter(prefix="/category", tags=["Category"])

# {
#     "content": "결제가 두 번 됐어요"
# }
@router.post("/classify", response_model=CategoryResponse)
def classify(request: CategoryRequest):
    system_prompt = """
        너는 고객 문의를 분류하는 시스템이다.

        규칙:
        - 카테고리는 "결제", "로그인", "기타" 중 하나만 반환한다.
        - 반드시 JSON 객체로만 응답한다.
        - 설명, 코드블록, 부가 문장은 포함하지 않는다.

        출력 형식:
        {
        "category": "결제",
        "content": "사용자 입력 문장"
        }
    """

    user_prompt = f"""
        아래 문의를 분류해라.

        입력:
        {request.content}
    """

    parsed = call_gpt_json(system_prompt, user_prompt)

    if parsed.get("category") not in ["결제", "로그인", "기타"]:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "허용되지 않은 category 값",
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