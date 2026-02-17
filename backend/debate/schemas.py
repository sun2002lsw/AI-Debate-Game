from pydantic import BaseModel

from evaluator.schemas import DebateScores


class FirstSpeakResult(BaseModel):
    pro_want_first: bool
    pro_reason: str
    con_want_first: bool
    con_reason: str
    first_speaker_idx: int


class DebateResult(BaseModel):
    pro_scores: DebateScores
    pro_result: float
    con_scores: DebateScores
    con_result: float
