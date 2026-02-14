from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, SystemMessage

from persona import Persona
from .prompts import first_announce_prompt, speak_prompt
from .schemas import FirstAnnounceDecision


class Character:
    def __init__(self, id: int, persona: Persona, llm: BaseChatModel):
        self.name = "-".join([persona.name, str(id)])
        self.persona = persona
        self.llm = llm

    def want_first_announce(self, topic: str) -> tuple[bool, str]:
        structured_llm = self.llm.with_structured_output(FirstAnnounceDecision)

        prompt = first_announce_prompt(topic, self.persona)
        messages = [SystemMessage(content=prompt)]

        response = structured_llm.invoke(messages)
        result: FirstAnnounceDecision = response  # type: ignore[assignment]
        return result.want_first, result.reason

    def speak(self, topic: str, chat_history: list[BaseMessage], remain: int) -> str:
        formatted_chat_history = self._format_chat_history(chat_history)

        prompt = speak_prompt(topic, self.persona, formatted_chat_history, remain)
        messages = [SystemMessage(content=prompt)]

        response = self.llm.invoke(messages)
        result: str = response.content  # type: ignore[assignment]
        return result

    def _format_chat_history(self, chat_history: list[BaseMessage]) -> str:
        lines: list[str] = []
        for chat in chat_history:
            speaker = "알 수 없음"
            if not chat.name or chat.name == "":
                speaker = "사회자"
            elif chat.name == self.name:
                speaker = "당신"
            else:
                speaker = "상대방"

            message = chat.content  # type: ignore[assignment]
            lines.append(f"{speaker}: {message}")

        return "\n\n".join(lines)
