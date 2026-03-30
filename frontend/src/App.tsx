import { useState } from "react";
import { analyzeIdea, type Requirement } from "./api";
import RtmTable from "./components/RtmTable";

export default function App() {
  const [idea, setIdea] = useState("");
  const [requirements, setRequirements] = useState<Requirement[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!idea.trim()) return;
    setLoading(true);
    setError(null);
    setRequirements([]);

    try {
      const data = await analyzeIdea(idea);
      setRequirements(data.requirements);
    } catch (err) {
      setError(err instanceof Error ? err.message : "알 수 없는 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white">
      {/* ── 헤더 ─────────────────────────────────────────────────── */}
      <header className="pt-10 pb-6 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight gradient-text mb-2">
          🛠️ PM Agent
        </h1>
        <p className="text-white/50 text-sm md:text-base max-w-xl mx-auto">
          아이디어를 입력하면 AI가 자동으로 요구사항 분석(RTM)을 수행합니다
        </p>
      </header>

      {/* ── 메인 컨텐츠 ─────────────────────────────────────────── */}
      <main className="max-w-6xl mx-auto px-4 pb-20 grid gap-8 lg:grid-cols-[1fr_1.5fr]">
        {/* 좌측: 입력 영역 */}
        <section className="glass-card p-6 flex flex-col gap-5 h-fit">
          <div>
            <label
              htmlFor="idea-input"
              className="block text-xs font-semibold text-indigo-300 uppercase tracking-wider mb-2"
            >
              💡 프로젝트 아이디어
            </label>
            <textarea
              id="idea-input"
              rows={10}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-sm text-white/90 placeholder-white/25 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-shadow"
              placeholder="예: 대학생을 위한 중고 교재 거래 플랫폼을 만들고 싶어요. 사용자 간 채팅, 가격 비교, 위치 기반 거래 기능이 필요합니다…"
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              disabled={loading}
            />
          </div>

          <button
            id="analyze-btn"
            onClick={handleAnalyze}
            disabled={loading || !idea.trim()}
            className="btn-glow w-full py-3 rounded-xl font-semibold text-sm tracking-wide bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-300 cursor-pointer"
          >
            {loading ? "🔄 분석 중… (약 15~30초 소요)" : "🚀 분석 시작"}
          </button>

          {/* 에러 메시지 */}
          {error && (
            <div className="animate-fade-in-up bg-rose-500/10 border border-rose-500/30 rounded-lg px-4 py-3 text-sm text-rose-300">
              ⚠️ {error}
            </div>
          )}
        </section>

        {/* 우측: 결과 영역 */}
        <section className="glass-card p-6 min-h-[300px] flex flex-col">
          <h2 className="text-xs font-semibold text-indigo-300 uppercase tracking-wider mb-4">
            📊 분석 결과 — Requirements Traceability Matrix
          </h2>

          {/* 로딩 스피너 */}
          {loading && (
            <div className="flex-1 flex flex-col items-center justify-center gap-4 animate-fade-in-up">
              <div className="w-12 h-12 rounded-full border-4 border-indigo-500/30 border-t-indigo-400 spinner" />
              <p className="text-white/40 text-sm">AI가 요구사항을 분석하고 있습니다…</p>
              <p className="text-white/25 text-xs">
                Gemini API Rate Limit 방지를 위해 노드 간 5초 딜레이가 있습니다
              </p>
            </div>
          )}

          {/* 결과 테이블 */}
          {!loading && requirements.length > 0 && (
            <>
              <RtmTable requirements={requirements} />
              <p className="mt-4 text-xs text-white/30 text-right">
                총 {requirements.length}개 요구사항 추출됨 · PROJECT_STATE.md 저장 완료
              </p>
            </>
          )}

          {/* 빈 상태 */}
          {!loading && requirements.length === 0 && !error && (
            <div className="flex-1 flex items-center justify-center">
              <p className="text-white/20 text-sm text-center">
                좌측에 아이디어를 입력한 뒤<br />
                <strong>분석 시작</strong> 버튼을 누르세요
              </p>
            </div>
          )}
        </section>
      </main>

      {/* ── 푸터 ────────────────────────────────────────────────── */}
      <footer className="fixed bottom-0 inset-x-0 py-3 text-center text-xs text-white/20 bg-black/20 backdrop-blur-sm">
        PM Agent · Powered by LangGraph + Gemini 2.5 Flash
      </footer>
    </div>
  );
}
