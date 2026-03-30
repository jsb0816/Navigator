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
