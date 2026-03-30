"""Pydantic 모델 정의 — 요구사항(Requirement) 및 RTM."""

from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Priority(str, Enum):
    """MoSCoW 우선순위."""
    MUST = "Must"
    SHOULD = "Should"
    COULD = "Could"
    WONT = "Won't"


class Requirement(BaseModel):
    """단일 요구사항."""
    req_id: str = Field(..., description="요구사항 ID (예: REQ_001)")
    title: str = Field(..., description="요구사항 제목")
    description: str = Field(..., description="요구사항 상세 설명")
    priority: Priority | None = Field(None, description="MoSCoW 우선순위")


class RTM_Master(BaseModel):
    """Requirements Traceability Matrix — 최종 산출물."""
    requirements: List[Requirement] = Field(default_factory=list)


# ── SA 에이전트용 모델 ────────────────────────────────────────────────

class ArchitectureDecision(BaseModel):
    """기술 스택 및 디자인 패턴 결정."""
    frontend: str = Field(..., description="프론트엔드 기술 (예: React, Vue)")
    backend: str = Field(..., description="백엔드 기술 (예: FastAPI, Spring)")
    database: str = Field(..., description="데이터베이스 (예: PostgreSQL, MongoDB)")
    design_pattern: str = Field(..., description="아키텍처 패턴 (예: MVC, Layered, Hexagonal)")
    reasoning: str = Field("", description="기술 선택 근거")


class Dependency(BaseModel):
    """요구사항 간 의존성 (DAG 엣지)."""
    req_id: str = Field(..., description="대상 요구사항 ID")
    depends_on: List[str] = Field(default_factory=list, description="선행 요구사항 ID 리스트")


class SA_Result(BaseModel):
    """SA 에이전트 최종 산출물."""
    architecture: ArchitectureDecision
    dependencies: List[Dependency] = Field(default_factory=list)
    execution_order: List[str] = Field(default_factory=list, description="위상 정렬된 개발 순서")
