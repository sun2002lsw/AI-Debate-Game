from common import prompts as common_prompts
from persona import Persona


def _intro() -> str:
    return "당신은 현재 토론에 참가한 참가자입니다. 토론에서 승리하기 위해 최선을 다하십시오."


def _stance(is_pro: bool) -> str:
    stance = "찬성" if is_pro else "반대"
    return f"## 당신의 토론 입장\n당신은 이 주제에 대해 **{stance}** 입장입니다. 반드시 이 입장을 일관되게 유지하세요."


def _persona(persona: Persona) -> str:
    return (
        f"## 당신의 정체성 (페르소나)\n"
        f"- 이름: {persona.name}\n"
        f"- 나이: {persona.age}\n"
        f"- 요약: {persona.summary}"
    )


def _strategy(persona: Persona) -> str:
    return f"## 토론 전략\n{persona.strategy}"


def get_system_prompt(topic: str, is_pro: bool, persona: Persona) -> str:
    sections = [
        _intro(),
        common_prompts.topic(topic),
        _stance(is_pro),
        _persona(persona),
        _strategy(persona),
        common_prompts.rules(),
    ]

    return "\n\n".join(sections)


def decide_first_prompt() -> str:
    return (
        f"토론을 시작하기 전 전략적 선택이 필요합니다.\n"
        f"먼저 발언하여 프레임을 주도할지, 나중에 발언하여 상대의 허점을 찌를지 결정하세요.\n"
        f"지금 바로 결정하여 당신의 선택과 그 이유를 말씀해 주세요."
    )


def get_first_speak_prompt() -> str:
    return (
        "토론의 첫 발언자로 선정되었습니다.\n"
        "첫 발언은 토론의 흐름을 결정합니다. "
        "강력한 첫마디로 주도권을 잡고, 상대방이 당신의 프레임 안에서 반응하게 만드세요."
    )


def get_next_speak_prompt(chat_history: str, remain: int) -> str:
    normal_speak = "상대방의 논리를 반박하거나 당신의 주장을 이어가세요."
    last_speak = "이것은 당신의 '최후 발언'입니다. 모든 논리를 쏟아부어 마무리하세요."

    return (
        f"{common_prompts.chat_history_section(chat_history)}"
        f"이제 당신이 발언할 차례입니다. 위 대화 맥락을 바탕으로 발언해 주세요.\n"
        f"남은 발언 횟수는 {remain}회입니다. 발언에 참고하세요.\n"
        f"{normal_speak if remain > 1 else last_speak}"
    )
