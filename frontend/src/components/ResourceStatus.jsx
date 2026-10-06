import React from 'react';
import { Cpu } from 'lucide-react';

export default function ResourceStatus({ totalResources, availableResources, resourceNames }) {
  const names = resourceNames && resourceNames.length ? resourceNames : ["R1", "R2", "R3"];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Cpu className="w-4 h-4 text-emerald-400" />
          Resource Status
        </h2>
        <span className="text-xs text-slate-400 font-mono">Available / Total</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {names.map((name, idx) => {
          const total = totalResources[idx] || 1;
          const available = availableResources[idx] !== undefined ? availableResources[idx] : total;
          const allocated = total - available;
          const pct = Math.round((allocated / total) * 100);

          return (
            <div key={name} className="bg-slate-950 p-4 rounded-lg border border-slate-800">
              <div className="flex justify-between items-center mb-1.5">
                <span className="text-xs font-bold text-slate-300 font-mono">{name}</span>
                <span className="text-xs font-mono font-bold text-emerald-400">
                  {available} <span className="text-slate-500">/ {total} Free</span>
                </span>
              </div>

              {/* Progress bar */}
              <div className="w-full bg-slate-800 h-3 rounded-full overflow-hidden p-0.5 border border-slate-700/50">
                <div
                  className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full transition-all duration-300"
                  style={{ width: `${pct}%` }}
                />
              </div>

              <div className="flex justify-between text-[10px] text-slate-400 mt-1.5 font-mono">
                <span>Allocated: {allocated}</span>
                <span>{pct}% Used</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
