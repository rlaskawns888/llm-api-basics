class EmptyInputException(Exception):
    def __init__(self, message: str = "질문은 비어 있을 수 없습니다."):
        self.message = message

class LLMTimeoutException(Exception):
    def __init__(self, message: str = "LLM 응답 시간이 초과되었습니다. 잠시 후 다시 시도해주세요."):
        self.message = message

class LLMServiceException(Exception):
    def __init__(self, message: str = "외부 AI 서비스 호출 중 오류가 발생했습니다."):
        self.message = message