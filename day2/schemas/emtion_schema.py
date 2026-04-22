from pydantic import BaseModel, Field

class EmotionRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class EmotionResponse(BaseModel):
    emotion: str
    content: str