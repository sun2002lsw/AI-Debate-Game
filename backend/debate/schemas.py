from pydantic import BaseModel

from moderator import DebateScore


class FirstPickResult(BaseModel):
    pro_want_first: bool
    pro_reason: str
    con_want_first: bool
    con_reason: str
    first_idx: int


class DebateResult(BaseModel):
    pro_scores: DebateScore
    pro_result: float
    con_scores: DebateScore
    con_result: float
