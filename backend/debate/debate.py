import random
import uuid

from langchain_core.messages import BaseMessage, AIMessage, HumanMessage

from character import Character


class Debate:
    def __init__(self, topic: str, pro: Character, con: Character, max_rounds: int):
        self.debate_id = str(uuid.uuid4())
        self.topic = topic

        self.pro = pro
        self.con = con
        self.speakers = (pro, con)

        self.start_speak_idx = 0
        self.current_speak_idx = 0
        self.max_speak_idx = max_rounds * 4  # 다들 각자 한번씩 말해야 하니깐

        self.chat_history: list[BaseMessage] = []

    def finished(self) -> bool:
        return self.current_speak_idx == self.max_speak_idx

    def pick_first_announce(self) -> tuple[bool, str, bool, str, int]:
        message = f"[{self.topic}] 주제에 대한 토론을 시작하겠습니다."
        self.chat_history.append(HumanMessage(content=message))

        pro_want_first, pro_reason = self.pro.want_first_announce(self.topic)
        con_want_first, con_reason = self.con.want_first_announce(self.topic)

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
        speaker = self.speakers[self._speaker_idx()]
        response = speaker.speak(self.topic, self.chat_history, self._remain_cnt())
        self.chat_history.append(AIMessage(content=response.message, name=speaker.name))

        current_speak_idx = self._speaker_idx()
        self.current_speak_idx += 1

        return current_speak_idx, response.emotion.value, response.message

    def _speaker_idx(self) -> int:
        return (self.start_speak_idx + self.current_speak_idx) % 2

    def _remain_cnt(self) -> int:
        return (self.max_speak_idx - self.current_speak_idx) // 2

    def close(self) -> str:
        return f"[{self.topic}] 주제에 대한 토론이 종료되었습니다."
