## 프로젝트 구조

```
backend/
  main.py              # FastAPI 서버 진입점 (uvicorn)
  cli.py               # CLI 기반 내부 테스트용 실행 스크립트
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
```

- 파일/디렉토리 구조가 변경되면 이 문서의 프로젝트 구조도 함께 갱신할 것

## 개발 환경 규칙

### Python 패키지 관리
- Python 모듈 설치 시 **반드시 venv 가상환경**을 사용할 것
- venv 경로: `.venv/`
- 활성화: `source .venv/bin/activate` (bash) 또는 `.venv/Scripts/activate` (Windows)
- `pip install`은 항상 venv가 활성화된 상태에서 실행

### Claude 설정 관리
- 사용자의 홈 디렉토리(`~/.claude/`)에 있는 설정 파일은 **절대 수정하지 말 것**
- Claude 관련 설정은 오직 이 프로젝트 저장소 내의 `.claude/` 디렉토리만 수정

### Windows 인코딩
- Windows의 Python 기본 인코딩은 cp949이므로, 한글이 포함된 파일을 `open()`할 때 반드시 `encoding='utf-8'`을 지정할 것
- Bash에서 Python 코드를 인라인 실행(`python -c`)할 때도 동일하게 주의

### Import 규칙
- 모듈의 공개 API를 전부(또는 대부분) 가져올 때는 `from . import module` 방식을 사용하고, `module.name`으로 접근
- 1~2개만 가져올 때는 `from module import name` 방식 허용
- `__init__.py`의 re-export는 `from .module import name` 방식 유지
- `__init__.py`에는 re-export만 작성할 것 — 로직, 설정, 부수효과 코드를 넣지 않기

### 파일 포맷
- 모든 파일은 POSIX 규칙에 따라 마지막에 반드시 빈 줄(trailing newline)을 포함할 것
