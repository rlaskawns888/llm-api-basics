from pydantic import BaseModel, Field

class CategoryRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class CategoryResponse(BaseModel):
    category: str
    content: str