import re
from dataclasses import dataclass

EMOJI_PATTERN = re.compile(r"[\U00010000-\U0010FFFF]")


def strip_emoji(text: str) -> str:
    return EMOJI_PATTERN.sub("", text)


@dataclass
class Chat:
    speaker_id: str  # 빈 문자열이면 사회자 발언
    message: str
