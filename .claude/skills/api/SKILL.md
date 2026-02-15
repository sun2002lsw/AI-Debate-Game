---
name: api
description: FastAPI 엔드포인트를 RESTful 설계 원칙에 따라 추가
---

# API 추가 스킬

기존 FastAPI 앱(`backend/main.py`)에 새로운 API 엔드포인트를 RESTful 설계 원칙에 따라 추가합니다.

## 절차

### 1단계: 요구사항 분석

사용자의 요청을 분석하여 아래 항목을 정리합니다:

- **리소스 이름**: REST 리소스 식별 (예: debates, debaters, personas)
- **필요한 동작**: CRUD 중 어떤 동작이 필요한지 결정
- **데이터 구조**: 요청/응답에 필요한 필드와 타입 파악
- **관련 모듈**: `backend/` 내 기존 모듈 중 활용할 것 확인 (debater, debate, persona, llm)

### 2단계: API 설계

RESTful 원칙에 따라 엔드포인트를 설계합니다:

#### URL 규칙
- 리소스명은 복수형 명사 사용: `/debates`, `/debaters`
- 계층 관계 표현: `/debates/{debate_id}/messages`
- 동작은 HTTP 메서드로 구분 (GET/POST/PUT/DELETE)

#### HTTP 메서드 매핑
| 동작 | 메서드 | 경로 예시 | 설명 |
|------|--------|-----------|------|
| 목록 조회 | GET | `/debates` | 리소스 목록 반환 |
| 단건 조회 | GET | `/debates/{id}` | 특정 리소스 반환 |
| 생성 | POST | `/debates` | 새 리소스 생성 |
| 수정 | PUT | `/debates/{id}` | 리소스 전체 수정 |
| 삭제 | DELETE | `/debates/{id}` | 리소스 삭제 |

### 3단계: Pydantic 스키마 작성

`backend/` 내에 스키마 파일을 작성합니다. 기존 패턴을 참고합니다:

- 기존 예시: `backend/debater/schemas.py` (Emotion, FirstAnnounceDecision, SpeakResponse)
- 요청 스키마: `XxxRequest(BaseModel)` — 클라이언트가 보내는 데이터
- 응답 스키마: `XxxResponse(BaseModel)` — 서버가 반환하는 데이터
- 모든 필드에 `Field(description="...")` 작성
- 필요시 `field_validator`로 입력 검증

스키마 파일 위치 규칙:
- API 전용 스키마는 `backend/api/schemas.py`에 작성
- 도메인 모듈 내부 스키마(LLM용 등)는 해당 모듈 내에 유지

### 4단계: 엔드포인트 구현

`backend/main.py`에 엔드포인트를 추가합니다:

```python
from fastapi import FastAPI, HTTPException

@app.post("/debates", response_model=DebateResponse, status_code=201)
async def create_debate(request: DebateRequest):
    try:
        # 비즈니스 로직
        ...
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

구현 규칙:
- 엔드포인트 함수명은 동작을 명확히 표현: `create_debate`, `get_debate`, `list_debates`
- `response_model`을 항상 지정하여 응답 형태를 명시
- 성공 상태 코드를 명시: 생성=201, 조회=200, 삭제=204
- 비즈니스 로직은 기존 도메인 모듈(debate, debater 등)에 위임

### 5단계: 에러 처리

일관된 에러 응답을 제공합니다:

| 상태 코드 | 사용 경우 |
|-----------|-----------|
| 400 | 잘못된 요청 (유효성 검증 실패) |
| 404 | 리소스를 찾을 수 없음 |
| 422 | Pydantic 검증 실패 (FastAPI 자동 처리) |
| 500 | 서버 내부 오류 |

```python
from fastapi import HTTPException

# 리소스 없음
raise HTTPException(status_code=404, detail="토론을 찾을 수 없습니다")

# 잘못된 요청
raise HTTPException(status_code=400, detail="유효하지 않은 페르소나입니다")
```

### 6단계: CORS 확인

`backend/main.py`에 이미 CORS 미들웨어가 설정되어 있는지 확인합니다:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- 프론트엔드 출처(`http://localhost:5173`)가 `allow_origins`에 포함되어 있는지 확인
- 새 엔드포인트가 특수 헤더를 요구하는 경우 `allow_headers`에 추가
- 배포 시에는 `allow_origins`를 실제 도메인으로 변경 필요

### 7단계: 설계 보고 및 확인

아래 형식으로 사용자에게 API 설계를 보고합니다:

```
## API 설계

### 엔드포인트
- `POST /debates` — 새 토론 생성
- `GET /debates/{id}` — 토론 상태 조회

### 스키마
- **요청**: DebateRequest(topic, pro_persona, con_persona, max_rounds)
- **응답**: DebateResponse(debate_id, topic, status)

### 변경 파일
- `backend/main.py` — 엔드포인트 추가
- `backend/api/schemas.py` — 요청/응답 스키마 (신규)
```

AskUserQuestion 도구를 사용하여 사용자에게 승인을 요청합니다.

## 주의사항

- 기존 `backend/main.py`의 CORS 설정과 앱 구조를 유지합니다
- 도메인 로직은 엔드포인트에 직접 작성하지 않고 기존 모듈에 위임합니다
- 모든 임포트는 기존 패턴을 따릅니다 (상대 임포트: `from debater import Debater`)
- `.env` 파일의 API 키 등 민감 정보는 응답에 포함하지 않습니다
- 스키마 필드 설명은 한글로 작성합니다
