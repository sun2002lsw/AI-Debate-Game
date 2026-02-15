import warnings

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from . import prompts, schemas

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings",
    category=UserWarning,
    module="pydantic",
)


class Moderator:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def interrupt(self, topic: str, chat_history: list[BaseMessage]) -> str:
        messages: list[BaseMessage] = []

        system_prompt = prompts.get_system_prompt(topic)
        messages.append(SystemMessage(content=system_prompt))

        formatted_chat_history = self._format_chat_history(chat_history)
        interrupt_prompt = prompts.get_interrupt_prompt(formatted_chat_history)
        messages.append(HumanMessage(content=interrupt_prompt))

        structured_llm = self.llm.with_structured_output(schemas.InterruptResponse)
        response = structured_llm.invoke(messages)

        result: schemas.InterruptResponse = response  # type: ignore[assignment]
        return result.message

    def analyze(
        self, topic: str, chat_history: list[BaseMessage]
    ) -> dict[str, schemas.DebateScore]:
        messages: list[BaseMessage] = []

        system_prompt = prompts.get_system_prompt(topic)
        messages.append(SystemMessage(content=system_prompt))

        formatted_chat_history = self._format_chat_history(chat_history)
        analyze_prompt = prompts.get_analyze_prompt(formatted_chat_history)
        messages.append(HumanMessage(content=analyze_prompt))

        structured_llm = self.llm.with_structured_output(schemas.AnalyzeResponse)
        response = structured_llm.invoke(messages)

        result: schemas.AnalyzeResponse = response  # type: ignore[assignment]
        return result.scores

    def _format_chat_history(self, chat_history: list[BaseMessage]) -> str:
        lines: list[str] = []
        for chat in chat_history:
            if not chat.id or chat.id == "":
                speaker = "사회자"
            else:
                speaker = chat.id

            message = chat.content  # type: ignore[assignment]
            lines.append(f"{speaker}: {message}")

        return "\n\n".join(lines)
