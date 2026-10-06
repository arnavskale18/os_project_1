from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from models.state import (
    SimulationState, SimulationMetrics, SimulationEvent,
    CandidateEvaluation, AlgorithmType, ScenarioType
)
from simulation.engine import SimulationEngine

app = FastAPI(
    title="Adaptive Banker's Algorithm Simulation API",
    description="Backend API for Adaptive Banker's Algorithm vs Classical Banker's Algorithm deadlock avoidance simulation.",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global in-memory simulation engine instance
engine = SimulationEngine(scenario=ScenarioType.STARVATION, algorithm=AlgorithmType.ADAPTIVE)

# Request DTOs
class CreateSimulationRequest(BaseModel):
    scenario: ScenarioType = ScenarioType.STARVATION
    algorithm: AlgorithmType = AlgorithmType.ADAPTIVE
    total_resources: Optional[List[int]] = None
    alpha: Optional[float] = 0.6
    safety_margin: Optional[float] = 1.0
    starvation_threshold: Optional[int] = 10

class ManualRequestEvaluationPayload(BaseModel):
    pid: str
    request: List[int]

class RunExperimentPayload(BaseModel):
    scenario: ScenarioType = ScenarioType.STARVATION
    max_ticks: int = 50

@app.get("/")
def read_root():
    return {
        "message": "Adaptive Banker's Algorithm Simulation API is running.",
        "status": "online"
    }

@app.post("/simulation/create")
def create_simulation(req: CreateSimulationRequest):
    global engine
    engine.reset(scenario=req.scenario, algorithm=req.algorithm)
    if req.total_resources:
        engine.total_resources = list(req.total_resources)
        # Update available
        alloc_sum = [0] * len(req.total_resources)
        for p in engine.processes.values():
            for i, a in enumerate(p.allocation):
                alloc_sum[i] += a
        engine.available_resources = [t - a for t, a in zip(req.total_resources, alloc_sum)]
    if req.alpha is not None:
        engine.alpha = req.alpha
    if req.safety_margin is not None:
        engine.safety_margin = req.safety_margin
    if req.starvation_threshold is not None:
        engine.starvation_threshold = req.starvation_threshold

    return engine.get_state()

@app.post("/simulation/start")
def start_simulation():
    engine.is_running = True
    return engine.get_state()

@app.post("/simulation/pause")
def pause_simulation():
    engine.is_running = False
    return engine.get_state()

@app.post("/simulation/reset")
def reset_simulation():
    engine.reset()
    return engine.get_state()

@app.post("/simulation/step")
def step_simulation():
    state = engine.step()
    return state

@app.get("/simulation/state")
def get_simulation_state():
    return engine.get_state()

@app.get("/simulation/metrics")
def get_simulation_metrics():
    return engine.metrics_collector.calculate(
        engine.tick, list(engine.processes.values()), engine.starvation_threshold
    )

@app.get("/simulation/events")
def get_simulation_events():
    return engine.events

@app.post("/request/evaluate")
def evaluate_manual_request(payload: ManualRequestEvaluationPayload):
    evaluation = engine.evaluate_manual_request(payload.pid, payload.request)
    return {
        "pid": payload.pid,
        "request": payload.request,
        "evaluation": evaluation
    }

@app.post("/experiment/run")
def run_experiment(payload: RunExperimentPayload):
    """
    Executes identical scenario workload on Classical Banker and Adaptive Banker side-by-side.
    Returns complete comparative analysis.
    """
    engine_classical = SimulationEngine(scenario=payload.scenario, algorithm=AlgorithmType.CLASSICAL)
    engine_adaptive = SimulationEngine(scenario=payload.scenario, algorithm=AlgorithmType.ADAPTIVE)
    
    ticks_history = []
    
    for t in range(1, payload.max_ticks + 1):
        state_c = engine_classical.step()
        state_a = engine_adaptive.step()
        
        ticks_history.append({
            "tick": t,
            "classical_waiting_time": state_c.metrics.avg_waiting_time,
            "adaptive_waiting_time": state_a.metrics.avg_waiting_time,
            "classical_utilization": state_c.metrics.resource_utilization,
            "adaptive_utilization": state_a.metrics.resource_utilization,
            "classical_completed": state_c.metrics.completed_processes,
            "adaptive_completed": state_a.metrics.completed_processes,
        })
        
        # Stop early if both completed all processes
        if (
            state_c.metrics.completed_processes == state_c.metrics.total_processes and
            state_a.metrics.completed_processes == state_a.metrics.total_processes
        ):
            break

    classical_metrics = engine_classical.get_state().metrics
    adaptive_metrics = engine_adaptive.get_state().metrics
    
    # Calculate improvements
    wait_reduction = (
        round(((classical_metrics.avg_waiting_time - adaptive_metrics.avg_waiting_time) / float(classical_metrics.avg_waiting_time)) * 100.0, 1)
        if classical_metrics.avg_waiting_time > 0 else 0.0
    )
    
    return {
        "scenario": payload.scenario,
        "classical_metrics": classical_metrics,
        "adaptive_metrics": adaptive_metrics,
        "ticks_history": ticks_history,
        "classical_events": engine_classical.events,
        "adaptive_events": engine_adaptive.events,
        "summary": {
            "wait_reduction_pct": wait_reduction,
            "starvation_prevented": classical_metrics.starvation_count > adaptive_metrics.starvation_count,
            "safety_violations_classical": classical_metrics.safety_violations,
            "safety_violations_adaptive": adaptive_metrics.safety_violations
        }
    }
