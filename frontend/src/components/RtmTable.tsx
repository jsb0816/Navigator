import { type Requirement } from "../api";

interface RtmTableProps {
  requirements: Requirement[];
}

/** MoSCoW 우선순위에 따른 배지 색상  */
function priorityBadge(priority: string | null) {
  const base =
    "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide uppercase";

  switch (priority) {
    case "Must":
      return (
        <span className={`${base} bg-rose-500/20 text-rose-300 ring-1 ring-rose-500/30`}>
          Must
        </span>
      );
    case "Should":
      return (
        <span className={`${base} bg-amber-500/20 text-amber-300 ring-1 ring-amber-500/30`}>
          Should
        </span>
      );
    case "Could":
      return (
        <span className={`${base} bg-emerald-500/20 text-emerald-300 ring-1 ring-emerald-500/30`}>
          Could
        </span>
      );
    case "Won't":
      return (
        <span className={`${base} bg-slate-500/20 text-slate-400 ring-1 ring-slate-500/30`}>
          Won't
        </span>
      );
    default:
      return (
        <span className={`${base} bg-slate-500/20 text-slate-400 ring-1 ring-slate-500/30`}>
          —
        </span>
      );
  }
}

export default function RtmTable({ requirements }: RtmTableProps) {
  if (requirements.length === 0) return null;

  return (
    <div className="animate-fade-in-up overflow-x-auto">
      <table className="w-full text-left border-collapse">
        {/* 헤더 */}
        <thead>
          <tr className="border-b border-white/10">
            <th className="py-3 px-4 text-xs font-semibold text-indigo-300 uppercase tracking-wider">
              ID
            </th>
            <th className="py-3 px-4 text-xs font-semibold text-indigo-300 uppercase tracking-wider">
              Title
            </th>
            <th className="py-3 px-4 text-xs font-semibold text-indigo-300 uppercase tracking-wider max-w-md">
              Description
            </th>
            <th className="py-3 px-4 text-xs font-semibold text-indigo-300 uppercase tracking-wider text-center">
              Priority
            </th>
          </tr>
        </thead>

        {/* 본문 */}
        <tbody>
          {requirements.map((req, idx) => (
            <tr
              key={req.req_id}
              className={`border-b border-white/5 transition-colors duration-200 hover:bg-white/[0.04] ${
                idx % 2 === 0 ? "bg-white/[0.02]" : ""
              }`}
              style={{ animationDelay: `${idx * 60}ms` }}
            >
              <td className="py-3 px-4 text-sm font-mono text-violet-300 whitespace-nowrap">
                {req.req_id}
              </td>
              <td className="py-3 px-4 text-sm text-white/90 font-medium">
                {req.title}
              </td>
              <td className="py-3 px-4 text-sm text-white/60 max-w-md">
                {req.description}
              </td>
              <td className="py-3 px-4 text-center">{priorityBadge(req.priority)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
