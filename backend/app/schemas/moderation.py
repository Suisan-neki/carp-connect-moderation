from pydantic import BaseModel
from typing import List


class ModerationCheck(BaseModel):
    content: str
    content_type: str


class ModerationData(BaseModel):
    moderation_id: str
    content: str
    result: str
    reason: str
    score: float
    created_at: int


class ModerationResult(BaseModel):
    status: str
    data: ModerationData


class ModerationHistory(ModerationData):
    pass


class ModerationHistoryResponse(BaseModel):
    status: str
    data: List[ModerationHistory]


class ModerationStats(BaseModel):
    total_count: int
    approved_count: int
    rejected_count: int
    approval_rate: float


class ModerationStatsResponse(BaseModel):
    status: str
    data: ModerationStats