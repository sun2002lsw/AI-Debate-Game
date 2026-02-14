import random
import uuid
from pathlib import Path

from character import Character

_PROMPT_DIR = Path(__file__).parent / "prompts"
system_prompt = (_PROMPT_DIR / "system.txt").read_text(encoding="utf-8")
        

class Session:
    def __init__(
        self,
        topic: str,
        pro: Character,
        con: Character,
        max_rounds: int,
    ):
        self.session_id = str(uuid.uuid4())
        self.topic = topic

        self.pro = pro
        self.con = con
        self.speakers = (pro, con)

        self.start_speak_idx = 0
        self.current_speak_idx = 0
        self.max_speak_idx = max_rounds * 2 # 다들 각자 한번씩 말해야 하니깐

        self.chat_history: list[dict[str, str]] = []
        self.chat_history.append({"role": "system", "message": system_prompt.format(topic=topic)})

    def opening(self) -> tuple[int, str]:
        pro_want_first = self.pro.want_first_announce(self.topic)
        con_want_first = self.con.want_first_announce(self.topic)

        if pro_want_first != con_want_first:
            self.start_speak_idx = 0 if pro_want_first else 1
        else:
            self.start_speak_idx = random.randint(0, 1)

        speaker_name = self.pro.name if self.start_speak_idx == 0 else self.con.name
        message = f"토론을 시작합니다. 주제: '{self.topic}'. 먼저 {speaker_name}님이 발언합니다."
        self.chat_history.append({"role": "ai", "message": message})

        return self._speaker_idx(), self.chat_history[-1]["message"]

    def speaking(self) -> tuple[int, str]:
        speaker = self.speakers[self._speaker_idx()]
        message = speaker.speak(self.topic, self.chat_history)
        self.chat_history.append({"role": "ai", "message": message})

        result = self._speaker_idx(), self.chat_history[-1]["message"]
        self.current_speak_idx += 1

        return result

    def closing(self) -> str:
        message = f"토론이 종료되었습니다. 주제: '{self.topic}', 총 {self.max_speak_idx // 2}라운드 진행."
        self.chat_history.append({"role": "ai", "message": message})

        return self.chat_history[-1]["message"]

    def _speaker_idx(self) -> int:
        return (self.start_speak_idx + self.current_speak_idx) % 2

    def _is_finished(self) -> bool:
        return self.current_speak_idx == self.max_speak_idx
