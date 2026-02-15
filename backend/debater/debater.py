import warnings

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from persona import Persona
from . import prompts, schemas

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings",
    category=UserWarning,
    module="pydantic",
)


class Debater:
    def __init__(self, id: str, persona: Persona, llm: BaseChatModel):
        self.id = id
        self.persona = persona
        self.llm = llm

    def want_first(self, topic: str, is_pro: bool) -> tuple[bool, str]:
        messages: list[BaseMessage] = []

        system_prompt = prompts.get_system_prompt(topic, is_pro, self.persona)
        messages.append(SystemMessage(content=system_prompt))

        first_prompt = prompts.decide_first_prompt()
        messages.append(HumanMessage(content=first_prompt))

        structured_llm = self.llm.with_structured_output(schemas.FirstSpeakDecision)
        response = structured_llm.invoke(messages)

        result: schemas.FirstSpeakDecision = response  # type: ignore[assignment]
        return result.want_first, result.reason

    def first_speak(self, topic: str, is_pro: bool) -> schemas.SpeakResponse:
        messages: list[BaseMessage] = []

        system_prompt = prompts.get_system_prompt(topic, is_pro, self.persona)
        messages.append(SystemMessage(content=system_prompt))

        first_speak_prompt = prompts.get_first_speak_prompt()
        messages.append(HumanMessage(content=first_speak_prompt))

        structured_llm = self.llm.with_structured_output(schemas.SpeakResponse)
        response = structured_llm.invoke(messages)

        result: schemas.SpeakResponse = response  # type: ignore[assignment]
        return result

    def next_speak(
        self, topic: str, is_pro: bool, chat_history: list[BaseMessage], remain_cnt: int
    ) -> schemas.SpeakResponse:
        messages: list[BaseMessage] = []

        system_prompt = prompts.get_system_prompt(topic, is_pro, self.persona)
        messages.append(SystemMessage(content=system_prompt))

        formatted_chat_history = self._format_chat_history(chat_history)
        next_speak_prompt = prompts.get_next_speak_prompt(formatted_chat_history, remain_cnt)
        messages.append(HumanMessage(content=next_speak_prompt))

        structured_llm = self.llm.with_structured_output(schemas.SpeakResponse)
        response = structured_llm.invoke(messages)

        result: schemas.SpeakResponse = response  # type: ignore[assignment]
        return result

    def _format_chat_history(self, chat_history: list[BaseMessage]) -> str:
        lines: list[str] = []
        for chat in chat_history:
            speaker = "알 수 없음"
            if not chat.id or chat.id == "":
                speaker = "사회자"
            elif chat.id == self.id:
                speaker = "당신"
            else:
                speaker = "상대방"

            message = chat.content  # type: ignore[assignment]
            lines.append(f"{speaker}: {message}")

        return "\n\n".join(lines)
