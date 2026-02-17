from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from common.schemas import Speak
from . import prompts, schemas


class Evaluator:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    async def evaluate(self, topic: str, chat_history: list[Speak]) -> dict[str, schemas.DebateEvaluation]:
        messages: list[BaseMessage] = []

        system_prompt = prompts.get_system_prompt(topic)
        messages.append(SystemMessage(content=system_prompt))

        formatted_chat_history = self._format_chat_history(chat_history)
        evaluate_prompt = prompts.get_evaluate_prompt(formatted_chat_history)
        messages.append(HumanMessage(content=evaluate_prompt))

        structured_llm = self.llm.with_structured_output(schemas.EvaluateResponse)
        response = await structured_llm.ainvoke(messages)

        result: schemas.EvaluateResponse = response  # type: ignore[assignment]
        return {id: scores.to_evaluation() for id, scores in result.debate_scores.items()}

    def _format_chat_history(self, chat_history: list[Speak]) -> str:
        lines: list[str] = []
        for chat in chat_history:
            if chat.speaker_id == "":
                speaker = "사회자"
            else:
                speaker = chat.speaker_id

            lines.append(f"{speaker}: {chat.message}")

        return "\n\n".join(lines)
