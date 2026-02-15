import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "AI 토론 게임 API 서버가 실행 중입니다."}


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
