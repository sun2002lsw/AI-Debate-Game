## 프로젝트 구조

```
backend/
  main.py              # FastAPI 서버 진입점 (uvicorn)
  cli.py               # CLI 기반 내부 테스트용 실행 스크립트
  cli_print.py         # CLI 출력 전용 유틸리티 (색상·포맷 포함)
  requirements.txt     # Python 의존성 (fastapi, uvicorn, langchain-* 등)
  common/              # 공통 모듈 — debater·moderator 공유 유틸리티
    warnings.py        #   configure() — Pydantic 경고 필터
    schemas.py         #   EMOJI_PATTERN, strip_emoji()
    prompts.py         #   topic(), rules(), chat_history_section()
  debater/             # 토론 참가자 모듈 — LLM과 상호작용하는 토론 참가자
    debater.py         #   Debater 클래스 (structured output으로 발언 생성)
    factory.py         #   create_debater() 팩토리 — 문자열/인덱스로 Debater 생성
    schemas.py         #   Pydantic 모델 (Emotion, SpeakResponse, FirstAnnounceDecision)
    prompts.py         #   시스템/사용자 프롬프트 템플릿
  debate/              # 토론 모듈 — 토론 진행 및 상태 관리
    debate.py          #   Debate 클래스 (라운드, 턴, 히스토리 관리)
    schemas.py         #   Pydantic 모델 (DebateResult)
    score_calculator.py #   calculate() — DebateScore → 가중 평균 점수 (100점 기준)
  moderator/           # 사회자 모듈 — 토론 이의 제기 및 평가
    moderator.py       #   Moderator 클래스 (interrupt, analyze)
    schemas.py         #   Pydantic 모델 (DebateScore, InterruptResponse, AnalyzeResponse)
    prompts.py         #   사회자 프롬프트 템플릿
  persona/             # 페르소나 모듈 — 토론 참가자 성격 정의
    persona.py         #   Persona 클래스 (info.txt + strategy.txt 파싱)
    factory.py         #   create_persona() 팩토리 + list_personas()
    personas/          #   페르소나 데이터 (philosopher, crybaby, psycho, thug)
  llm/                 # LLM 모듈 — 다중 프로바이더 지원
    factory.py         #   create_llm() 팩토리 + list_models()
frontend/
  src/App.jsx          # React 앱 (Vite, localhost:5173)
.claude/
  skills/commit/       # /commit 스킬
  skills/api/          # /api 스킬 (RESTful 엔드포인트 추가 가이드)
  skills/coding-style/ # 코딩 스타일 규칙
  skills/terminal/     # 터미널 명령어 규칙
```

- 파일/디렉토리 구조가 변경되면 이 문서의 프로젝트 구조도 함께 갱신할 것

## 개발 환경 규칙

- 코딩 스타일: `.claude/skills/coding-style/SKILL.md` 참고
- 터미널 명령어: `.claude/skills/terminal/SKILL.md` 참고
