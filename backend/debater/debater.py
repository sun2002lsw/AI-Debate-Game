from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from common.schemas import Speak
from persona import Persona
from . import prompts, schemas


class Debater:
    def __init__(self, id: str, persona: Persona, llm: BaseChatModel):
        self.id = id
        self.persona = persona
        self.llm = llm

    async def want_first(self, topic: str, is_pro: bool) -> tuple[bool, str]:
        messages: list[BaseMessage] = []

        system_prompt = prompts.get_system_prompt(topic, is_pro, self.persona)
        messages.append(SystemMessage(content=system_prompt))

        first_prompt = prompts.decide_first_prompt()
        messages.append(HumanMessage(content=first_prompt))

        structured_llm = self.llm.with_structured_output(schemas.FirstSpeakDecision)
        response = await structured_llm.ainvoke(messages)

        result: schemas.FirstSpeakDecision = response  # type: ignore[assignment]
        return result.want_first, result.reason

    async def first_speak(self, topic: str, is_pro: bool) -> schemas.SpeakResponse:
        messages: list[BaseMessage] = []

        system_prompt = prompts.get_system_prompt(topic, is_pro, self.persona)
        messages.append(SystemMessage(content=system_prompt))

        first_speak_prompt = prompts.get_first_speak_prompt()
        messages.append(HumanMessage(content=first_speak_prompt))

        structured_llm = self.llm.with_structured_output(schemas.SpeakResponse)
        response = await structured_llm.ainvoke(messages)

        result: schemas.SpeakResponse = response  # type: ignore[assignment]
        return result

    async def next_speak(
        self, topic: str, is_pro: bool, chat_history: list[Speak], remain_cnt: int
    ) -> schemas.SpeakResponse:
        messages: list[BaseMessage] = []

        system_prompt = prompts.get_system_prompt(topic, is_pro, self.persona)
        messages.append(SystemMessage(content=system_prompt))

        formatted_chat_history = self._format_chat_history(chat_history)
        next_speak_prompt = prompts.get_next_speak_prompt(formatted_chat_history, remain_cnt)
        messages.append(HumanMessage(content=next_speak_prompt))

        structured_llm = self.llm.with_structured_output(schemas.SpeakResponse)
        response = await structured_llm.ainvoke(messages)

        result: schemas.SpeakResponse = response  # type: ignore[assignment]
        return result

    def _format_chat_history(self, chat_history: list[Speak]) -> str:
        lines: list[str] = []
        for chat in chat_history:
            if chat.speaker_id == "":
                speaker = "사회자"
            elif chat.speaker_id == self.id:
                speaker = "당신"
            else:
                speaker = "상대방"

            lines.append(f"{speaker}: {chat.message}")

        return "\n\n".join(lines)
