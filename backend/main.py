"""FastAPI 엔트리포인트 — CORS 설정 및 API 라우터."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.pm_graph import pm_app

app = FastAPI(title="PM Agent API", version="0.1.0")

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


# ── 엔드포인트 ────────────────────────────────────────────────────────
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


@app.get("/health")
async def health():
    return {"status": "ok"}
