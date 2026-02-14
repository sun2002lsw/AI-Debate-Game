from pydantic import BaseModel, Field


class FirstAnnounceDecision(BaseModel):
    want_first: bool = Field(description="먼저 발언하고 싶으면 True, 아니면 False")
    reason: str = Field(description="해당 결정의 이유")
