import warnings

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from persona import Persona

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings",
    category=UserWarning,
    module="pydantic",
)
from .prompts import get_system_prompt, get_first_prompt, get_speak_prompt
from .schemas import FirstAnnounceDecision, SpeakResponse


class Character:
    def __init__(self, id: int, persona: Persona, llm: BaseChatModel):
        self.name = "-".join([persona.name, str(id)])
        self.persona = persona
        self.llm = llm

    def want_first_announce(self, topic: str) -> tuple[bool, str]:
        messages: list[BaseMessage] = []

        system_prompt = get_system_prompt(topic, self.persona)
        messages.append(SystemMessage(content=system_prompt))

        first_prompt = get_first_prompt()
        messages.append(HumanMessage(content=first_prompt))

        structured_llm = self.llm.with_structured_output(FirstAnnounceDecision)
        response = structured_llm.invoke(messages)

        result: FirstAnnounceDecision = response  # type: ignore[assignment]
        return result.want_first, result.reason

    def speak(self, topic: str, chat_history: list[BaseMessage], remain_cnt: int) -> SpeakResponse:
        messages: list[BaseMessage] = []

        system_prompt = get_system_prompt(topic, self.persona)
        messages.append(SystemMessage(content=system_prompt))

        formatted_chat_history = self._format_chat_history(chat_history)
        speak_prompt = get_speak_prompt(formatted_chat_history, remain_cnt)
        messages.append(HumanMessage(content=speak_prompt))

        structured_llm = self.llm.with_structured_output(SpeakResponse)
        response = structured_llm.invoke(messages)

        result: SpeakResponse = response  # type: ignore[assignment]
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
