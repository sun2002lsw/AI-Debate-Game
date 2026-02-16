import threading

from dotenv import load_dotenv

from cli_print import *
from common.warnings import configure as configure_warnings
from debater import create_debater
from persona import list_personas
from llm import list_models, create_llm
from debate import Debate
from moderator import Moderator


def main():
    topic, speak_cnt = input_debate_setup()

    print_options(list_personas(), list_models())
    pro_perso, pro_model, con_perso, con_model, mod_model = input_selections()

    # 토론 참가자 생성
    pro = create_debater(persona=pro_perso, model=pro_model)
    con = create_debater(persona=con_perso, model=con_model)
    moderator = Moderator(llm=create_llm(mod_model))

    # 토론 처리 알림들
    first_pick_done = threading.Event()
    score_done = threading.Event()

    def first_picked_noti() -> None:
        first_pick_done.set()

    def speak_ready_noti(speaker_idx: int) -> None:
        print_speak_ready(speaker_idx)

    def score_calculated_noti():
        score_done.set()

    # 토론 구성
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
    print_deciding_first()
    first_pick_done.wait()

    result = debate.first_pick_result()
    assert result is not None
    print_first_pick(result)

    # 2) 토론 진행
    while not debate.finished():
        input()
        speaker_idx, emotion, message = debate.listen()
        print_speak(speaker_idx, emotion, message)

    # 3) 종료 및 채점 대기
    print_debate_ended(topic)
    print_scoring()
    score_done.wait()

    result = debate.debate_result()
    assert result is not None
    print_debate_result(result)


if __name__ == "__main__":
    load_dotenv()
    configure_warnings()
    main()
