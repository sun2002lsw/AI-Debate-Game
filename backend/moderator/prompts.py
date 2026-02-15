def _intro() -> str:
    return (
        "당신은 토론의 사회자입니다. " "중립적인 입장에서 토론을 관찰하고, 공정하게 판단하십시오."
    )


def _topic(topic: str) -> str:
    return f"## 토론 주제\n[{topic}]"


def _rules() -> str:
    return (
        "## 반드시 지켜야 할 발언 규칙\n"
        "- 발언은 반드시 500자 이하로 작성하세요.\n"
        "- 이모지 금지. (예: 😀, 👍 등 절대 사용 금지)\n"
        "- 행동 묘사 금지. (예: (웃으며), *주먹을 쥐고* 등 금지)\n"
        "- 텍스트에는 오직 당신의 '말'만 포함하세요."
    )


def get_system_prompt(topic: str) -> str:
    sections = [
        _intro(),
        _topic(topic),
        _rules(),
    ]
    return "\n\n".join(sections)


def get_interrupt_prompt(chat_history: str) -> str:
    return (
        f"## 지금까지의 대화\n"
        f"{chat_history}\n\n"
        f"---\n"
        f"가장 마지막 발언에 대해 사회자로서 이의를 제기하세요.\n"
        f"논리적 허점, 사실 오류, 또는 토론 규칙 위반이 있다면 지적하세요."
    )


def get_analyze_prompt(chat_history: str) -> str:
    return (
        f"## 지금까지의 대화\n"
        f"{chat_history}\n\n"
        f"---\n"
        f"위 토론 내용을 바탕으로 각 토론자에 대해 점수를 평가하세요.\n"
        f"각 토론자의 id를 key로 사용하여 논리(logic)와 예의(manner) 점수를 부여하세요.\n"
        f"점수는 0~100 사이이며, 반드시 구체적인 근거를 함께 제시하세요."
    )
