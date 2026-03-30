"""LangGraph State 스키마 정의."""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class PMState(TypedDict, total=False):
    """PM 에이전트 그래프의 상태."""
    user_idea: str                   # 사용자 원본 아이디어 텍스트
    requirements_raw: List[Dict[str, Any]]  # Atomizer → Prioritizer 중간 결과
    final_rtm: Dict[str, Any]        # 최종 RTM JSON
