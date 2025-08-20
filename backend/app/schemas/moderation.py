from pydantic import BaseModel
from typing import Optional

class ModerationCheck(BaseModel):
    content: str
    content_type: str

class ModerationResult(BaseModel):
    moderation_id: str
    content: str
    result: str
    reason: str
    score: float
    created_at: int

class ModerationHistory(BaseModel):
    moderation_id: str
    content_id: str
    content_type: str
    original_content: str
    moderation_result: str
    moderation_reason: str
    moderation_score: float
    created_at: int 