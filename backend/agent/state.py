"""LangGraph State 스키마 정의."""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class PMState(TypedDict, total=False):
    """PM 에이전트 그래프의 상태."""
    user_idea: str                   # 사용자 원본 아이디어 텍스트
    requirements_raw: List[Dict[str, Any]]  # Atomizer → Prioritizer 중간 결과
    final_rtm: Dict[str, Any]        # 최종 RTM JSON


class SAState(TypedDict, total=False):
    """SA 에이전트 그래프의 상태."""
    requirements: List[Dict[str, Any]]       # PM에서 넘어온 요구사항 목록
    architecture_raw: Dict[str, Any]         # Tech Architect 노드 결과
    dependencies_raw: List[Dict[str, Any]]   # Dependency Mapper 노드 결과
    execution_order: List[str]               # 위상 정렬된 개발 순서
    final_sa: Dict[str, Any]                 # 최종 SA 결과 JSON
