import warnings

from dotenv import load_dotenv

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings",
    category=UserWarning,
    module="pydantic",
)

from character import Character
from persona import Persona
from debate import Debate
from llm.factory import create_llm


def main():
    topic = "인공지능이 인간의 일자리를 대체해야 하는가"

    llm = create_llm("gemini-2.5-pro")
    pro = Character(id=0, persona=Persona("crybaby"), llm=llm)
    con = Character(id=1, persona=Persona("thug"), llm=llm)

    debate = Debate(topic=topic, pro=pro, con=con, max_rounds=2)

    # 1) 선공 결정
    pro_want_first, pro_reason, con_want_first, con_reason, first_idx = debate.pick_first_announce()

    print(f"[선공 결정]")
    print(f"찬성측: {'선공 희망' if pro_want_first else '후공 희망'} - {pro_reason}")
    print(f"반대측: {'선공 희망' if con_want_first else '후공 희망'} - {con_reason}")
    print(f"→ {speaker(first_idx)}이 먼저 발언합니다.")
    print()

    # 2) 토론 진행
    while not debate.finished():
        speaker_idx, emotion, message = debate.speaking()
        print(f"{speaker(speaker_idx)}: ({emotion}) {message}")

    # 3) 종료
    print(debate.close())


def speaker(idx: int) -> str:
    return "반대측" if idx else "찬성측"


if __name__ == "__main__":
    load_dotenv()
    main()
