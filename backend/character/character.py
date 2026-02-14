import random


class Character:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def want_first_announce(self, topic: str) -> bool:
        return random.choice([True, False])

    def speak(self, topic: str, chat_history: list[dict[str, str]]) -> str:
        return f"메시지 - {random.randint(1, 1000)}"
