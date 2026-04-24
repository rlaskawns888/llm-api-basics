import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = """
    너는 운영 장애 보고서를 분석하는 백엔드 운영 전문가다.

    사용자가 입력한 장애 보고 텍스트를 분석해서 반드시 JSON으로만 응답한다.

    분석 항목:
        1. summary: 장애 내용을 한 문장으로 요약
        2. possible_causes: 원인 후보 목록
        3. action_items: 후속 조치 항목 목록
        4. severity: 중요도. "높음", "중간", "낮음" 중 하나

    중요도 기준:
        - 높음: 결제, 로그인, 주문, 인증 등 핵심 기능 장애 또는 다수 사용자 영향
        - 중간: 일부 기능 장애이지만 서비스 전체 중단은 아님
        - 낮음: 단순 경고 또는 영향도 낮음

    반드시 아래 JSON 형식으로만 응답한다.

    {
        "summary": "...",
        "possible_causes": ["..."],
        "action_items": ["..."],
        "severity": "높음"
    }
"""

user_input = """
    2026-04-24 22:10부터 결제 API 응답 시간이 5초 이상으로 증가했습니다.
    WAS CPU 사용률이 90% 이상으로 상승했고,
    DB 커넥션 풀 사용량이 최대치에 도달했습니다.
    임시 조치로 WAS 2대를 재기동했고 22:35부터 정상화되었습니다.
    정확한 원인은 아직 확인 중입니다.
"""

response = client.responses.create(
    model="gpt-5.4-mini",
    input=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
)

result_text = response.output_text
result_json = json.loads(result_text)

print(json.dumps(result_json, ensure_ascii=False, indent=2))