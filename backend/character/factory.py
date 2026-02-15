"""Character factory -- 문자열만으로 Character를 생성."""

from __future__ import annotations

import uuid

from persona import create_persona
from llm.factory import create_llm

from .character import Character


def create_character(
    topic: str,
    is_pro: bool,
    persona: str | int,
    model: str | int,
) -> Character:
    character_id = uuid.uuid4().hex[:8]
    persona_obj = create_persona(persona)
    llm = create_llm(model)

    return Character(id=character_id, topic=topic, is_pro=is_pro, persona=persona_obj, llm=llm)
