from __future__ import annotations

import uuid

from persona import create_persona
from llm.factory import create_llm

from .debater import Debater


def create_debater(persona: str | int, model: str | int) -> Debater:
    debater_id = uuid.uuid4().hex[:8]
    persona_obj = create_persona(persona)
    llm = create_llm(model)

    return Debater(id=debater_id, persona=persona_obj, llm=llm)
