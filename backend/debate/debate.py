import random
import threading
import uuid
from typing import Callable

from common.schemas import Chat
from debater import Debater
from debater.schemas import SpeakResponse
from moderator import Moderator
from .schemas import FirstSpeakResult, DebateResult
from .score_calculator import calculate


class Debate:
    def __init__(
        self,
        topic: str,
        speak_cnt: int,
        first_speak_decided_noti: Callable[[], None],
        speak_ready_noti: Callable[[int], None],
        score_calculated_noti: Callable[[], None],
        pro: Debater,
        con: Debater,
        moderator: Moderator,
    ):
        self.topic = topic
        self.max_speak_idx = speak_cnt * 2 - 1  # 다들 각자 한번씩 말해야 하니깐

        self.first_speak_decided_noti = first_speak_decided_noti
        self.speak_ready_noti = speak_ready_noti
        self.score_calculated_noti = score_calculated_noti
        self._first_speak_result: FirstSpeakResult | None = None
        self._debate_result: DebateResult | None = None
        self._prepared_event = threading.Event()
        self._listened_event = threading.Event()

        self.pro = pro
        self.con = con
        self.moderator = moderator

        self.speakers = (pro, con)
        self.start_speak_idx = 0
        self.current_speak_idx = 0
        self.chat_history: list[Chat] = []

    def start(self):
        """선공 결정 → 발언 루프 → 채점 (블로킹)"""
        self._first_speak_result = self._decide_first_speak()
        self.first_speak_decided_noti()

        while not self.finished():
            speaker_idx, response = self._generate()
            id = str(uuid.uuid4())
            chat = Chat(
                id=id,
                speaker_id=self.speakers[speaker_idx].id,
                emotion=response.emotion.value,
                message=response.message,
            )
            self.chat_history.append(chat)
            self.current_speak_idx += 1
            self.speak_ready_noti(speaker_idx)
            self._prepared_event.set()
            self._listened_event.wait()
            self._listened_event.clear()

        self._debate_result = self._score_calculate()
        self.score_calculated_noti()

    def _decide_first_speak(self) -> FirstSpeakResult:
        """누가 먼저 최초 발언을 할지 결정"""
        pro_want_first, pro_reason = self.pro.want_first(self.topic, True)
        con_want_first, con_reason = self.con.want_first(self.topic, False)

        if pro_want_first != con_want_first:
            self.start_speak_idx = 0 if pro_want_first else 1
        else:
            self.start_speak_idx = random.randint(0, 1)

        result = FirstSpeakResult(
            pro_want_first=pro_want_first,
            pro_reason=pro_reason,
            con_want_first=con_want_first,
            con_reason=con_reason,
            first_idx=self.start_speak_idx,
        )

        return result

    def first_speak_result(self) -> FirstSpeakResult | None:
        return self._first_speak_result

    def debate_result(self) -> DebateResult | None:
        return self._debate_result

    def finished(self) -> bool:
        return self.current_speak_idx > self.max_speak_idx

    def listen(self) -> tuple[int, str, str]:
        """준비된 발언 반환 (미완료 시 블로킹)"""
        self._prepared_event.wait()
        self._prepared_event.clear()

        chat = self.chat_history[-1]
        speaker_idx = 0 if chat.speaker_id == self.pro.id else 1

        self._listened_event.set()

        return speaker_idx, chat.emotion, chat.message

    def _generate(self) -> tuple[int, SpeakResponse]:
        """현재 순서 화자의 발언 생성"""
        speaker_idx = (self.start_speak_idx + self.current_speak_idx) % 2
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

        id = str(uuid.uuid4())
        self.chat_history.append(Chat(id=id, speaker_id="", emotion="", message=message))

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
