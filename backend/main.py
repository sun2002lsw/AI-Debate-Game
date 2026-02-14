from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from character import Character
from debate import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 인메모리 세션 저장소
sessions: dict[str, Session] = {}


class CharacterCreate(BaseModel):
    name: str
    age: int


class SessionCreate(BaseModel):
    topic: str
    pro: CharacterCreate
    con: CharacterCreate
    max_rounds: int = 3


@app.get("/")
def root():
    return {"message": "hello world"}


@app.post("/api/debate")
def create_debate(body: SessionCreate):
    pro = Character(body.pro.name, body.pro.age)
    con = Character(body.con.name, body.con.age)

    session = Session(body.topic, pro, con, body.max_rounds)
    result = session.opening()

    sessions[session.session_id] = session
    return result


@app.post("/api/debate/{session_id}/speak")
def speak(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")

    try:
        return session.speaking()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/debate/{session_id}/history")
def get_history(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")

    return session.get_history()


@app.get("/api/debate/{session_id}/status")
def get_status(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")

    return session.get_status()
