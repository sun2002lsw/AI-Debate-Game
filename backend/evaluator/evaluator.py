from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from common.schemas import Chat
from . import prompts, schemas


class Evaluator:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    async def evaluate(self, topic: str, chat_history: list[Chat]) -> dict[str, schemas.DebateScore]:
        messages: list[BaseMessage] = []

        system_prompt = prompts.get_system_prompt(topic)
        messages.append(SystemMessage(content=system_prompt))

        formatted_chat_history = self._format_chat_history(chat_history)
        evaluate_prompt = prompts.get_evaluate_prompt(formatted_chat_history)
        messages.append(HumanMessage(content=evaluate_prompt))

        structured_llm = self.llm.with_structured_output(schemas.EvaluateResponse)
        response = await structured_llm.ainvoke(messages)

        result: schemas.EvaluateResponse = response  # type: ignore[assignment]
        return result.scores

    def _format_chat_history(self, chat_history: list[Chat]) -> str:
        lines: list[str] = []
        for chat in chat_history:
            if chat.speaker_id == "":
                speaker = "사회자"
            else:
                speaker = chat.speaker_id

            lines.append(f"{speaker}: {chat.message}")

        return "\n\n".join(lines)
