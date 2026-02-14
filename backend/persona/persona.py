from pathlib import Path

_PERSONAS_DIR = Path(__file__).parent / "personas"


class Persona:
    def __init__(self, persona_id: str):
        persona_dir = _PERSONAS_DIR / persona_id
        if not persona_dir.exists():
            raise FileNotFoundError(f"Persona directory not found: {persona_dir}")

        self.name, self.age, self.summary = self._parse_personal_info(persona_dir / "info.txt")
        self.strategy = (persona_dir / "strategy.txt").read_text(encoding="utf-8").strip()

    @staticmethod
    def _parse_personal_info(path: Path) -> tuple[str, int, str]:
        text = path.read_text(encoding="utf-8").strip()
        lines = text.splitlines()

        name = ""
        age = 0
        rest_lines: list[str] = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("이름:"):
                name = stripped.removeprefix("이름:").strip()
            elif stripped.startswith("나이:"):
                age = int(stripped.removeprefix("나이:").strip())
            elif stripped:
                rest_lines.append(stripped)

        summary = "\n".join(rest_lines)
        return name, age, summary
