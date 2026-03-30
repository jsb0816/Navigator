"""PM 에이전트 LangGraph — Atomizer → Prioritizer → State Writer."""

from __future__ import annotations

import json
import os
import re
import time
from typing import Any, Dict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph

from agent.schemas import RTM_Master
from agent.state import PMState
from utils.file_io import save_project_state

load_dotenv()

# ── LLM 인스턴스 ──────────────────────────────────────────────────────
_LLM = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
    convert_system_message_to_human=True,
)

SYSTEM_PERSONA = (
    "당신은 10년 경력의 IT 서비스 기획자(PM)입니다. "
    "사용자의 아이디어를 분석하여 체계적인 요구사항 명세로 변환합니다. "
    "반드시 JSON 형식으로만 답변하세요. 추가 설명이나 마크다운 코드블럭 없이 순수 JSON만 출력합니다."
)


def _extract_json(text: str) -> Any:
    """LLM 응답에서 JSON을 안전하게 추출합니다."""
    # 코드블럭 안에 있을 수 있으므로 제거
    cleaned = re.sub(r"```(?:json)?\s*", "", text)
    cleaned = cleaned.strip().rstrip("`")
    return json.loads(cleaned)


# ── Node 1: Atomizer ──────────────────────────────────────────────────
def atomizer_node(state: PMState) -> Dict[str, Any]:
    """사용자 아이디어를 최소 단위 기능으로 분해합니다."""
    prompt = f"""{SYSTEM_PERSONA}

아래 아이디어를 분석하여 최소 단위의 기능 요구사항으로 쪼개 주세요.
각 요구사항에는 req_id (REQ_001, REQ_002 ...), title, description 을 포함합니다.

결과를 아래 JSON 형식으로 출력하세요:
{{"requirements": [{{"req_id": "REQ_001", "title": "...", "description": "..."}}]}}

사용자 아이디어:
{state["user_idea"]}
"""
    response = _LLM.invoke(prompt)
    data = _extract_json(response.content)
    requirements = data.get("requirements", [])
    return {"requirements_raw": requirements}


# ── Node 2: Prioritizer ──────────────────────────────────────────────
def prioritizer_node(state: PMState) -> Dict[str, Any]:
    """각 요구사항에 MoSCoW 우선순위를 할당합니다."""
    time.sleep(5)  # 429 에러 방지

    reqs_json = json.dumps(state["requirements_raw"], ensure_ascii=False)
    prompt = f"""{SYSTEM_PERSONA}

아래 요구사항 목록에 MoSCoW 우선순위(Must, Should, Could, Won't)를 할당해 주세요.
각 항목에 "priority" 필드를 추가하세요.

결과를 아래 JSON 형식으로 출력하세요:
{{"requirements": [{{"req_id": "...", "title": "...", "description": "...", "priority": "Must|Should|Could|Won't"}}]}}

요구사항 목록:
{reqs_json}
"""
    response = _LLM.invoke(prompt)
    data = _extract_json(response.content)
    requirements = data.get("requirements", [])
    return {"requirements_raw": requirements}


# ── Node 3: State Writer ─────────────────────────────────────────────
def state_writer_node(state: PMState) -> Dict[str, Any]:
    """완성된 RTM을 검증하고 PROJECT_STATE.md로 저장합니다."""
    time.sleep(5)  # 429 에러 방지 (이전 노드와의 간격)

    reqs = state["requirements_raw"]

    # Pydantic 검증
    rtm = RTM_Master(requirements=[])
    for r in reqs:
        try:
            from agent.schemas import Requirement
            rtm.requirements.append(Requirement(**r))
        except Exception:
            # priority 값이 Enum 에 맞지 않을 경우 문자열 그대로 유지
            rtm.requirements.append(
                Requirement(
                    req_id=r.get("req_id", "UNKNOWN"),
                    title=r.get("title", ""),
                    description=r.get("description", ""),
                    priority=r.get("priority"),
                )
            )

    rtm_dict = rtm.model_dump()

    # Markdown 파일로 저장
    save_project_state(rtm_dict["requirements"])

    return {"final_rtm": rtm_dict}


# ── 그래프 조립 ───────────────────────────────────────────────────────
def build_pm_graph() -> StateGraph:
    """PM 에이전트 LangGraph를 조립하여 반환합니다."""
    graph = StateGraph(PMState)

    graph.add_node("atomizer", atomizer_node)
    graph.add_node("prioritizer", prioritizer_node)
    graph.add_node("state_writer", state_writer_node)

    graph.set_entry_point("atomizer")
    graph.add_edge("atomizer", "prioritizer")
    graph.add_edge("prioritizer", "state_writer")
    graph.add_edge("state_writer", END)

    return graph.compile()


# 컴파일된 그래프 싱글턴
pm_app = build_pm_graph()
