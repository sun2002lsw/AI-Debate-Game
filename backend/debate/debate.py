import random

from langchain_core.messages import BaseMessage, AIMessage

from debater import Debater


class Debate:
    def __init__(self, topic: str, speak_cnt: int, pro: Debater, con: Debater):
        self.topic = topic
        self.max_speak_idx = speak_cnt * 2 - 1  # 다들 각자 한번씩 말해야 하니깐

        self.pro = pro
        self.con = con
        self.speakers = (pro, con)

        self.start_speak_idx = 0
        self.current_speak_idx = 0

        self.chat_history: list[BaseMessage] = []

    def finished(self) -> bool:
        return self.current_speak_idx > self.max_speak_idx

    def pick_first(self) -> tuple[bool, str, bool, str, int]:
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

    def close(self) -> str:
        return f"[{self.topic}] 주제에 대한 토론이 종료되었습니다."
