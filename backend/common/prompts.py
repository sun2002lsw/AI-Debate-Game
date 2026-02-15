def topic(topic: str) -> str:
    return f"## 토론 주제\n[{topic}]"


def rules() -> str:
    return (
        "## 반드시 지켜야 할 발언 규칙\n"
        "- 발언은 반드시 500자 이하로 작성하세요.\n"
        "- 이모지 금지. (예: 😀, 👍 등 절대 사용 금지)\n"
        "- 행동 묘사 금지. (예: (웃으며), *주먹을 쥐고* 등 금지)\n"
        "- 텍스트에는 오직 당신의 '말'만 포함하세요."
    )


def chat_history_section(chat_history: str) -> str:
    return f"## 지금까지의 대화\n{chat_history}\n\n---\n"
