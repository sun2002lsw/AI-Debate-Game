import unicodedata

from debate.schemas import DebateResult, FirstSpeakResult
from evaluator.schemas import DebateScores
from persona import Persona

_COLORS = ["\033[94m", "\033[91m", "\033[93m"]  # 찬성=파랑, 반대=빨강, 시스템=노랑
_RESET = "\033[0m"

_SIDE_NAMES = ["찬성측", "반대측"]


def input_debate_setup() -> tuple[str, int]:
    topic = input("토론 주제: ")
    speak_cnt = int(input("발언 횟수: "))

    return topic, speak_cnt


def print_options(personas: list[Persona], models: list[str]):
    print("\n===== 페르소나 목록 =====")
    for i, p in enumerate(personas):
        print(f"  {i}: {p.name}({p.age}세) - {p.summary}")
    print("\n===== LLM 모델 목록 =====")
    for i, m in enumerate(models):
        print(f"  {i}: {m}")
    print()


def input_selections() -> tuple[int, int, int, int, int]:
    pro_perso = int(input("찬성측 인격 선택: "))
    pro_model = int(input("찬성측 모델 선택: "))
    con_perso = int(input("반대측 인격 선택: "))
    con_model = int(input("반대측 모델 선택: "))
    mod_model = int(input("평가자 모델 선택: "))
    print()

    return pro_perso, pro_model, con_perso, con_model, mod_model


def print_speak_ready(speaker_idx: int):
    print(f"\n{_COLORS[2]}{_SIDE_NAMES[speaker_idx]}의 발언이 준비되었습니다.{_RESET}")


def print_deciding_first():
    print(f"{_COLORS[2]}선공을 결정하고 있습니다...{_RESET}")


def print_first_speak(result: FirstSpeakResult):
    pro_choice = "선공 희망" if result.pro_want_first else "후공 희망"
    con_choice = "선공 희망" if result.con_want_first else "후공 희망"

    print(f"{_COLORS[0]}찬성측: {pro_choice} - {result.pro_reason}{_RESET}")
    print(f"{_COLORS[1]}반대측: {con_choice} - {result.con_reason}{_RESET}")
    print(f"{_COLORS[2]}→ {_SIDE_NAMES[result.first_speaker_idx]}이 먼저 발언합니다.{_RESET}")


def print_speak(speaker_idx: int, emotion: str, message: str):
    side = _SIDE_NAMES[speaker_idx]
    print(f"{_COLORS[speaker_idx]}{side}: ({emotion}) {message}{_RESET}")


def print_debate_ended(topic: str):
    print(f"\n{_COLORS[2]}[{topic}] 주제에 대한 토론이 종료되었습니다. 토론에 대한 평가를 시작합니다.{_RESET}")


def print_debate_result(result: DebateResult):
    print(f"\n{_COLORS[2]}===== 토론 평가 결과 ====={_RESET}")

    for side, color, evaluation in [("찬성측", _COLORS[0], result.pro), ("반대측", _COLORS[1], result.con)]:
        print(f"\n{color}{side} 총점: {evaluation.total_score:>5}점{_RESET}")

        # description "라벨: 설명" 형태에서 콜론 앞부분(라벨)만 추출
        labels: dict[str, str] = {}
        for name, field in DebateScores.model_fields.items():
            desc = field.description or name
            labels[name] = desc.split(":")[0]

        # 가장 넓은 라벨에 맞춰 패딩하여 테이블 정렬
        max_w = max(_display_width(label) for label in labels.values())
        for name, label in labels.items():
            pad = " " * (max_w - _display_width(label))
            elem = getattr(evaluation.scores, name)
            print(f"{color}  {label}{pad}  {elem.score:>5}점 — {elem.reason}{_RESET}")

    if result.pro.total_score > result.con.total_score:
        print(f"\n{_COLORS[2]}찬성측이 승리하였습니다.{_RESET}")
    elif result.pro.total_score < result.con.total_score:
        print(f"\n{_COLORS[2]}반대측이 승리하였습니다.{_RESET}")
    else:
        print(f"\n{_COLORS[2]}무승부입니다.{_RESET}")


def _display_width(s: str) -> int:
    """터미널에서의 실제 표시 폭을 계산한다.

    한글·한자 등 동아시아 전각 문자(F, W)는 2칸,
    영문·숫자·공백 등 반각 문자는 1칸으로 계산한다.
    """
    width = 0
    for char in s:
        east_asian = unicodedata.east_asian_width(char)
        if east_asian in ("F", "W"):  # Fullwidth / Wide — 한글, 한자 등
            width += 2
        else:
            width += 1

    return width
