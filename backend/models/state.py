from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class ProcessState(str, Enum):
    READY = "READY"
    WAITING = "WAITING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"

class AlgorithmType(str, Enum):
    CLASSICAL = "CLASSICAL"
    ADAPTIVE = "ADAPTIVE"

class ScenarioType(str, Enum):
    NORMAL = "NORMAL"
    HIGH_CONTENTION = "HIGH_CONTENTION"
    STARVATION = "STARVATION"
    DYNAMIC_DEMAND = "DYNAMIC_DEMAND"

class ScriptedRequest(BaseModel):
    tick: int
    request: List[int]
    burst: int = 3

class ProcessModel(BaseModel):
    pid: str
    priority: int = 5  # 1 to 10
    max_claim: List[int]
    allocation: List[int]
    need: List[int]
    waiting_time: int = 0
    execution_time: int = 3
    remaining_execution_time: int = 0
    request_history: List[List[int]] = Field(default_factory=list)
    predicted_demand: List[float] = Field(default_factory=list)
    estimated_demand: List[int] = Field(default_factory=list)
    aging_score: float = 0.0
    state: ProcessState = ProcessState.READY
    current_request: Optional[List[int]] = None
    scripted_requests: List[ScriptedRequest] = Field(default_factory=list)

class CandidateEvaluation(BaseModel):
    pid: str
    request: List[int]
    is_safe: bool
    safe_sequence: List[str] = Field(default_factory=list)
    reason: str
    scores: Dict[str, float] = Field(default_factory=dict)
    total_score: float = 0.0
    selected: bool = False

class SimulationEvent(BaseModel):
    tick: int
    pid: Optional[str] = None
    event_type: str  # REQUEST, SAFETY_CHECK, SAFE, UNSAFE, DEFERRED, RANKING, GRANT, RUN, RELEASE, COMPLETE
    message: str
    details: Optional[Dict[str, Any]] = None

class SimulationMetrics(BaseModel):
    avg_waiting_time: float = 0.0
    max_waiting_time: int = 0
    resource_utilization: float = 0.0  # percentage
    throughput: float = 0.0
    starvation_count: int = 0
    deferred_requests: int = 0
    completed_processes: int = 0
    total_processes: int = 0
    simulation_duration: int = 0
    safety_checks: int = 0
    candidate_evaluations: int = 0
    safety_violations: int = 0

class SimulationState(BaseModel):
    tick: int = 0
    algorithm: AlgorithmType = AlgorithmType.ADAPTIVE
    scenario: ScenarioType = ScenarioType.STARVATION
    total_resources: List[int] = Field(default_factory=lambda: [10, 8, 6])
    available_resources: List[int] = Field(default_factory=lambda: [10, 8, 6])
    resource_names: List[str] = Field(default_factory=lambda: ["R1", "R2", "R3"])
    processes: List[ProcessModel] = Field(default_factory=list)
    candidates: List[CandidateEvaluation] = Field(default_factory=list)
    last_selection: Optional[CandidateEvaluation] = None
    events: List[SimulationEvent] = Field(default_factory=list)
    metrics: SimulationMetrics = Field(default_factory=SimulationMetrics)
    is_running: bool = False
    alpha: float = 0.6
    safety_margin: float = 1.0
    starvation_threshold: int = 10
    speed_ms: int = 500
