import random
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable

from langchain_core.messages import BaseMessage, AIMessage

from debater import Debater
from debater.schemas import SpeakResponse
from moderator import Moderator
from .schemas import FirstPickResult, DebateResult
from .score_calculator import calculate


class Debate:
    def __init__(
        self,
        topic: str,
        speak_cnt: int,
        first_picked_noti: Callable[[], None],
        speak_ready_noti: Callable[[int], None],
        score_calculated_noti: Callable[[], None],
        pro: Debater,
        con: Debater,
        moderator: Moderator,
    ):
        self.topic = topic
        self.max_speak_idx = speak_cnt * 2 - 1  # 다들 각자 한번씩 말해야 하니깐

        self.first_picked_noti = first_picked_noti
        self.speak_ready_noti = speak_ready_noti
        self.score_calculated_noti = score_calculated_noti
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._future: Future[tuple[int, SpeakResponse]] = Future()

        self._first_pick_result: FirstPickResult | None = None
        self._debate_result: DebateResult | None = None

        self.pro = pro
        self.con = con
        self.moderator = moderator

        self.speakers = (pro, con)
        self.start_speak_idx = 0
        self.current_speak_idx = 0
        self.chat_history: list[BaseMessage] = []

        self._start_pick_first()

    def _start_pick_first(self) -> None:
        """선공 결정을 백그라운드에서 시작"""
        future = self._executor.submit(self._pick_first)

        def _notify(future: Future[FirstPickResult]) -> None:
            self._first_pick_result = future.result()
            self.first_picked_noti()

        future.add_done_callback(_notify)

    def _pick_first(self) -> FirstPickResult:
        """누가 먼저 최초 발언을 할지 결정"""
        pro_want_first, pro_reason = self.pro.want_first(self.topic, True)
        con_want_first, con_reason = self.con.want_first(self.topic, False)

        if pro_want_first != con_want_first:
            self.start_speak_idx = 0 if pro_want_first else 1
        else:
            self.start_speak_idx = random.randint(0, 1)

        # 다음 발언 미리 준비
        self._prepare()

        result = FirstPickResult(
            pro_want_first=pro_want_first,
            pro_reason=pro_reason,
            con_want_first=con_want_first,
            con_reason=con_reason,
            first_idx=self.start_speak_idx,
        )

        return result

    def first_pick_result(self) -> FirstPickResult | None:
        return self._first_pick_result

    def debate_result(self) -> DebateResult | None:
        return self._debate_result

    def finished(self) -> bool:
        return self.current_speak_idx > self.max_speak_idx

    def listen(self) -> tuple[int, str, str]:
        """준비된 발언 반환 (미완료 시 블로킹). 자동으로 다음 발언 준비 시작"""
        speaker_idx, response = self._future.result()
        self.chat_history.append(AIMessage(content=response.message, id=self.speakers[speaker_idx].id))
        self.current_speak_idx += 1

        # 다음 발언 미리 준비
        self._prepare()
        self._start_scoring()

        return speaker_idx, response.emotion.value, response.message

    def _prepare(self):
        """다음 발언을 백그라운드에서 준비 시작"""
        if self.finished():
            return

        speaker_idx = (self.start_speak_idx + self.current_speak_idx) % 2
        self._future = self._executor.submit(self._generate, speaker_idx)

        def _notify(_: Future[tuple[int, SpeakResponse]]):
            self.speak_ready_noti(speaker_idx)

        self._future.add_done_callback(_notify)

    def _start_scoring(self):
        """채점을 백그라운드에서 시작. 토론이 끝나지 않았으면 무시"""
        if not self.finished():
            return

        future = self._executor.submit(self._score_calculate)

        def _notify(future: Future[DebateResult]):
            self._debate_result = future.result()
            self.score_calculated_noti()

        future.add_done_callback(_notify)

    def _generate(self, speaker_idx: int) -> tuple[int, SpeakResponse]:
        """실제 LLM 호출 (백그라운드 스레드에서 실행)"""
        speaker = self.speakers[speaker_idx]
        is_pro = speaker_idx == 0

        if len(self.chat_history) == 0:
            response = speaker.first_speak(self.topic, is_pro)
        else:
            remain_cnt = (self.max_speak_idx - self.current_speak_idx) // 2 + 1  # 남은 횟수는 인덱스 + 1
            response = speaker.next_speak(self.topic, is_pro, self.chat_history, remain_cnt)

        return speaker_idx, response

    def moderator_interrupt(self, message: str) -> str:
        if len(message) == 0:
            message = self.moderator.interrupt(self.topic, self.chat_history)
        self.chat_history.append(AIMessage(content=message, id=""))
        return message

    def _score_calculate(self) -> DebateResult:
        scores = self.moderator.analyze(self.topic, self.chat_history)

        result = DebateResult(
            pro_scores=scores[self.pro.id],
            pro_result=calculate(scores[self.pro.id]),
            con_scores=scores[self.con.id],
            con_result=calculate(scores[self.con.id]),
        )

        return result
