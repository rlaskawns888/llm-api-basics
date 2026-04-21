import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-5.4-mini",
    messages=[
        {"role":"user", "content":"FastAPI가 뭐야? (50자 이내로 대답해줘)"}
    ]
)

print(response)
print(response.choices[0].message.content)