import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """
너는 백엔드 서비스의 AI 엔진이다.

규칙:
- 반드시 JSON으로만 응답해라
- 다른 설명 절대 금지
- key 이름은 정확히 지켜라
"""

user_prompt = """
에러: ERROR 500: DB Connection Timeout

아래 JSON 형식으로 반환해라.

{
  "root_cause": "",
  "solution": ""
}
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
try:
    parsed = json.loads(content)
except:
    print("JSON 파싱 에러")

print("PARSED:", parsed)