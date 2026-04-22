import os
import json
from openai import OpenAI
from fastapi import HTTPException

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_gpt_json(system_prompt: str, user_prompt: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-5.4-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "OpenAI 호출 실패",
                "error": str(e)
            }
        )

    content = response.choices[0].message.content
    print("RAW:", content)

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