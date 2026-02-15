from __future__ import annotations

from .persona import Persona, PERSONAS_DIR


def list_personas() -> list[Persona]:
    """사용 가능한 페르소나를 정렬된 리스트로 반환."""
    return [Persona(d.name) for d in sorted(PERSONAS_DIR.iterdir()) if d.is_dir()]


def create_persona(value: str | int) -> Persona:
    """str | int → Persona 객체. 리스트에 없으면 에러."""
    personas = list_personas()

    if isinstance(value, int):
        if not (0 <= value < len(personas)):
            raise IndexError(f"Persona 인덱스 {value}가 범위를 벗어났습니다. ")
        return personas[value]

    for p in personas:
        if p.id == value:
            return p

    raise ValueError(f"알 수 없는 Persona: {value}")
