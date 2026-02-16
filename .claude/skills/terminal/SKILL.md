---
name: terminal
description: 터미널 명령어 실행 시 환경 규칙
---

# 터미널 명령어 규칙

터미널에서 명령어를 실행할 때 반드시 아래 규칙을 따릅니다.

## Python 패키지 관리

- Python 모듈 설치 시 **반드시 venv 가상환경**을 사용할 것
- venv 경로: `.venv/`
- 활성화: `source .venv/bin/activate` (bash) 또는 `.venv/Scripts/activate` (Windows)
- `pip install`은 항상 venv가 활성화된 상태에서 실행

## Claude 설정 관리

- 사용자의 홈 디렉토리(`~/.claude/`)에 있는 설정 파일은 **절대 수정하지 말 것**
- Claude 관련 설정은 오직 이 프로젝트 저장소 내의 `.claude/` 디렉토리만 수정

## Windows 인코딩

- Windows의 Python 기본 인코딩은 cp949이므로, 한글이 포함된 파일을 `open()`할 때 반드시 `encoding='utf-8'`을 지정할 것
- Bash에서 Python 코드를 인라인 실행(`python -c`)할 때도 동일하게 주의
