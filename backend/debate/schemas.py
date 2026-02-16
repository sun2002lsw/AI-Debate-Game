from pydantic import BaseModel

from moderator import DebateScore


class DebateResult(BaseModel):
    pro_scores: DebateScore
    pro_result: float
    con_scores: DebateScore
    con_result: float
