"""PROJECT_STATE.md 파일 저장 유틸리티."""

from __future__ import annotations

import os
from typing import Any, Dict, List


def _build_markdown_table(requirements: List[Dict[str, Any]]) -> str:
    """요구사항 리스트를 Markdown 표로 변환합니다."""
    lines: list[str] = []
    lines.append("# 📋 PROJECT STATE — Requirements Traceability Matrix\n")
    lines.append("| REQ ID | Title | Description | Priority |")
    lines.append("|--------|-------|-------------|----------|")
    for req in requirements:
        rid = req.get("req_id", "")
        title = req.get("title", "")
        desc = req.get("description", "")
        prio = req.get("priority", "")
        lines.append(f"| {rid} | {title} | {desc} | {prio} |")
    return "\n".join(lines) + "\n"


def save_project_state(requirements: List[Dict[str, Any]], output_dir: str | None = None) -> str:
    """PROJECT_STATE.md를 프로젝트 루트(또는 지정 경로)에 저장합니다.

    Returns:
        저장된 파일의 절대 경로.
    """
    if output_dir is None:
        # backend/ 의 상위 디렉토리(프로젝트 루트)를 기본값으로 사용
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    md_content = _build_markdown_table(requirements)
    filepath = os.path.join(output_dir, "PROJECT_STATE.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)
    return filepath
