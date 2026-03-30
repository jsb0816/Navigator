import type { ArchitectureDecision, DependencyItem } from "../api";

interface ArchitectureViewProps {
  architecture: ArchitectureDecision;
  dependencies: DependencyItem[];
  executionOrder: string[];
}

/** 기술 스택 항목별 아이콘 + 색상 */
const STACK_META: Record<string, { emoji: string; gradient: string }> = {
  frontend: { emoji: "🎨", gradient: "from-cyan-500/20 to-blue-500/20" },
  backend: { emoji: "⚙️", gradient: "from-violet-500/20 to-purple-500/20" },
  database: { emoji: "🗄️", gradient: "from-emerald-500/20 to-teal-500/20" },
  design_pattern: { emoji: "🧩", gradient: "from-amber-500/20 to-orange-500/20" },
};

const STACK_LABELS: Record<string, string> = {
  frontend: "Frontend",
  backend: "Backend",
  database: "Database",
  design_pattern: "Design Pattern",
};

export default function ArchitectureView({
  architecture,
  dependencies,
  executionOrder,
}: ArchitectureViewProps) {
  return (
    <div className="space-y-8 animate-fade-in-up">
      {/* ── 기술 스택 카드 그리드 ──────────────────────────────── */}
      <div>
        <h3 className="text-xs font-semibold text-teal-300 uppercase tracking-wider mb-3">
          🏗️ 기술 스택 & 디자인 패턴
        </h3>
        <div className="grid grid-cols-2 gap-3">
          {(["frontend", "backend", "database", "design_pattern"] as const).map(
            (key) => {
              const meta = STACK_META[key];
              const value = architecture[key];
              return (
                <div
                  key={key}
                  className={`bg-gradient-to-br ${meta.gradient} border border-white/10 rounded-xl p-4 transition-transform duration-200 hover:scale-[1.02]`}
                >
                  <p className="text-xs text-white/40 uppercase tracking-wider mb-1">
                    {meta.emoji} {STACK_LABELS[key]}
                  </p>
                  <p className="text-sm font-semibold text-white/90">{value}</p>
                </div>
              );
            }
          )}
        </div>

        {/* 선택 근거 */}
        {architecture.reasoning && (
          <div className="mt-3 bg-white/[0.03] border border-white/5 rounded-lg px-4 py-3">
            <p className="text-xs text-white/30 mb-1">💬 선택 근거</p>
            <p className="text-sm text-white/60 leading-relaxed">
              {architecture.reasoning}
            </p>
          </div>
        )}
      </div>

      {/* ── 개발 순서 타임라인 ─────────────────────────────────── */}
      <div>
        <h3 className="text-xs font-semibold text-teal-300 uppercase tracking-wider mb-3">
          📐 개발 순서 (위상 정렬)
        </h3>
        <div className="relative pl-6">
          {/* 세로 연결선 */}
          <div className="absolute left-[11px] top-2 bottom-2 w-[2px] bg-gradient-to-b from-indigo-500/60 via-purple-500/40 to-transparent" />

          {executionOrder.map((reqId, idx) => {
            // 해당 req의 의존성 정보 찾기
            const dep = dependencies.find((d) => d.req_id === reqId);
            const depText =
              dep && dep.depends_on.length > 0
                ? dep.depends_on.join(", ")
                : null;

            return (
              <div
                key={reqId}
                className="relative flex items-start gap-3 mb-4 last:mb-0 group"
                style={{ animationDelay: `${idx * 80}ms` }}
              >
                {/* 원형 노드 */}
                <div className="relative z-10 flex items-center justify-center w-6 h-6 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 text-[10px] font-bold text-white shadow-lg shadow-indigo-500/30 group-hover:scale-110 transition-transform">
                  {idx + 1}
                </div>

                {/* 내용 */}
                <div className="flex-1 bg-white/[0.04] border border-white/10 rounded-lg px-4 py-2.5 hover:bg-white/[0.07] transition-colors">
                  <p className="text-sm font-mono font-semibold text-violet-300">
                    {reqId}
                  </p>
                  {depText && (
                    <p className="text-xs text-white/30 mt-0.5">
                      ← 의존: {depText}
                    </p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* ── 의존성 DAG 테이블 ──────────────────────────────────── */}
      <div>
        <h3 className="text-xs font-semibold text-teal-300 uppercase tracking-wider mb-3">
          🔗 요구사항 의존성 맵 (DAG)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-white/10">
                <th className="py-2 px-3 text-xs font-semibold text-indigo-300 uppercase tracking-wider">
                  REQ ID
                </th>
                <th className="py-2 px-3 text-xs font-semibold text-indigo-300 uppercase tracking-wider">
                  Depends On
                </th>
              </tr>
            </thead>
            <tbody>
              {dependencies.map((dep, idx) => (
                <tr
                  key={dep.req_id}
                  className={`border-b border-white/5 transition-colors hover:bg-white/[0.04] ${
                    idx % 2 === 0 ? "bg-white/[0.02]" : ""
                  }`}
                >
                  <td className="py-2 px-3 text-sm font-mono text-violet-300">
                    {dep.req_id}
                  </td>
                  <td className="py-2 px-3 text-sm text-white/50">
                    {dep.depends_on.length > 0 ? (
                      dep.depends_on.map((d) => (
                        <span
                          key={d}
                          className="inline-block mr-1.5 mb-1 px-2 py-0.5 rounded-md bg-indigo-500/15 text-indigo-300 text-xs font-mono"
                        >
                          {d}
                        </span>
                      ))
                    ) : (
                      <span className="text-white/20 text-xs">의존성 없음</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
