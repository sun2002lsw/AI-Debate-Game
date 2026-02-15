## 프로젝트 구조

```
backend/
  main.py              # FastAPI 서버 진입점 (uvicorn)
  cli.py               # CLI 기반 내부 테스트용 실행 스크립트
  requirements.txt     # Python 의존성 (fastapi, uvicorn, langchain-* 등)
  character/           # 캐릭터 모듈 — LLM과 상호작용하는 토론 참가자
    character.py       #   Character 클래스 (structured output으로 발언 생성)
    schemas.py         #   Pydantic 모델 (Emotion, SpeakResponse, FirstAnnounceDecision)
    prompts.py         #   시스템/사용자 프롬프트 템플릿
  debate/              # 토론 모듈 — 토론 진행 및 상태 관리
    debate.py          #   Debate 클래스 (라운드, 턴, 히스토리 관리)
  persona/             # 페르소나 모듈 — 캐릭터 성격 정의
    persona.py         #   Persona 로더 (info.txt + strategy.txt 파싱)
    personas/          #   페르소나 데이터 (philosopher, crybaby, psycho, thug)
  llm/                 # LLM 모듈 — 다중 프로바이더 지원
    factory.py         #   create_llm() — 모델명으로 OpenAI/Anthropic/Google 자동 선택
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

### 파일 포맷
- 모든 파일은 POSIX 규칙에 따라 마지막에 반드시 빈 줄(trailing newline)을 포함할 것
