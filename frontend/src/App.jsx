import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ResourceStatus from './components/ResourceStatus';
import ProcessStatus from './components/ProcessStatus';
import CurrentRequests from './components/CurrentRequests';
import SelectionExplanation from './components/SelectionExplanation';
import DemandMonitor from './components/DemandMonitor';
import EventLog from './components/EventLog';
import ManualRequestPanel from './components/ManualRequestPanel';
import ComparisonDashboard from './components/ComparisonDashboard';
import { api } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('simulator');
  const [simState, setSimState] = useState(null);
  const [speedMs, setSpeedMs] = useState(600);
  const [loading, setLoading] = useState(true);

  // Initial state fetch
  const fetchState = async () => {
    try {
      const state = await api.getState();
      setSimState(state);
    } catch (err) {
      console.error("Failed to fetch simulation state:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchState();
  }, []);

  // Timer loop when simulation is running
  useEffect(() => {
    let timer = null;
    if (simState && simState.is_running) {
      timer = setInterval(async () => {
        try {
          const newState = await api.stepSimulation();
          setSimState(newState);
          // If all processes completed, pause automatically
          const allCompleted = newState.processes.every(p => p.state === 'COMPLETED');
          if (allCompleted) {
            await api.pauseSimulation();
          }
        } catch (err) {
          console.error("Error stepping simulation:", err);
        }
      }, speedMs);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [simState?.is_running, speedMs]);

  const handleStart = async () => {
    const newState = await api.startSimulation();
    setSimState(newState);
  };

  const handlePause = async () => {
    const newState = await api.pauseSimulation();
    setSimState(newState);
  };

  const handleStep = async () => {
    const newState = await api.stepSimulation();
    setSimState(newState);
  };

  const handleReset = async () => {
    const newState = await api.resetSimulation();
    setSimState(newState);
  };

  const handleScenarioChange = async (scenario) => {
    const newState = await api.createSimulation({
      scenario,
      algorithm: simState?.algorithm || 'ADAPTIVE'
    });
    setSimState(newState);
  };

  const handleAlgorithmChange = async (algorithm) => {
    const newState = await api.createSimulation({
      scenario: simState?.scenario || 'STARVATION',
      algorithm
    });
    setSimState(newState);
  };

  if (loading || !simState) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-slate-100">
        <div className="animate-spin w-10 h-10 border-4 border-emerald-500 border-t-transparent rounded-full mb-4" />
        <p className="text-sm font-semibold tracking-wide">Initializing Adaptive Banker Simulation Environment...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 pb-12">
      <Header
        state={simState}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onStart={handleStart}
        onPause={handlePause}
        onStep={handleStep}
        onReset={handleReset}
        onScenarioChange={handleScenarioChange}
        onAlgorithmChange={handleAlgorithmChange}
        speedMs={speedMs}
        setSpeedMs={setSpeedMs}
      />

      <main className="max-w-7xl mx-auto px-6 pt-6">
        {activeTab === 'simulator' ? (
          <div className="space-y-6">
            {/* Top Row: Resources & Decision Rationale */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ResourceStatus
                totalResources={simState.total_resources}
                availableResources={simState.available_resources}
                resourceNames={simState.resource_names}
              />
              <SelectionExplanation
                lastSelection={simState.last_selection}
                algorithm={simState.algorithm}
              />
            </div>

            {/* Middle Row: Process Status & Current Requests */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ProcessStatus processes={simState.processes} />
              <CurrentRequests
                candidates={simState.candidates}
                lastSelection={simState.last_selection}
                algorithm={simState.algorithm}
              />
            </div>

            {/* Demand Monitor & Manual Request Panel */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <DemandMonitor
                processes={simState.processes}
                alpha={simState.alpha}
                safetyMargin={simState.safety_margin}
              />
              <ManualRequestPanel
                processes={simState.processes}
                resourceNames={simState.resource_names}
              />
            </div>

            {/* Bottom Row: Event Log */}
            <EventLog events={simState.events} />
          </div>
        ) : (
          <ComparisonDashboard currentScenario={simState.scenario} />
        )}
      </main>
    </div>
  );
}
