from openai import OpenAI
from openai import APITimeoutError, APIConnectionError, APIError

from config.settings import OPENAI_API_KEY, OPENAI_MODEL, LLM_TIMEOUT
from exceptions.custom_exceptions import (
    EmptyInputException,
    LLMTimeoutException,
    LLMServiceException
)

class LLMService:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY X ")
        
        self.client = OpenAI(
            api_key=OPENAI_API_KEY
            , timeout=LLM_TIMEOUT
        )

    def ask(self, question: str) -> str:
        if question is None or not question.strip():
            raise EmptyInputException()
        
        try:
            response = self.client.responses.create(
                model=OPENAI_MODEL,
                input = [
                    {
                        "role": "system",
                        "content": "너는 사용자의 질문에 간결하고 이해하기 쉽게 답변하는 AI 도우미다."
                    },
                    {
                        "role": "user",
                        "content": question.strip()
                    }
                ]
            )

            answer = response.output_text

            if not answer or not answer.strip():
                raise LLMServiceException("LLM 응답이 비어 있습니다.")
            
            return answer.strip()
        
        except APITimeoutError:
            raise LLMTimeoutException()

        except APIConnectionError:
            raise LLMServiceException("AI 서비스 연결에 실패했습니다.")

        except APIError:
            raise LLMServiceException("AI 서비스 처리 중 오류가 발생했습니다.")

        except Exception:
            raise LLMServiceException("알 수 없는 외부 API 오류가 발생했습니다.") 

