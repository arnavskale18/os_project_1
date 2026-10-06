import React, { useState } from 'react';
import { Sliders, CheckCircle2, XCircle, ArrowRight, ChevronDown } from 'lucide-react';
import { api } from '../services/api';

export default function ManualRequestPanel({ processes, resourceNames }) {
  const [selectedPid, setSelectedPid] = useState(processes[0]?.pid || 'P1');
  const [requestInputs, setRequestInputs] = useState({ r0: 1, r1: 0, r2: 1 });
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const names = resourceNames && resourceNames.length ? resourceNames : ["R1", "R2", "R3"];

  const handleEvaluate = async () => {
    setLoading(true);
    try {
      const requestVec = [
        parseInt(requestInputs.r0) || 0,
        parseInt(requestInputs.r1) || 0,
        parseInt(requestInputs.r2) || 0,
      ];
      const res = await api.evaluateRequest(selectedPid, requestVec);
      setEvaluationResult(res.evaluation);
    } catch (err) {
      console.error("Evaluation failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Sliders className="w-4 h-4 text-emerald-400" />
          Manual Request Evaluation (Demonstration Mode)
        </h2>
        <span className="text-xs text-slate-400 font-mono">Test arbitrary process requests</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-3 items-end mb-4">
        <div className="md:col-span-2">
          <label className="text-[11px] text-slate-400 uppercase font-semibold block mb-1">
            Target Process
          </label>
          <div className="relative">
            <select
              value={selectedPid}
              onChange={(e) => setSelectedPid(e.target.value)}
              className="w-full bg-slate-950 text-xs text-slate-200 border border-slate-700/80 rounded-lg px-3 py-2 font-mono appearance-none focus:outline-none focus:border-emerald-500 cursor-pointer pr-8"
            >
              {processes.map((p) => (
                <option key={p.pid} value={p.pid} className="bg-slate-900 text-slate-200 py-1">
                  {p.pid} (Priority {p.priority}) {p.need ? `[Need: ${p.need.join(',')}]` : ''}
                </option>
              ))}
            </select>
            <ChevronDown className="w-4 h-4 text-slate-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>

        {names.map((name, idx) => (
          <div key={name} className="md:col-span-1">
            <label className="text-[11px] text-slate-400 uppercase font-semibold block mb-1">{name} Amount</label>
            <input
              type="number"
              min="0"
              max="20"
              value={requestInputs[`r${idx}`] ?? 0}
              onChange={(e) => setRequestInputs({ ...requestInputs, [`r${idx}`]: e.target.value })}
              className="w-full bg-slate-950 text-xs text-slate-200 border border-slate-700/80 rounded-lg px-3 py-2 font-mono focus:outline-none focus:border-emerald-500"
            />
          </div>
        ))}
      </div>

      <button
        onClick={handleEvaluate}
        disabled={loading}
        className="w-full bg-emerald-600 hover:bg-emerald-500 text-white py-2 rounded-lg text-xs font-semibold transition flex items-center justify-center gap-2 shadow-md shadow-emerald-950/20 active:scale-[0.99]"
      >
        {loading ? "Evaluating Banker Safety..." : "Evaluate Request"}
      </button>

      {/* Result Display */}
      {evaluationResult && (
        <div className="mt-4 pt-4 border-t border-slate-800 font-mono text-xs space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-slate-400">Target Process: <strong className="text-slate-200">{selectedPid}</strong></span>
            {evaluationResult.is_safe ? (
              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30">
                <CheckCircle2 className="w-3.5 h-3.5" /> BANKER SAFE
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-rose-500/20 text-rose-400 font-bold border border-rose-500/30">
                <XCircle className="w-3.5 h-3.5" /> BANKER UNSAFE / REJECTED
              </span>
            )}
          </div>

          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1.5 text-slate-300">
            <div><span className="text-slate-500">Reason:</span> {evaluationResult.reason}</div>

            {evaluationResult.is_safe && evaluationResult.safe_sequence && (
              <div className="flex items-center gap-2 pt-1 border-t border-slate-900">
                <span className="text-slate-500">Safe Sequence:</span>
                <span className="text-emerald-400 font-bold">
                  {evaluationResult.safe_sequence.join(' -> ')}
                </span>
              </div>
            )}

            {evaluationResult.total_score > 0 && (
              <div className="flex items-center gap-2 pt-1 border-t border-slate-900">
                <span className="text-slate-500">Calculated Adaptive Score:</span>
                <span className="text-amber-400 font-bold">{evaluationResult.total_score.toFixed(2)}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
