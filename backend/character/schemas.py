import re
from enum import Enum

from pydantic import BaseModel, Field, field_validator

_EMOJI_PATTERN = re.compile(r"[\U00010000-\U0010FFFF]")


class Emotion(str, Enum):
    CALM = "평온"
    ANGRY = "분노"
    SCORNFUL = "조소"
    CONFIDENT = "자신감"
    SAD = "슬픔"
    FLUSTERED = "당황"
    PASSIONATE = "열정"
    CONTEMPTUOUS = "경멸"
    JOYFUL = "즐거움"
    NERVOUS = "긴장"


class FirstSpeakDecision(BaseModel):
    want_first: bool = Field(description="먼저 발언하고 싶으면 True, 아니면 False")
    reason: str = Field(description="해당 결정의 이유")


class SpeakResponse(BaseModel):
    emotion: Emotion = Field(description="현재 감정 상태")
    message: str = Field(description="발언 내용")

    @field_validator("message")
    @classmethod
    def strip_emoji(cls, v: str) -> str:
        return _EMOJI_PATTERN.sub("", v)
