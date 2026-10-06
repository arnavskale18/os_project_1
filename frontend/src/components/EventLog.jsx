import React, { useRef, useEffect } from 'react';
import { Terminal } from 'lucide-react';

export default function EventLog({ events }) {
  const logEndRef = useRef(null);

  const getEventBadge = (type) => {
    switch (type) {
      case 'REQUEST':
        return <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30">REQUEST</span>;
      case 'SAFE':
        return <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">SAFE</span>;
      case 'UNSAFE':
        return <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30">UNSAFE</span>;
      case 'GRANT':
        return <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-500 text-slate-950">GRANT</span>;
      case 'RANKING':
        return <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">RANKING</span>;
      case 'RELEASE':
        return <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-purple-500/20 text-purple-400 border border-purple-500/30">RELEASE</span>;
      case 'COMPLETE':
        return <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300">COMPLETE</span>;
      default:
        return <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-400">{type}</span>;
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Terminal className="w-4 h-4 text-emerald-400" />
          Simulation Event Log
        </h2>
        <span className="text-xs text-slate-500 font-mono">{events.length} Events</span>
      </div>

      <div className="bg-slate-950 rounded-lg p-3 border border-slate-800 h-64 overflow-y-auto font-mono text-xs space-y-2">
        {events && events.length > 0 ? (
          events.slice().reverse().map((ev, idx) => (
            <div key={idx} className="flex items-start gap-2.5 border-b border-slate-900 pb-1.5 hover:bg-slate-900/50 p-1 rounded">
              <span className="text-slate-500 text-[10px] min-w-[50px]">Tick {ev.tick}</span>
              <div className="flex-shrink-0">{getEventBadge(ev.event_type)}</div>
              {ev.pid && <span className="text-emerald-400 font-bold min-w-[30px]">{ev.pid}</span>}
              <span className="text-slate-300 flex-1 break-words">{ev.message}</span>
            </div>
          ))
        ) : (
          <div className="text-slate-600 text-center py-10">No events logged yet.</div>
        )}
        <div ref={logEndRef} />
      </div>
    </div>
  );
}
