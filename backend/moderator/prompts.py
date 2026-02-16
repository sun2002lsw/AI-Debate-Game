from common import prompts as common_prompts


def _intro() -> str:
    return (
        "당신은 토론의 사회자입니다. " "중립적인 입장에서 토론을 관찰하고, 공정하게 판단하십시오."
    )


def get_system_prompt(topic: str) -> str:
    sections = [
        _intro(),
        common_prompts.topic(topic),
        common_prompts.rules(),
    ]

    return "\n\n".join(sections)


def get_interrupt_prompt(chat_history: str) -> str:
    return (
        f"{common_prompts.chat_history_section(chat_history)}"
        f"가장 마지막 발언에 대해 사회자로서 이의를 제기하세요.\n"
        f"논리적 허점, 사실 오류, 또는 토론 규칙 위반이 있다면 지적하세요."
    )


def get_analyze_prompt(chat_history: str) -> str:
    return (
        f"{common_prompts.chat_history_section(chat_history)}"
        f"위 토론 내용을 바탕으로 각 토론자에 대해 점수를 평가하세요.\n"
        f"각 토론자의 id를 key로 사용하여 논리(logic)와 예의(manner) 점수를 부여하세요.\n"
        f"점수는 0~100 사이이며, 반드시 구체적인 근거를 함께 제시하세요."
    )
