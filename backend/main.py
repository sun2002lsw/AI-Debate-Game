import warnings

from dotenv import load_dotenv

from character import Character
from persona import Persona
from debate import Debate
from llm.factory import create_llm


warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings",
    category=UserWarning,
    module="pydantic",
)

COLORS = ["\033[94m", "\033[91m", "\033[93m"]  # 찬성=파랑, 반대=빨강, 사회=노랑
RESET = "\033[0m"


def main():
    topic = "스타2에서 프로토스의 점멸추적자 빌드를 테란이 막을 때, 본진 벙커 없이 막아야 한다"

    llm = create_llm("gemini-2.5-pro")
    pro = Character(id=0, persona=Persona("philosopher"), llm=llm)
    con = Character(id=1, persona=Persona("crybaby"), llm=llm)

    debate = Debate(topic=topic, pro=pro, con=con, max_rounds=2)

    # 1) 선공 결정
    pro_want_first, pro_reason, con_want_first, con_reason, first_idx = debate.pick_first_announce()
    pro_choice = "선공 희망" if pro_want_first else "후공 희망"
    con_choice = "선공 희망" if con_want_first else "후공 희망"

    print(f"{COLORS[0]}찬성측: {pro_choice} - {pro_reason}{RESET}")
    print(f"{COLORS[1]}반대측: {con_choice} - {con_reason}{RESET}")
    print(f"{COLORS[2]}→ {"반대측" if first_idx else "찬성측"}이 먼저 발언합니다.{RESET}")
    print()

    # 2) 토론 진행
    while not debate.finished():
        speaker_idx, emotion, message = debate.speaking()
        speaker = "반대측" if speaker_idx else "찬성측"
        print(f"{COLORS[speaker_idx]}{speaker}: ({emotion}) {message}{RESET}")

    # 3) 종료
    print(f"{COLORS[2]}{debate.close()}{RESET}")


if __name__ == "__main__":
    load_dotenv()
    main()
