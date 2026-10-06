import React from 'react';
import { HelpCircle, CheckCircle2, ArrowRight, Award, ShieldAlert } from 'lucide-react';

export default function SelectionExplanation({ lastSelection, algorithm }) {
  if (!lastSelection) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
        <h2 className="text-sm font-semibold text-slate-200 flex items-center gap-2 mb-3">
          <HelpCircle className="w-4 h-4 text-emerald-400" />
          Allocation Decision Rationale
        </h2>
        <div className="text-xs text-slate-500 py-6 text-center border border-dashed border-slate-800 rounded-lg">
          No allocation decision made in current tick.
        </div>
      </div>
    );
  }

  const { pid, request, safe_sequence, scores, total_score, reason } = lastSelection;

  return (
    <div className="bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 border border-emerald-500/30 rounded-xl p-5 shadow-lg">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <h2 className="text-sm font-bold text-emerald-400 flex items-center gap-2">
          <Award className="w-4 h-4 text-amber-400" />
          WHY WAS {pid} SELECTED?
        </h2>
        <span className="text-xs font-mono font-bold text-slate-300 bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-1 rounded-lg">
          Score: {total_score ? total_score.toFixed(2) : 'SAFE'}
        </span>
      </div>

      {/* Safety Verification Badge */}
      <div className="flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-3 mb-4 text-xs font-mono text-emerald-300">
        <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
        <span>Banker Safety Test PASSED for request [{request.join(', ')}]</span>
      </div>

      {/* Safe Sequence Display */}
      <div className="mb-4">
        <label className="text-[11px] text-slate-400 uppercase font-semibold block mb-1.5 font-mono">
          Safe Execution Path:
        </label>
        <div className="flex flex-wrap items-center gap-2 bg-slate-950 p-3 rounded-lg border border-slate-800 font-mono text-xs">
          {safe_sequence && safe_sequence.length > 0 ? (
            safe_sequence.map((p, idx) => (
              <React.Fragment key={p}>
                <span className={`px-2.5 py-1 rounded-md font-bold ${p === pid ? 'bg-emerald-600 text-white' : 'bg-slate-800 text-slate-300'}`}>
                  {p}
                </span>
                {idx < safe_sequence.length - 1 && (
                  <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
                )}
              </React.Fragment>
            ))
          ) : (
            <span className="text-slate-500">None</span>
          )}
        </div>
      </div>

      {/* Score Breakdown Grid */}
      {algorithm === 'ADAPTIVE' && scores && (
        <div className="mb-4">
          <label className="text-[11px] text-slate-400 uppercase font-semibold block mb-2 font-mono">
            Starvation-Aware Score Breakdown:
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs font-mono">
            <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
              <span className="text-[10px] text-slate-400 block">Waiting (40%)</span>
              <span className="text-sm font-bold text-amber-400">{scores.waiting_score ?? 0}</span>
            </div>
            <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
              <span className="text-[10px] text-slate-400 block">Priority (20%)</span>
              <span className="text-sm font-bold text-blue-400">{scores.priority_score ?? 0}</span>
            </div>
            <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
              <span className="text-[10px] text-slate-400 block">Efficiency (20%)</span>
              <span className="text-sm font-bold text-teal-400">{scores.efficiency_score ?? 0}</span>
            </div>
            <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
              <span className="text-[10px] text-slate-400 block">Aging (20%)</span>
              <span className="text-sm font-bold text-rose-400">{scores.aging_score ?? 0}</span>
            </div>
          </div>
        </div>
      )}

      {/* Rationale explanation text */}
      <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs text-slate-300">
        <span className="font-semibold text-emerald-400 block mb-1 font-mono">Decision Rationale:</span>
        <p className="leading-relaxed">
          {algorithm === 'ADAPTIVE'
            ? `${pid} was selected because it passed the mandatory Banker's safety test and achieved the highest composite Starvation-Aware score (${total_score.toFixed(2)}) among all safe candidate requests.`
            : `${pid} was selected as the first safe candidate under Classical Banker's Algorithm FCFS policy.`}
        </p>
      </div>
    </div>
  );
}
