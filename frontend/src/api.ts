/**
 * FastAPI 백엔드 통신 모듈
 */

const API_BASE = "http://localhost:8000";

export interface Requirement {
  req_id: string;
  title: string;
  description: string;
  priority: string | null;
}

export interface AnalyzeResponse {
  requirements: Requirement[];
}

// ── SA 관련 타입 ─────────────────────────────────────────────────

export interface ArchitectureDecision {
  frontend: string;
  backend: string;
  database: string;
  design_pattern: string;
  reasoning: string;
}

export interface DependencyItem {
  req_id: string;
  depends_on: string[];
}

export interface SAResponse {
  architecture: ArchitectureDecision;
  dependencies: DependencyItem[];
  execution_order: string[];
}

// ── API 함수 ─────────────────────────────────────────────────────

/**
 * 사용자 아이디어를 분석하여 RTM을 반환합니다.
 */
export async function analyzeIdea(idea: string): Promise<AnalyzeResponse> {
  const response = await fetch(`${API_BASE}/api/analyze-idea`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ idea }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(
      errorData?.detail || `서버 오류가 발생했습니다 (${response.status})`
    );
  }

  return response.json();
}

/**
 * PROJECT_STATE.md 기반으로 SA 에이전트를 실행하여 아키텍처 설계 결과를 반환합니다.
 */
export async function designArchitecture(): Promise<SAResponse> {
  const response = await fetch(`${API_BASE}/api/design-architecture`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(
      errorData?.detail || `SA 분석 중 오류가 발생했습니다 (${response.status})`
    );
  }

  return response.json();
}

