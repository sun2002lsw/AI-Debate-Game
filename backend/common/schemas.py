import re
from dataclasses import dataclass
from enum import Enum

EMOJI_PATTERN = re.compile(r"[\U00010000-\U0010FFFF]")


def strip_emoji(text: str) -> str:
    return EMOJI_PATTERN.sub("", text)


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


@dataclass
class Chat:
    id: str
    speaker_idx: int  # 0: 찬성측, 1: 반대측
    speaker_id: str  # 빈 문자열이면 사회자 발언
    emotion: str  # 빈 문자열이면 사회자 발언
    message: str
