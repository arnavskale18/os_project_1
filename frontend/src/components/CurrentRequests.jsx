import React from 'react';
import { GitPullRequest, CheckCircle2, XCircle, Award } from 'lucide-react';

export default function CurrentRequests({ candidates, lastSelection, algorithm }) {
  if (!candidates || candidates.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
        <h2 className="text-sm font-semibold text-slate-200 flex items-center gap-2 mb-3">
          <GitPullRequest className="w-4 h-4 text-emerald-400" />
          Current Requests
        </h2>
        <div className="text-xs text-slate-500 py-6 text-center border border-dashed border-slate-800 rounded-lg">
          No pending resource requests at current tick.
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <GitPullRequest className="w-4 h-4 text-emerald-400" />
          Current Requests & Candidate Set
        </h2>
        <span className="text-xs text-slate-400 font-mono">
          Policy: <span className="text-emerald-400 font-bold">{algorithm}</span>
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <th className="py-2.5 px-3">PID</th>
              <th className="py-2.5 px-3 font-mono">Request</th>
              <th className="py-2.5 px-3">Banker Safety</th>
              {algorithm === 'ADAPTIVE' && <th className="py-2.5 px-3">Ranking Score</th>}
              <th className="py-2.5 px-3">Decision</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-xs font-mono">
            {candidates.map((cand) => {
              const isSelected = cand.selected || (lastSelection && lastSelection.pid === cand.pid && lastSelection.is_safe);

              return (
                <tr
                  key={cand.pid}
                  className={`transition ${isSelected ? 'bg-emerald-950/40 border-l-2 border-emerald-500' : 'hover:bg-slate-800/40'}`}
                >
                  <td className="py-3 px-3 font-bold text-slate-200 flex items-center gap-1.5">
                    {cand.pid}
                    {isSelected && <Award className="w-3.5 h-3.5 text-amber-400 inline" />}
                  </td>

                  <td className="py-3 px-3 text-emerald-400">[{cand.request.join(', ')}]</td>

                  <td className="py-3 px-3">
                    {cand.is_safe ? (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                        <CheckCircle2 className="w-3 h-3" /> SAFE
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30">
                        <XCircle className="w-3 h-3" /> UNSAFE
                      </span>
                    )}
                  </td>

                  {algorithm === 'ADAPTIVE' && (
                    <td className="py-3 px-3 font-bold text-amber-400">
                      {cand.is_safe ? cand.total_score.toFixed(2) : '--'}
                    </td>
                  )}

                  <td className="py-3 px-3 font-semibold">
                    {isSelected ? (
                      <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500 text-slate-950">
                        SELECTED
                      </span>
                    ) : cand.is_safe ? (
                      <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-blue-500/20 text-blue-300 border border-blue-500/30">
                        Candidate
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-800 text-slate-400">
                        Deferred
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
