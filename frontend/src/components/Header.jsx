import React from 'react';
import { Play, Pause, StepForward, RotateCcw, ShieldCheck, Activity, BarChart2 } from 'lucide-react';

export default function Header({
  state,
  activeTab,
  setActiveTab,
  onStart,
  onPause,
  onStep,
  onReset,
  onScenarioChange,
  onAlgorithmChange,
  speedMs,
  setSpeedMs
}) {
  return (
    <header className="bg-slate-900 border-b border-slate-800 sticky top-0 z-50 px-6 py-4 shadow-lg">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Title & Badge */}
        <div className="flex items-center space-x-3">
          <div className="bg-emerald-500/10 p-2.5 rounded-xl border border-emerald-500/30">
            <ShieldCheck className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
              Adaptive Banker's Simulator
              <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono border border-emerald-500/30">
                Academic Edition
              </span>
            </h1>
            <p className="text-xs text-slate-400">Deadlock Avoidance with EWMA Demand Estimation & Starvation-Aware Ranking</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('simulator')}
            className={`flex items-center space-x-2 px-4 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'simulator'
                ? 'bg-emerald-600 text-white shadow-md'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Activity className="w-3.5 h-3.5" />
            <span>Interactive Simulator</span>
          </button>
          <button
            onClick={() => setActiveTab('comparison')}
            className={`flex items-center space-x-2 px-4 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'comparison'
                ? 'bg-emerald-600 text-white shadow-md'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <BarChart2 className="w-3.5 h-3.5" />
            <span>Classical vs Adaptive Benchmark</span>
          </button>
        </div>

        {/* Controls Bar */}
        <div className="flex items-center space-x-3">
          {/* Scenario Select */}
          <div className="flex flex-col">
            <label className="text-[10px] text-slate-400 uppercase font-semibold">Scenario</label>
            <select
              value={state.scenario}
              onChange={(e) => onScenarioChange(e.target.value)}
              className="bg-slate-800 text-xs text-slate-200 border border-slate-700 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-emerald-500"
            >
              <option value="STARVATION">Starvation Demo</option>
              <option value="NORMAL">Normal Workload</option>
              <option value="HIGH_CONTENTION">High Contention</option>
              <option value="DYNAMIC_DEMAND">Dynamic Demand</option>
            </select>
          </div>

          {/* Algorithm Toggle */}
          <div className="flex flex-col">
            <label className="text-[10px] text-slate-400 uppercase font-semibold">Policy</label>
            <select
              value={state.algorithm}
              onChange={(e) => onAlgorithmChange(e.target.value)}
              className="bg-slate-800 text-xs font-semibold text-emerald-400 border border-slate-700 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-emerald-500"
            >
              <option value="ADAPTIVE">Adaptive Banker</option>
              <option value="CLASSICAL">Classical Banker</option>
            </select>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-1.5 pt-3">
            {state.is_running ? (
              <button
                onClick={onPause}
                className="bg-amber-500/20 text-amber-400 hover:bg-amber-500/30 border border-amber-500/40 p-2 rounded-lg text-xs font-semibold transition"
                title="Pause Simulation"
              >
                <Pause className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={onStart}
                className="bg-emerald-600 hover:bg-emerald-500 text-white p-2 rounded-lg text-xs font-semibold transition shadow-lg shadow-emerald-900/30"
                title="Start Simulation"
              >
                <Play className="w-4 h-4" />
              </button>
            )}

            <button
              onClick={onStep}
              disabled={state.is_running}
              className="bg-indigo-600/20 text-indigo-400 hover:bg-indigo-600/30 border border-indigo-500/40 p-2 rounded-lg text-xs font-semibold transition disabled:opacity-40"
              title="Step 1 Tick"
            >
              <StepForward className="w-4 h-4" />
            </button>

            <button
              onClick={onReset}
              className="bg-slate-800 hover:bg-slate-700 text-slate-300 p-2 rounded-lg text-xs font-semibold transition border border-slate-700"
              title="Reset Simulation"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>

          {/* Simulation Tick Badge */}
          <div className="bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800 text-center font-mono">
            <span className="text-[10px] text-slate-500 uppercase block">Tick</span>
            <span className="text-sm font-bold text-emerald-400">{state.tick}</span>
          </div>
        </div>
      </div>
    </header>
  );
}
