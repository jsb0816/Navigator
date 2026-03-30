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
