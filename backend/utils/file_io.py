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


def read_project_state(output_dir: str | None = None) -> str:
    """PROJECT_STATE.md를 읽어 문자열로 반환합니다."""
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    filepath = os.path.join(output_dir, "PROJECT_STATE.md")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"PROJECT_STATE.md를 찾을 수 없습니다: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def append_sa_result(
    architecture: Dict[str, Any],
    dependencies: List[Dict[str, Any]],
    execution_order: List[str],
    output_dir: str | None = None,
) -> str:
    """SA 분석 결과를 PROJECT_STATE.md 하단에 Append합니다.

    Returns:
        저장된 파일의 절대 경로.
    """
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    filepath = os.path.join(output_dir, "PROJECT_STATE.md")

    lines: list[str] = []
    lines.append("\n---\n")
    lines.append("# 🏗️ SA Analysis — Architecture & Execution Order\n")

    # 기술 스택
    lines.append("## 기술 스택 & 디자인 패턴\n")
    lines.append(f"| 항목 | 선택 |")
    lines.append(f"|------|------|")
    lines.append(f"| Frontend | {architecture.get('frontend', '-')} |")
    lines.append(f"| Backend | {architecture.get('backend', '-')} |")
    lines.append(f"| Database | {architecture.get('database', '-')} |")
    lines.append(f"| Design Pattern | {architecture.get('design_pattern', '-')} |")
    if architecture.get("reasoning"):
        lines.append(f"\n> **선택 근거:** {architecture['reasoning']}\n")

    # 의존성 맵
    lines.append("\n## 요구사항 의존성 (DAG)\n")
    lines.append("| REQ ID | Depends On |")
    lines.append("|--------|-----------|")
    for dep in dependencies:
        rid = dep.get("req_id", "")
        deps = ", ".join(dep.get("depends_on", [])) or "(없음)"
        lines.append(f"| {rid} | {deps} |")

    # 위상 정렬 결과
    lines.append("\n## 개발 순서 (위상 정렬)\n")
    for idx, req_id in enumerate(execution_order, 1):
        lines.append(f"{idx}. **{req_id}**")

    sa_content = "\n".join(lines) + "\n"

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(sa_content)

    return filepath
