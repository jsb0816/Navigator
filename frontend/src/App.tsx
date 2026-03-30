import { useState } from "react";
import {
  analyzeIdea,
  designArchitecture,
  type Requirement,
  type SAResponse,
} from "./api";
import RtmTable from "./components/RtmTable";
import ArchitectureView from "./components/ArchitectureView";

export default function App() {
  // ── PM 상태 ─────────────────────────────────────────────────────
  const [idea, setIdea] = useState("");
  const [requirements, setRequirements] = useState<Requirement[]>([]);
  const [pmLoading, setPmLoading] = useState(false);
  const [pmError, setPmError] = useState<string | null>(null);

  // ── SA 상태 ─────────────────────────────────────────────────────
  const [saResult, setSaResult] = useState<SAResponse | null>(null);
  const [saLoading, setSaLoading] = useState(false);
  const [saError, setSaError] = useState<string | null>(null);

  // ── 탭 ──────────────────────────────────────────────────────────
  const [activeTab, setActiveTab] = useState<"pm" | "sa">("pm");

  const handleAnalyze = async () => {
    if (!idea.trim()) return;
    setPmLoading(true);
    setPmError(null);
    setRequirements([]);
    setSaResult(null);

    try {
      const data = await analyzeIdea(idea);
      setRequirements(data.requirements);
    } catch (err) {
      setPmError(
        err instanceof Error ? err.message : "알 수 없는 오류가 발생했습니다."
      );
    } finally {
      setPmLoading(false);
    }
  };

  const handleDesignArch = async () => {
    setSaLoading(true);
    setSaError(null);
    setSaResult(null);
    setActiveTab("sa");

    try {
      const data = await designArchitecture();
      setSaResult(data);
    } catch (err) {
      setSaError(
        err instanceof Error
          ? err.message
          : "SA 분석 중 오류가 발생했습니다."
      );
    } finally {
      setSaLoading(false);
    }
  };

  const pmDone = requirements.length > 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white">
      {/* ── 헤더 ─────────────────────────────────────────────────── */}
      <header className="pt-10 pb-6 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight gradient-text mb-2">
          🛠️ SDLC Pipeline
        </h1>
        <p className="text-white/50 text-sm md:text-base max-w-xl mx-auto">
          PM → SA · 아이디어를 입력하면 AI가 요구사항 분석과 아키텍처 설계를
          자동으로 수행합니다
        </p>
      </header>

      {/* ── 메인 컨텐츠 ─────────────────────────────────────────── */}
      <main className="max-w-7xl mx-auto px-4 pb-20 grid gap-8 lg:grid-cols-[1fr_1.8fr]">
        {/* ── 좌측: 입력 & 컨트롤 ───────────────────────────────── */}
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
              rows={8}
              className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-sm text-white/90 placeholder-white/25 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-shadow"
              placeholder="예: 대학생을 위한 중고 교재 거래 플랫폼을 만들고 싶어요. 사용자 간 채팅, 가격 비교, 위치 기반 거래 기능이 필요합니다…"
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              disabled={pmLoading || saLoading}
            />
          </div>

          {/* PM 분석 버튼 */}
          <button
            id="analyze-btn"
            onClick={handleAnalyze}
            disabled={pmLoading || saLoading || !idea.trim()}
            className="btn-glow w-full py-3 rounded-xl font-semibold text-sm tracking-wide bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-300 cursor-pointer"
          >
            {pmLoading
              ? "🔄 PM 분석 중… (약 15~30초)"
              : "🚀 1단계: 요구사항 분석 (PM)"}
          </button>

          {/* SA 설계 버튼 — PM 완료 후 활성화 */}
          <button
            id="sa-btn"
            onClick={handleDesignArch}
            disabled={!pmDone || pmLoading || saLoading}
            className="btn-glow w-full py-3 rounded-xl font-semibold text-sm tracking-wide bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-500 hover:to-emerald-500 disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-300 cursor-pointer"
          >
            {saLoading
              ? "🔄 SA 분석 중… (약 60초 소요)"
              : "🏗️ 2단계: 아키텍처 설계 (SA)"}
          </button>

          {/* 에러 메시지 */}
          {(pmError || saError) && (
            <div className="animate-fade-in-up bg-rose-500/10 border border-rose-500/30 rounded-lg px-4 py-3 text-sm text-rose-300">
              ⚠️ {pmError || saError}
            </div>
          )}
        </section>

        {/* ── 우측: 결과 영역 (탭 전환) ─────────────────────────── */}
        <section className="glass-card p-6 min-h-[400px] flex flex-col">
          {/* 탭 바 */}
          <div className="flex gap-1 mb-5 bg-white/5 rounded-lg p-1">
            <button
              onClick={() => setActiveTab("pm")}
              className={`flex-1 py-2 rounded-md text-xs font-semibold tracking-wide transition-all cursor-pointer ${
                activeTab === "pm"
                  ? "bg-indigo-600/60 text-white shadow-lg shadow-indigo-500/20"
                  : "text-white/40 hover:text-white/60"
              }`}
            >
              📊 PM — 요구사항
              {pmDone && (
                <span className="ml-1.5 px-1.5 py-0.5 rounded-full bg-indigo-500/30 text-[10px]">
                  {requirements.length}
                </span>
              )}
            </button>
            <button
              onClick={() => setActiveTab("sa")}
              disabled={!pmDone}
              className={`flex-1 py-2 rounded-md text-xs font-semibold tracking-wide transition-all cursor-pointer ${
                activeTab === "sa"
                  ? "bg-teal-600/60 text-white shadow-lg shadow-teal-500/20"
                  : "text-white/40 hover:text-white/60 disabled:opacity-30 disabled:cursor-not-allowed"
              }`}
            >
              🏗️ SA — 아키텍처
              {saResult && (
                <span className="ml-1.5 px-1.5 py-0.5 rounded-full bg-teal-500/30 text-[10px]">
                  ✓
                </span>
              )}
            </button>
          </div>

          {/* ── PM 탭 콘텐츠 ───────────────────────────────────── */}
          {activeTab === "pm" && (
            <>
              <h2 className="text-xs font-semibold text-indigo-300 uppercase tracking-wider mb-4">
                📊 Requirements Traceability Matrix
              </h2>

              {pmLoading && (
                <div className="flex-1 flex flex-col items-center justify-center gap-4 animate-fade-in-up">
                  <div className="w-12 h-12 rounded-full border-4 border-indigo-500/30 border-t-indigo-400 spinner" />
                  <p className="text-white/40 text-sm">
                    AI가 요구사항을 분석하고 있습니다…
                  </p>
                </div>
              )}

              {!pmLoading && pmDone && (
                <>
                  <RtmTable requirements={requirements} />
                  <p className="mt-4 text-xs text-white/30 text-right">
                    총 {requirements.length}개 요구사항 추출됨 ·
                    PROJECT_STATE.md 저장 완료
                  </p>
                </>
              )}

              {!pmLoading && !pmDone && !pmError && (
                <div className="flex-1 flex items-center justify-center">
                  <p className="text-white/20 text-sm text-center">
                    좌측에 아이디어를 입력한 뒤
                    <br />
                    <strong>1단계: 요구사항 분석</strong> 버튼을 누르세요
                  </p>
                </div>
              )}
            </>
          )}

          {/* ── SA 탭 콘텐츠 ───────────────────────────────────── */}
          {activeTab === "sa" && (
            <>
              <h2 className="text-xs font-semibold text-teal-300 uppercase tracking-wider mb-4">
                🏗️ Architecture & Execution Order
              </h2>

              {saLoading && (
                <div className="flex-1 flex flex-col items-center justify-center gap-4 animate-fade-in-up">
                  <div className="w-12 h-12 rounded-full border-4 border-teal-500/30 border-t-teal-400 spinner" />
                  <p className="text-white/40 text-sm">
                    AI가 아키텍처를 설계하고 있습니다…
                  </p>
                  <p className="text-white/25 text-xs">
                    Rate Limit 방지를 위해 노드 간 20초 딜레이가 있습니다
                  </p>
                </div>
              )}

              {!saLoading && saResult && (
                <>
                  <ArchitectureView
                    architecture={saResult.architecture}
                    dependencies={saResult.dependencies}
                    executionOrder={saResult.execution_order}
                  />
                  <p className="mt-4 text-xs text-white/30 text-right">
                    {saResult.execution_order.length}개 요구사항 정렬됨 ·
                    PROJECT_STATE.md 업데이트 완료
                  </p>
                </>
              )}

              {!saLoading && !saResult && !saError && (
                <div className="flex-1 flex items-center justify-center">
                  <p className="text-white/20 text-sm text-center">
                    좌측의{" "}
                    <strong>2단계: 아키텍처 설계(SA)</strong> 버튼을
                    누르세요
                  </p>
                </div>
              )}
            </>
          )}
        </section>
      </main>

      {/* ── 푸터 ────────────────────────────────────────────────── */}
      <footer className="fixed bottom-0 inset-x-0 py-3 text-center text-xs text-white/20 bg-black/20 backdrop-blur-sm">
        SDLC Pipeline · PM → SA · Powered by LangGraph + Gemini 2.5 Flash
      </footer>
    </div>
  );
}
