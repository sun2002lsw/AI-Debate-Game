from dotenv import load_dotenv

from common.warnings import configure as configure_warnings
from debater import create_debater
from persona import list_personas
from llm import list_models
from debate import Debate


COLORS = ["\033[94m", "\033[91m", "\033[93m"]  # 찬성=파랑, 반대=빨강, 사회=노랑
RESET = "\033[0m"


def main():
    topic = input("토론 주제: ")
    speak_cnt = int(input("발언 횟수: "))

    print("\n===== 페르소나 목록 =====")
    personas = list_personas()
    for i, p in enumerate(personas):
        print(f"  {i}: {p.name}({p.age}세) - {p.summary}")
    print("\n===== LLM 모델 목록 =====")
    models = list_models()
    for i, m in enumerate(models):
        print(f"  {i}: {m}")
    print()

    pro_perso = int(input("찬성측 인격 선택: "))
    pro_model = int(input("찬성측 모델 선택: "))
    con_perso = int(input("반대측 인격 선택: "))
    con_model = int(input("반대측 모델 선택: "))
    print()

    # 토론 참가자 생성
    pro = create_debater(persona=pro_perso, model=pro_model)
    con = create_debater(persona=con_perso, model=con_model)

    debate = Debate(topic=topic, speak_cnt=speak_cnt, pro=pro, con=con)

    # 1) 선공 결정
    pro_want_first, pro_reason, con_want_first, con_reason, first_idx = debate.pick_first()
    pro_choice = "선공 희망" if pro_want_first else "후공 희망"
    con_choice = "선공 희망" if con_want_first else "후공 희망"

    print(f"{COLORS[2]}먼저 발언할 토론자를 선택합니다.{RESET}")
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
    print(f"\n{COLORS[2]}{debate.close()}{RESET}")


if __name__ == "__main__":
    load_dotenv()
    configure_warnings()
    main()
