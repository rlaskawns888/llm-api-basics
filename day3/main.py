from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# "로그인이 안되고 500 에러가 나요"

class ErrorRequest(BaseModel):
    content: str

class ErrorResponose(BaseModel):
    category: str
    priority: str
    summary: str

@app.post("/error", response_model=ErrorResponose)
def error_check(request: ErrorRequest):
    system_promt = """
        너는 로그를 분석하는 분석가야

        에러 로그를 확인하고 규칙에 맞춰서 나에게 응답을 해줘 

        - 규칙
        1. JSON으로 응답해라 
        2. "서버", "클라이언트" 카테고리 분류
        3. "높음", "중간", "낮음" 로그 상태 분류

        - JSON 예시
        {
            "category": "서버",
            "priority": "높음",
            "summary": "로그인 중 500 에러 발생"
        }
    """

    try:
        response = client.chat.completions.create (
            model="gpt-5.4-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": system_promt},
                {"role": "user", "content": request.content}
            ]
        )
    except Exception as e:
        raise HTTPException (
            status_code=502,
            detail={
                "message": "AI CALL FAIL"
                , "error": str(e)
            }
        )
    
    content = response.choices[0].message.content
    print("RAW: ", content)

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "OpenAI 응답 JSON 파싱 실패",
                "raw_response": content
            }
        )

    return parsed
