from evaluator import DebateScores

WEIGHTS = {
    "relevance": 5,  # 주제 적합성
    "logic": 4,  # 논리성
    "persuasiveness": 3,  # 설득력
    "rebuttal": 3,  # 반박 능력
    "evidence": 3,  # 근거 활용
    "manner": 2,  # 태도
}

_TOTAL_WEIGHT = sum(WEIGHTS.values())


def calculate(score: DebateScores) -> float:
    weighted_sum = (
        0
        + score.relevance.score * WEIGHTS["relevance"]
        + score.logic.score * WEIGHTS["logic"]
        + score.persuasiveness.score * WEIGHTS["persuasiveness"]
        + score.rebuttal.score * WEIGHTS["rebuttal"]
        + score.evidence.score * WEIGHTS["evidence"]
        + score.manner.score * WEIGHTS["manner"]
    )

    return round(weighted_sum / _TOTAL_WEIGHT, 1)
