import warnings

from dotenv import load_dotenv

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings",
    category=UserWarning,
    module="pydantic",
)

from character import Character, Persona
from debate.session import Session
from llm.factory import create_llm


def main():
    topic = "인공지능이 인간의 일자리를 대체해야 하는가"

    llm = create_llm("gpt-4o")
    pro = Character(id=0, persona=Persona("yuna"), llm=llm)
    con = Character(id=1, persona=Persona("socrates"), llm=llm)

    session = Session(topic=topic, pro=pro, con=con, max_rounds=2)

    # 1) 선공 결정
    pro_want, pro_reason, con_want, con_reason, first_idx = (
        session.pick_first_announce()
    )

    print(f"[선공 결정]")
    print(f"찬성측: {'선공 희망' if pro_want else '후공 희망'} - {pro_reason}")
    print(f"반대측: {'선공 희망' if con_want else '후공 희망'} - {con_reason}")
    print(f"→ {speaker(first_idx)}이 먼저 발언합니다.")
    print()

    # 2) 토론 진행
    while not session.finished():
        speaker_idx, message = session.speaking()
        print(f"{speaker(speaker_idx)}: {message}")

    # 3) 종료
    print(session.close())


def speaker(idx: int) -> str:
    return "반대측" if idx else "찬성측"


if __name__ == "__main__":
    load_dotenv()
    main()
