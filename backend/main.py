"""FastAPI 엔트리포인트 — CORS 설정 및 API 라우터."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.pm_graph import pm_app
from agent.sa_graph import sa_app
from utils.file_io import read_project_state

app = FastAPI(title="SDLC Pipeline API", version="0.2.0")

# ── CORS 설정 ─────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 개발 환경 — 프론트엔드 어디서든 접근 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response 모델 ──────────────────────────────────────────
class IdeaRequest(BaseModel):
    idea: str


class AnalyzeResponse(BaseModel):
    requirements: list


class SAResponse(BaseModel):
    architecture: dict
    dependencies: list
    execution_order: list


# ── PM 엔드포인트 ─────────────────────────────────────────────────────
@app.post("/api/analyze-idea", response_model=AnalyzeResponse)
async def analyze_idea(payload: IdeaRequest):
    """사용자 아이디어를 받아 PM 에이전트를 실행하고 RTM을 반환합니다."""
    if not payload.idea.strip():
        raise HTTPException(status_code=400, detail="아이디어를 입력해 주세요.")

    try:
        result = pm_app.invoke({"user_idea": payload.idea})
        rtm = result.get("final_rtm", {})
        return AnalyzeResponse(requirements=rtm.get("requirements", []))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── SA 엔드포인트 ─────────────────────────────────────────────────────
@app.post("/api/design-architecture", response_model=SAResponse)
async def design_architecture():
    """PROJECT_STATE.md를 읽어 SA 에이전트를 실행하고 아키텍처 설계 결과를 반환합니다."""
    try:
        # PROJECT_STATE.md에서 요구사항 읽기
        md_content = read_project_state()
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail="PROJECT_STATE.md를 찾을 수 없습니다. 먼저 PM 분석을 실행해 주세요.",
        )

    try:
        # MD 파일에서 요구사항 파싱 (테이블 행 추출)
        requirements = _parse_requirements_from_md(md_content)
        if not requirements:
            raise HTTPException(status_code=400, detail="요구사항이 비어 있습니다.")

        result = sa_app.invoke({"requirements": requirements})
        sa = result.get("final_sa", {})
        return SAResponse(
            architecture=sa.get("architecture", {}),
            dependencies=sa.get("dependencies", []),
            execution_order=sa.get("execution_order", []),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _parse_requirements_from_md(md_content: str) -> list[dict]:
    """PROJECT_STATE.md의 Markdown 테이블에서 요구사항을 파싱합니다."""
    import re
    requirements = []
    # 테이블 행 패턴: | REQ_xxx | title | desc | priority |
    pattern = re.compile(
        r"^\|\s*(REQ_\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|",
        re.MULTILINE,
    )
    for match in pattern.finditer(md_content):
        requirements.append({
            "req_id": match.group(1).strip(),
            "title": match.group(2).strip(),
            "description": match.group(3).strip(),
            "priority": match.group(4).strip() or None,
        })
    return requirements


@app.get("/health")
async def health():
    return {"status": "ok"}

