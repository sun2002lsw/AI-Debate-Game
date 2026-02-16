import threading

from dotenv import load_dotenv

from common.warnings import configure as configure_warnings
from debater import create_debater
from persona import list_personas
from llm import list_models, create_llm
from debate import Debate, FirstPickResult, DebateResult
from moderator import Moderator


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
    mod_model = int(input("사회자 모델 선택: "))
    print()

    # 토론 참가자 생성
    pro = create_debater(persona=pro_perso, model=pro_model)
    con = create_debater(persona=con_perso, model=con_model)
    moderator = Moderator(llm=create_llm(mod_model))

    first_pick_done = threading.Event()

    def first_picked_noti(result: FirstPickResult) -> None:
        pro_choice = "선공 희망" if result.pro_want_first else "후공 희망"
        con_choice = "선공 희망" if result.con_want_first else "후공 희망"

        print(f"{COLORS[2]}먼저 발언할 토론자를 선택합니다.{RESET}")
        print(f"{COLORS[0]}찬성측: {pro_choice} - {result.pro_reason}{RESET}")
        print(f"{COLORS[1]}반대측: {con_choice} - {result.con_reason}{RESET}")
        print(f"{COLORS[2]}→ {"반대측" if result.first_idx else "찬성측"}이 먼저 발언합니다.{RESET}")
        print()

        first_pick_done.set()

    def speak_ready_noti(speaker_idx: int) -> None:
        speaker = "반대측" if speaker_idx else "찬성측"
        print(f"\n{COLORS[2]}{speaker}의 발언이 준비되었습니다.{RESET}")

    score_done = threading.Event()

    def score_calculated_noti(result: DebateResult):
        labels = {
            "relevance": "주제 적합성",
            "logic": "논리성     ",
            "persuasiveness": "설득력     ",
            "rebuttal": "반박 능력  ",
            "evidence": "근거 활용  ",
            "manner": "태도       ",
        }

        print(f"\n{COLORS[2]}===== 토론 평가 결과 ====={RESET}")
        for side, color, scores, total in [
            ("찬성측", COLORS[0], result.pro_scores, result.pro_result),
            ("반대측", COLORS[1], result.con_scores, result.con_result),
        ]:
            print(f"\n{color}{side} 총점: {total:>5}점{RESET}")
            for field, label in labels.items():
                elem = getattr(scores, field)
                print(f"{color}  {label}  {elem.score:>5}점 — {elem.reason}{RESET}")

        if result.pro_result > result.con_result:
            print(f"\n{COLORS[2]}찬성측이 승리하였습니다.{RESET}")
        elif result.pro_result < result.con_result:
            print(f"\n{COLORS[2]}반대측이 승리하였습니다.{RESET}")
        else:
            print(f"\n{COLORS[2]}무승부입니다.{RESET}")

        score_done.set()

    debate = Debate(
        topic=topic,
        speak_cnt=speak_cnt,
        first_picked_noti=first_picked_noti,
        speak_ready_noti=speak_ready_noti,
        score_calculated_noti=score_calculated_noti,
        moderator=moderator,
        pro=pro,
        con=con,
    )

    # 1) 선공 결정 대기
    print(f"{COLORS[2]}선공을 결정하고 있습니다...{RESET}")
    first_pick_done.wait()

    # 2) 토론 진행
    while not debate.finished():
        input()
        speaker_idx, emotion, message = debate.listen()
        speaker = "반대측" if speaker_idx else "찬성측"
        print(f"{COLORS[speaker_idx]}{speaker}: ({emotion}) {message}{RESET}")

    # 3) 종료 및 채점 대기
    print(f"\n{COLORS[2]}[{topic}] 주제에 대한 토론이 종료되었습니다.{RESET}")
    print(f"{COLORS[2]}채점 중입니다...{RESET}")
    score_done.wait()


if __name__ == "__main__":
    load_dotenv()
    configure_warnings()
    main()
