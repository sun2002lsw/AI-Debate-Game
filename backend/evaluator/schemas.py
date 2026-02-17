from __future__ import annotations

from pydantic import BaseModel, Field


class ScoreElement(BaseModel):
    score: int = Field(description="0~100 사이의 점수")
    reason: str = Field(description="해당 점수를 부여한 이유")


class DebateScores(BaseModel):
    relevance: ScoreElement = Field(
        description="주제 적합성: 주어진 토론 주제에서 벗어나지 않고 논점을 유지했는지 평가"
    )
    logic: ScoreElement = Field(description="논리성: 주장이 모순 없이 일관되며, 인과 관계가 명확한지 평가")
    evidence: ScoreElement = Field(
        description="근거 활용: 주장을 뒷받침하는 객관적 사실, 통계, 예시가 적절히 사용되었는지 평가"
    )
    rebuttal: ScoreElement = Field(
        description="반박 능력: 상대방의 핵심 논리를 파악하고 이에 대해 효과적으로 방어하거나 역공했는지 평가 (첫 발언인 경우 입론의 완성도로 대체)"
    )
    manner: ScoreElement = Field(description="태도: 비방, 욕설 없이 정중한 어조를 유지하며 상대를 존중했는지 평가")
    persuasiveness: ScoreElement = Field(
        description="설득력: 문장이 명료하고 호소력이 있어 청중을 설득할 수 있는 표현력을 갖췄는지 평가"
    )

    def to_evaluation(self) -> DebateEvaluation:
        from .score_calculator import calculate

        return DebateEvaluation(scores=self, total_score=calculate(self))


class DebateEvaluation(BaseModel):
    scores: DebateScores
    total_score: float


class EvaluateResponse(BaseModel):
    debate_scores: dict[str, DebateScores] = Field(description="각 토론자 id를 key로 가지는 딕셔너리")
