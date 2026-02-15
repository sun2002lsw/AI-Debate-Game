import re

EMOJI_PATTERN = re.compile(r"[\U00010000-\U0010FFFF]")


def strip_emoji(text: str) -> str:
    return EMOJI_PATTERN.sub("", text)
