"""SA 에이전트 LangGraph — Tech Architect → Dependency Mapper → Topological Sorter."""

from __future__ import annotations

import json
import os
import re
import time
from collections import defaultdict, deque
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph

from agent.schemas import SA_Result
from agent.state import SAState
from utils.file_io import append_sa_result, read_project_state

load_dotenv()

# ── LLM 인스턴스 ──────────────────────────────────────────────────────
_LLM = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
    convert_system_message_to_human=True,
)

SYSTEM_PERSONA = (
    "당신은 15년 경력의 소프트웨어 아키텍트(SA)입니다. "
    "요구사항 명세서를 분석하여 최적의 기술 스택, 아키텍처 패턴, 의존성 관계를 도출합니다. "
    "반드시 JSON 형식으로만 답변하세요. 추가 설명이나 마크다운 코드블럭 없이 순수 JSON만 출력합니다."
)


def _extract_json(text: str) -> Any:
    """LLM 응답에서 JSON을 안전하게 추출합니다."""
    cleaned = re.sub(r"```(?:json)?\s*", "", text)
    cleaned = cleaned.strip().rstrip("`")
    return json.loads(cleaned)


def _topological_sort(dependencies: list[Dict[str, Any]], all_req_ids: list[str]) -> list[str]:
    """Kahn 알고리즘 기반 위상 정렬을 수행합니다.

    Args:
        dependencies: [{"req_id": "REQ_002", "depends_on": ["REQ_001"]}, ...]
        all_req_ids: 전체 요구사항 ID 목록

    Returns:
        위상 정렬된 req_id 리스트. 순환 의존성이 있으면 남은 항목을 뒤에 추가.
    """
    # 그래프 구축
    in_degree: Dict[str, int] = {rid: 0 for rid in all_req_ids}
    adj: Dict[str, list[str]] = defaultdict(list)

    for dep in dependencies:
        node = dep["req_id"]
        for parent in dep.get("depends_on", []):
            if parent in in_degree:
                adj[parent].append(node)
                in_degree[node] = in_degree.get(node, 0) + 1

    # BFS (Kahn)
    queue: deque[str] = deque()
    for rid in all_req_ids:
        if in_degree.get(rid, 0) == 0:
            queue.append(rid)

    result: list[str] = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # 순환 의존성이 있을 경우 남은 노드 추가
    remaining = [rid for rid in all_req_ids if rid not in result]
    result.extend(remaining)

    return result


# ── Node 1: Tech Architect ────────────────────────────────────────────
def tech_architect_node(state: SAState) -> Dict[str, Any]:
    """요구사항을 분석하여 기술 스택과 디자인 패턴을 결정합니다."""
    reqs_json = json.dumps(state["requirements"], ensure_ascii=False)
    prompt = f"""{SYSTEM_PERSONA}

아래 요구사항 목록을 분석하여 최적의 기술 스택과 아키텍처 패턴을 결정해 주세요.

결과를 아래 JSON 형식으로 출력하세요:
{{
  "frontend": "프론트엔드 프레임워크명",
  "backend": "백엔드 프레임워크명",
  "database": "데이터베이스명",
  "design_pattern": "아키텍처 패턴명 (예: MVC, Layered, Clean Architecture)",
  "reasoning": "선택 근거 (한국어 2~3문장)"
}}

요구사항 목록:
{reqs_json}
"""
    response = _LLM.invoke(prompt)
    architecture = _extract_json(response.content)
    return {"architecture_raw": architecture}


# ── Node 2: Dependency Mapper ─────────────────────────────────────────
def dependency_mapper_node(state: SAState) -> Dict[str, Any]:
    """각 요구사항 간의 의존성(선수 조건)을 파악하여 DAG를 생성합니다."""
    time.sleep(20)  # 429 에러 방지

    reqs_json = json.dumps(state["requirements"], ensure_ascii=False)
    req_ids = [r["req_id"] for r in state["requirements"]]

    prompt = f"""{SYSTEM_PERSONA}

아래 요구사항 목록에서 각 기능 간의 의존성(선수 조건)을 분석해 주세요.
예를 들어, "댓글 작성" 기능은 "게시글 조회" 기능이 먼저 구현되어야 합니다.
의존성이 없는 경우 depends_on을 빈 배열로 두세요.

사용 가능한 req_id 목록: {json.dumps(req_ids)}

결과를 아래 JSON 형식으로 출력하세요:
{{"dependencies": [{{"req_id": "REQ_002", "depends_on": ["REQ_001"]}}]}}

요구사항 목록:
{reqs_json}
"""
    response = _LLM.invoke(prompt)
    data = _extract_json(response.content)
    dependencies = data.get("dependencies", [])
    return {"dependencies_raw": dependencies}


# ── Node 3: Topological Sorter & Writer ───────────────────────────────
def topological_sorter_node(state: SAState) -> Dict[str, Any]:
    """위상 정렬을 수행하고 결과를 PROJECT_STATE.md에 Append 합니다."""
    time.sleep(20)  # 429 에러 방지

    req_ids = [r["req_id"] for r in state["requirements"]]
    deps = state["dependencies_raw"]
    arch = state["architecture_raw"]

    # 위상 정렬 실행
    order = _topological_sort(deps, req_ids)

    # Pydantic 검증
    from agent.schemas import ArchitectureDecision, Dependency
    try:
        arch_model = ArchitectureDecision(**arch)
    except Exception:
        arch_model = ArchitectureDecision(
            frontend=arch.get("frontend", "Unknown"),
            backend=arch.get("backend", "Unknown"),
            database=arch.get("database", "Unknown"),
            design_pattern=arch.get("design_pattern", "Unknown"),
            reasoning=arch.get("reasoning", ""),
        )

    dep_models = []
    for d in deps:
        try:
            dep_models.append(Dependency(**d))
        except Exception:
            dep_models.append(Dependency(
                req_id=d.get("req_id", "UNKNOWN"),
                depends_on=d.get("depends_on", []),
            ))

    sa_result = SA_Result(
        architecture=arch_model,
        dependencies=dep_models,
        execution_order=order,
    )
    sa_dict = sa_result.model_dump()

    # PROJECT_STATE.md에 Append
    append_sa_result(
        architecture=sa_dict["architecture"],
        dependencies=sa_dict["dependencies"],
        execution_order=sa_dict["execution_order"],
    )

    return {"execution_order": order, "final_sa": sa_dict}


# ── 그래프 조립 ───────────────────────────────────────────────────────
def build_sa_graph() -> StateGraph:
    """SA 에이전트 LangGraph를 조립하여 반환합니다."""
    graph = StateGraph(SAState)

    graph.add_node("tech_architect", tech_architect_node)
    graph.add_node("dependency_mapper", dependency_mapper_node)
    graph.add_node("topological_sorter", topological_sorter_node)

    graph.set_entry_point("tech_architect")
    graph.add_edge("tech_architect", "dependency_mapper")
    graph.add_edge("dependency_mapper", "topological_sorter")
    graph.add_edge("topological_sorter", END)

    return graph.compile()


# 컴파일된 그래프 싱글턴
sa_app = build_sa_graph()
