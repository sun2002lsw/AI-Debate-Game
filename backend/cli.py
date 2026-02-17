import asyncio
import msvcrt

from dotenv import load_dotenv

from cli_print import *
from common.warnings import configure as configure_warnings
from debater import create_debater
from persona import list_personas
from llm import list_models, create_llm
from debate import Debate
from evaluator import Evaluator


async def main():
    topic, speak_cnt = input_debate_setup()

    print_options(list_personas(), list_models())
    pro_perso, pro_model, con_perso, con_model, mod_model = input_selections()

    # 토론 참가자 생성
    pro = create_debater(persona=pro_perso, model=pro_model)
    con = create_debater(persona=con_perso, model=con_model)
    evaluator = Evaluator(llm=create_llm(mod_model))

    # 토론 처리 알림들
    first_speak_decided = asyncio.Event()
    debate_result_evaluating = asyncio.Event()
    debate_result_evaluated = asyncio.Event()

    def first_speak_deciding_noti():
        print_deciding_first()

    def first_speak_decided_noti():
        first_speak_decided.set()
        result = debate.first_speak_result()
        assert result is not None
        print_first_speak(result)

    def speak_ready_noti(speaker_idx: int):
        print_speak_ready(speaker_idx)

    def debate_result_evaluating_noti():
        debate_result_evaluating.set()
        print_debate_ended(topic)

    def debate_result_evaluated_noti():
        debate_result_evaluated.set()
        result = debate.debate_result()
        assert result is not None
        print_debate_result(result)

    # 토론 구성
    debate = Debate(
        topic=topic,
        speak_cnt=speak_cnt,
        first_speak_deciding_noti=first_speak_deciding_noti,
        first_speak_decided_noti=first_speak_decided_noti,
        speak_ready_noti=speak_ready_noti,
        debate_result_evaluating_noti=debate_result_evaluating_noti,
        debate_result_evaluated_noti=debate_result_evaluated_noti,
        evaluator=evaluator,
        pro=pro,
        con=con,
    )

    debate.start()

    # 1) 선공 결정 대기
    await first_speak_decided.wait()

    # 2) 토론 진행
    while not debate_result_evaluating.is_set():
        await asyncio.to_thread(msvcrt.getwch)
        chat = debate.listen()
        if chat:
            print_speak(chat.speaker_idx, chat.emotion, chat.message)

    # 3) 채점 완료 대기
    await debate_result_evaluated.wait()


if __name__ == "__main__":
    load_dotenv()
    configure_warnings()
    asyncio.run(main())
