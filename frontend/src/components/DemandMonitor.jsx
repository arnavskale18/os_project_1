import React from 'react';
import { TrendingUp } from 'lucide-react';

export default function DemandMonitor({ processes, alpha, safetyMargin }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-emerald-400" />
          Runtime Demand Estimator (EWMA)
        </h2>
        <span className="text-xs text-slate-400 font-mono">
          &alpha; = {alpha} | Margin = +{safetyMargin}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {processes.map((proc) => {
          const hasHistory = proc.request_history && proc.request_history.length > 0;
          const predicted = proc.predicted_demand || [];
          const estimated = proc.estimated_demand || [];

          return (
            <div key={proc.pid} className="bg-slate-950 p-3.5 rounded-lg border border-slate-800 font-mono text-xs">
              <div className="flex justify-between items-center mb-2 pb-1.5 border-b border-slate-800">
                <span className="font-bold text-slate-200">{proc.pid}</span>
                <span className="text-[10px] text-slate-500">
                  {proc.request_history ? proc.request_history.length : 0} Requests Observed
                </span>
              </div>

              {hasHistory ? (
                <div className="space-y-1.5">
                  <div className="flex justify-between text-slate-400 text-[11px]">
                    <span>Observed Last:</span>
                    <span className="text-emerald-400 font-bold">
                      [{proc.request_history[proc.request_history.length - 1].join(', ')}]
                    </span>
                  </div>

                  <div className="flex justify-between text-slate-400 text-[11px]">
                    <span>EWMA Prediction:</span>
                    <span className="text-amber-400 font-bold">
                      [{predicted.map(v => v.toFixed(1)).join(', ')}]
                    </span>
                  </div>

                  <div className="flex justify-between text-slate-400 text-[11px] pt-1 border-t border-slate-800/80">
                    <span>Est. Demand (+{safetyMargin}):</span>
                    <span className="text-teal-300 font-bold">
                      [{estimated.join(', ')}]
                    </span>
                  </div>
                </div>
              ) : (
                <div className="text-slate-600 text-[11px] py-2 text-center">
                  No requests recorded yet
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
