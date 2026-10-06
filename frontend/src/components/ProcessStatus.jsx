import React from 'react';
import { Layers } from 'lucide-react';

export default function ProcessStatus({ processes }) {
  const getStateBadge = (state) => {
    switch (state) {
      case 'RUNNING':
        return <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">RUNNING</span>;
      case 'WAITING':
        return <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">WAITING</span>;
      case 'READY':
        return <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30">READY</span>;
      case 'COMPLETED':
        return <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-slate-800 text-slate-400 border border-slate-700">COMPLETED</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-slate-800 text-slate-300">{state}</span>;
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Layers className="w-4 h-4 text-emerald-400" />
          Process Status
        </h2>
        <span className="text-xs text-slate-400">{processes.length} Processes</span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <th className="py-2.5 px-3">PID</th>
              <th className="py-2.5 px-3">State</th>
              <th className="py-2.5 px-3">Priority</th>
              <th className="py-2.5 px-3 font-mono">Allocation</th>
              <th className="py-2.5 px-3 font-mono">Need</th>
              <th className="py-2.5 px-3">Wait Time</th>
              <th className="py-2.5 px-3">Aging Score</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-xs font-mono">
            {processes.map((proc) => (
              <tr key={proc.pid} className="hover:bg-slate-800/40 transition">
                <td className="py-3 px-3 font-bold text-slate-200">{proc.pid}</td>
                <td className="py-3 px-3">{getStateBadge(proc.state)}</td>
                <td className="py-3 px-3 font-semibold text-slate-300">P{proc.priority}</td>
                <td className="py-3 px-3 text-emerald-400">[{proc.allocation.join(', ')}]</td>
                <td className="py-3 px-3 text-teal-300">[{proc.need.join(', ')}]</td>
                <td className="py-3 px-3 text-slate-300">
                  {proc.waiting_time} <span className="text-[10px] text-slate-500">ticks</span>
                </td>
                <td className="py-3 px-3">
                  <div className="flex items-center gap-2">
                    <span className={`font-semibold ${proc.aging_score >= 0.7 ? 'text-amber-400 font-bold' : 'text-slate-400'}`}>
                      {proc.aging_score.toFixed(2)}
                    </span>
                    <div className="w-16 bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div
                        className={`h-full ${proc.aging_score >= 0.7 ? 'bg-amber-400' : 'bg-emerald-500'}`}
                        style={{ width: `${Math.min(100, proc.aging_score * 100)}%` }}
                      />
                    </div>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
