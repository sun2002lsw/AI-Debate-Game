import random
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable

from langchain_core.messages import BaseMessage, AIMessage

from debater import Debater
from debater.schemas import SpeakResponse
from moderator import Moderator, DebateScore
from .score_calculator import calculate


class Debate:
    def __init__(
        self,
        topic: str,
        speak_cnt: int,
        speak_ready_noti: Callable[[int], None],
        pro: Debater,
        con: Debater,
        moderator: Moderator,
    ):
        self.topic = topic
        self.max_speak_idx = speak_cnt * 2 - 1  # 다들 각자 한번씩 말해야 하니깐

        self.speak_ready_noti = speak_ready_noti
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._future: Future[tuple[int, SpeakResponse]] = Future()

        self.pro = pro
        self.con = con
        self.moderator = moderator

        self.speakers = (pro, con)
        self.start_speak_idx = 0
        self.current_speak_idx = 0
        self.chat_history: list[BaseMessage] = []

    def pick_first(self) -> tuple[bool, str, bool, str, int]:
        """누가 먼저 최초 발언을 할지 결정"""
        pro_want_first, pro_reason = self.pro.want_first(self.topic, True)
        con_want_first, con_reason = self.con.want_first(self.topic, False)

        if pro_want_first != con_want_first:
            self.start_speak_idx = 0 if pro_want_first else 1
        else:
            self.start_speak_idx = random.randint(0, 1)

        return (
            pro_want_first,
            pro_reason,
            con_want_first,
            con_reason,
            self.start_speak_idx,
        )

    def finished(self) -> bool:
        return self.current_speak_idx > self.max_speak_idx

    def prepare(self):
        """다음 발언을 백그라운드에서 준비 시작."""
        if self.finished():
            return

        speaker_idx = self._speaker_idx()
        self._future = self._executor.submit(self._generate, speaker_idx)

        def _notify(future: Future[tuple[int, SpeakResponse]]):
            if not future.exception():
                self.speak_ready_noti(speaker_idx)

        self._future.add_done_callback(_notify)

    def _generate(self, speaker_idx: int) -> tuple[int, SpeakResponse]:
        """실제 LLM 호출 (백그라운드 스레드에서 실행)"""
        speaker = self.speakers[speaker_idx]
        is_pro = speaker_idx == 0

        if len(self.chat_history) == 0:
            response = speaker.first_speak(self.topic, is_pro)
        else:
            response = speaker.next_speak(self.topic, is_pro, self.chat_history, self._remain_cnt())

        return speaker_idx, response

    def is_ready(self) -> bool:
        """발언이 준비됐는지 확인"""
        return self._future.done()

    def listen(self) -> tuple[int, str, str]:
        """준비된 발언 반환 (미완료 시 블로킹). 자동으로 다음 발언 준비 시작"""
        speaker_idx, response = self._future.result()
        self.chat_history.append(AIMessage(content=response.message, id=self.speakers[speaker_idx].id))
        self.current_speak_idx += 1

        # 다음 발언 미리 준비
        if not self.finished():
            self.prepare()

        return speaker_idx, response.emotion.value, response.message

    def speaking(self) -> tuple[int, str, str]:
        speaker_idx = self._speaker_idx()
        speaker = self.speakers[speaker_idx]
        is_pro = speaker_idx == 0

        if len(self.chat_history) == 0:
            response = speaker.first_speak(self.topic, is_pro)
        else:
            response = speaker.next_speak(self.topic, is_pro, self.chat_history, self._remain_cnt())
        self.chat_history.append(AIMessage(content=response.message, id=speaker.id))
        self.current_speak_idx += 1

        return speaker_idx, response.emotion.value, response.message

    def _speaker_idx(self) -> int:
        return (self.start_speak_idx + self.current_speak_idx) % 2

    def _remain_cnt(self) -> int:
        return (self.max_speak_idx - self.current_speak_idx) // 2 + 1  # 남은 횟수는 인덱스 + 1

    def moderator_interrupt(self, message: str) -> str:
        if len(message) == 0:
            message = self.moderator.interrupt(self.topic, self.chat_history)
        self.chat_history.append(AIMessage(content=message, id=""))
        return message

    def score_calculate(self) -> tuple[DebateScore, float, DebateScore, float]:
        scores = self.moderator.analyze(self.topic, self.chat_history)

        pro_scores = scores[self.pro.id]
        pro_result = calculate(pro_scores)
        con_scores = scores[self.con.id]
        con_result = calculate(con_scores)

        return pro_scores, pro_result, con_scores, con_result
