from pydantic import BaseModel, Field, field_validator

from common.schemas import Emotion, strip_emoji as _strip_emoji


class FirstSpeakDecision(BaseModel):
    want_first: bool = Field(description="먼저 발언하고 싶으면 True, 아니면 False")
    reason: str = Field(description="해당 결정의 이유")


class SpeakResponse(BaseModel):
    emotion: Emotion = Field(description="현재 감정 상태")
    message: str = Field(description="발언 내용")

    @field_validator("message")
    @classmethod
    def strip_emoji(cls, v: str) -> str:
        return _strip_emoji(v)
