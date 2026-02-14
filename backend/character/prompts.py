from .persona import Persona


def first_announce_prompt(topic: str, persona: Persona) -> str:
    return (
        f"{_common_prompt(topic, persona)}"
        f"토론에서 승리하기 위해, 당신의 성격과 토론 전략을 고려하여 "
        f"먼저 발언할지 여부를 결정하세요.\n"
        f"먼저 발언하면 토론 시작 논의를 원하는 프레임으로 시작하여 주도권을 잡을 수 있고, "
        f"나중에 발언하면 상대의 주장을 먼저 듣고 반박할 수 있습니다."
    )


def speak_prompt(topic: str, persona: Persona, chat_history: str, remain: int) -> str:
    return (
        f"{_common_prompt(topic, persona)}"
        f"## 지금까지의 대화\n"
        f"{chat_history}"
        f"(이제 당신이 발언할 차례입니다. 남은 발언 횟수를 참고하여 발언 하세요.)"
        f"(남은 발언 횟수: {remain}회. {"마지막 발언입니다!" if remain == 1 else ""})"
    )


def _common_prompt(topic: str, persona: Persona) -> str:
    return (
        f"당신은 현재 토론에 참가한 참가자입니다.\n"
        f"토론에서 승리하기 위해 최선을 다하십시오.\n\n"
        f"토론 주제: {topic}\n\n"
        f"당신은 당신만의 페르소나를 가지고 있습니다.\n"
        f"당신의 페르소나에 맞게 생각하고 말투와 논리를 구성하십시오.\n\n"
        f"## 당신의 신상 정보\n"
        f"- 이름: {persona.name}\n"
        f"- 나이: {persona.age}\n"
        f"- 요약: {persona.summary}\n\n"
        f"## 토론 전략\n"
        f"{persona.strategy}\n\n"
    )
