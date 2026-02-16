---
name: coding-style
description: 프로젝트 코딩 스타일 및 포맷 규칙
---

# 코딩 스타일 규칙

코드 작성 시 반드시 아래 규칙을 따릅니다.

## Import 규칙

- 모듈의 공개 API를 전부(또는 대부분) 가져올 때는 `from module import *` 사용
- 1~2개만 가져올 때는 `from module import name` 방식 허용
- `__init__.py`의 re-export는 `from .module import name` 방식 유지
- `__init__.py`에는 re-export만 작성할 것 — 로직, 설정, 부수효과 코드를 넣지 않기

## 타입 힌트

- 모든 함수의 매개변수와 반환값에 반드시 타입 힌트를 명시할 것

## 코딩 스타일

- `return` 문은 항상 한 줄로 작성할 것 — 복잡한 표현식은 변수에 먼저 할당한 뒤 반환
- `return` 앞에 코드가 여러 줄이면 `return` 직전에 빈 줄을 넣을 것 (한 줄이면 생략 가능)
- docstring 끝에 마침표(`.`)를 붙이지 말 것

## 파일 포맷

- 모든 파일은 POSIX 규칙에 따라 마지막에 반드시 빈 줄(trailing newline)을 포함할 것
