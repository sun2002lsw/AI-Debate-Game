import asyncio
import random
import uuid
from typing import Callable

from common.schemas import Chat
from debater import Debater
from evaluator import Evaluator
from .schemas import FirstSpeakResult, DebateResult


class Debate:
    def __init__(
        self,
        topic: str,
        speak_cnt: int,
        first_speak_deciding_noti: Callable[[], None],
        first_speak_decided_noti: Callable[[], None],
        speak_ready_noti: Callable[[int], None],
        debate_result_evaluating_noti: Callable[[], None],
        debate_result_evaluated_noti: Callable[[], None],
        pro: Debater,
        con: Debater,
        evaluator: Evaluator,
    ):
        self.topic = topic
        self.max_speak_idx = speak_cnt * 2 - 1  # 다들 각자 한번씩 말해야 하니깐

        self.first_speak_deciding_noti = first_speak_deciding_noti
        self.first_speak_decided_noti = first_speak_decided_noti
        self.speak_ready_noti = speak_ready_noti
        self.debate_result_evaluating_noti = debate_result_evaluating_noti
        self.debate_result_evaluated_noti = debate_result_evaluated_noti

        self._first_speak_result: FirstSpeakResult | None = None
        self._last_speak: asyncio.Queue[Chat] = asyncio.Queue(maxsize=1)
        self._speak_consumed = asyncio.Event()
        self._debate_result: DebateResult | None = None

        self.pro = pro
        self.con = con
        self.evaluator = evaluator

        self.speakers = (pro, con)
        self.start_speak_idx = 0
        self.current_speak_idx = 0
        self.chat_history: list[Chat] = []

    def start(self):
        asyncio.create_task(self._run())

    async def _run(self):
        """선공 결정 → 발언 루프 → 채점 (블로킹)"""
        self.first_speak_deciding_noti()
        self._first_speak_result = await self._decide_first_speak()
        self.first_speak_decided_noti()

        while self.current_speak_idx <= self.max_speak_idx:
            speaker_idx, chat = await self._speak()
            await self._last_speak.put(chat)
            self.speak_ready_noti(speaker_idx)
            self.current_speak_idx += 1

            await self._speak_consumed.wait()
            self._speak_consumed.clear()

        self.debate_result_evaluating_noti()
        self._debate_result = await self._evaluate_debate_result()
        self.debate_result_evaluated_noti()

    async def _decide_first_speak(self) -> FirstSpeakResult:
        """누가 먼저 최초 발언을 할지 결정"""
        pro_want_first, pro_reason = await self.pro.want_first(self.topic, True)
        con_want_first, con_reason = await self.con.want_first(self.topic, False)

        if pro_want_first != con_want_first:
            self.start_speak_idx = 0 if pro_want_first else 1
        else:
            self.start_speak_idx = random.randint(0, 1)

        result = FirstSpeakResult(
            pro_want_first=pro_want_first,
            pro_reason=pro_reason,
            con_want_first=con_want_first,
            con_reason=con_reason,
            first_speaker_idx=self.start_speak_idx,
        )

        return result

    async def _speak(self) -> tuple[int, Chat]:
        """현재 순서 화자의 발언 생성"""
        speaker_idx = (self.start_speak_idx + self.current_speak_idx) % 2
        speaker = self.speakers[speaker_idx]
        is_pro = speaker_idx == 0

        # 발언 진행
        if len(self.chat_history) == 0:
            response = await speaker.first_speak(self.topic, is_pro)
        else:
            remain_cnt = (self.max_speak_idx - self.current_speak_idx) // 2 + 1  # 남은 횟수는 인덱스 + 1
            response = await speaker.next_speak(self.topic, is_pro, self.chat_history, remain_cnt)

        # 발언 저장
        id = str(uuid.uuid4())
        emotion = response.emotion.value
        message = response.message
        chat = Chat(id=id, speaker_idx=speaker_idx, speaker_id=speaker.id, emotion=emotion, message=message)
        self.chat_history.append(chat)

        return speaker_idx, chat

    async def _evaluate_debate_result(self) -> DebateResult:
        """토론 결과 점수 계산"""
        evaluations = await self.evaluator.evaluate(self.topic, self.chat_history)

        result = DebateResult(
            pro=evaluations[self.pro.id],
            con=evaluations[self.con.id],
        )

        return result

    def first_speak_result(self) -> FirstSpeakResult | None:
        return self._first_speak_result

    def listen(self) -> Chat | None:
        try:
            chat = self._last_speak.get_nowait()
            self._speak_consumed.set()
            return chat
        except asyncio.QueueEmpty:
            return None

    def debate_result(self) -> DebateResult | None:
        return self._debate_result
