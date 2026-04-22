import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """
    너는 감정을 분석하는 심리 분석가 이다.

    문의한 내용을 아래의 제약조건에 맞춰서 반환을 해줘야 한다
    
    [제약 조건]
    - 감정을 긍정, 부정, 중립으로 반환해라
    - JSON 으로 반환해라

    [출력 형식]
    {
        "emotion": "긍정"
    }
"""

user_prompt = """
    나는 AI 서비스 개발자가 되었다!
"""

response = client.chat.completions.create(
    model="gpt-5.4-mini",
    temperature=0,  # 👈 중요 (일관성)
    messages=[
        {"role": "system", "content": system_prompt}, # 규칙 정의
        {"role": "user", "content": user_prompt} # 요청
    ]
)

content = response.choices[0].message.content

print("RAW:", content)

# 👉 실제 JSON 파싱 시도
parsed = None

try:
    parsed = json.loads(content)
except json.JSONDecodeError:
    print("JSON 파싱 에러")

print("PARSED:", parsed)