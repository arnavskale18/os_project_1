import copy
from typing import List, Dict, Tuple, Optional
from models.state import (
    SimulationState, ProcessModel, ProcessState, CandidateEvaluation,
    SimulationEvent, AlgorithmType, ScenarioType, ScriptedRequest
)
from algorithms.banker import evaluate_banker_request, run_safety_algorithm
from algorithms.demand_estimator import calculate_ewma_prediction
from algorithms.ranking import rank_safe_candidates, compute_starvation_score
from simulation.scenarios import get_scenario_data
from metrics.metrics import MetricsCollector

class SimulationEngine:
    def __init__(self, scenario: ScenarioType = ScenarioType.STARVATION, algorithm: AlgorithmType = AlgorithmType.ADAPTIVE):
        self.scenario = scenario
        self.algorithm = algorithm
        self.alpha = 0.6
        self.safety_margin = 1.0
        self.starvation_threshold = 10
        self.script_indices: Dict[str, int] = {}
        self.metrics_collector = MetricsCollector()
        self.reset(scenario, algorithm)

    def reset(self, scenario: Optional[ScenarioType] = None, algorithm: Optional[AlgorithmType] = None):
        if scenario is not None:
            self.scenario = scenario
        if algorithm is not None:
            self.algorithm = algorithm

        total_resources, process_models = get_scenario_data(self.scenario)
        self.tick = 0
        self.total_resources = list(total_resources)
        self.script_indices = {p.pid: 0 for p in process_models}
        
        # Available = Total - sum(allocation)
        allocated_sum = [0] * len(total_resources)
        for p in process_models:
            for i, a in enumerate(p.allocation):
                allocated_sum[i] += a
                
        self.available_resources = [t - a for t, a in zip(self.total_resources, allocated_sum)]
        self.processes: Dict[str, ProcessModel] = {p.pid: copy.deepcopy(p) for p in process_models}
        self.candidates: List[CandidateEvaluation] = []
        self.last_selection: Optional[CandidateEvaluation] = None
        self.events: List[SimulationEvent] = []
        self.is_running = False
        self.metrics_collector.reset()
        
        self.log_event(None, "SYSTEM_INIT", f"Simulation initialized with Scenario '{self.scenario.value}' and Algorithm '{self.algorithm.value}'.")

    def log_event(self, pid: Optional[str], event_type: str, message: str, details: Optional[dict] = None):
        event = SimulationEvent(
            tick=self.tick,
            pid=pid,
            event_type=event_type,
            message=message,
            details=details
        )
        self.events.append(event)
        # Keep event log bounded to last 200 events
        if len(self.events) > 200:
            self.events.pop(0)

    def get_active_pids(self) -> List[str]:
        return [pid for pid, p in self.processes.items() if p.state != ProcessState.COMPLETED]

    def evaluate_manual_request(self, pid: str, request: List[int]) -> CandidateEvaluation:
        """
        Manual Request evaluation mode (does not alter simulation state permanently).
        """
        if pid not in self.processes:
            return CandidateEvaluation(
                pid=pid, request=request, is_safe=False,
                reason=f"Process {pid} does not exist.", selected=False
            )
            
        proc = self.processes[pid]
        active_pids = self.get_active_pids()
        
        allocations = {p: self.processes[p].allocation for p in active_pids}
        needs = {p: self.processes[p].need for p in active_pids}
        
        self.metrics_collector.record_candidate_eval()
        self.metrics_collector.record_safety_check()
        
        eval_res = evaluate_banker_request(
            pid, request, self.available_resources, allocations, needs, active_pids
        )
        
        if self.algorithm == AlgorithmType.ADAPTIVE and eval_res.is_safe:
            max_wait = max(p.waiting_time for p in self.processes.values())
            scores = compute_starvation_score(eval_res, proc, max_wait, self.starvation_threshold)
            eval_res.scores = scores
            eval_res.total_score = scores["total_score"]
            
        return eval_res

    def step(self) -> SimulationState:
        """
        Advance discrete simulation by exactly ONE tick.
        """
        self.tick += 1
        
        # 1. Update RUNNING processes progress
        for pid, p in self.processes.items():
            if p.state == ProcessState.RUNNING:
                p.remaining_execution_time -= 1
                self.log_event(pid, "RUN", f"Process {pid} executing. Ticks remaining: {p.remaining_execution_time}.")
                
                if p.remaining_execution_time <= 0:
                    # Release allocated resources!
                    released = list(p.allocation)
                    self.available_resources = [a + r for a, r in zip(self.available_resources, released)]
                    p.allocation = [0] * len(self.total_resources)
                    # Need remains max_claim - allocation
                    p.need = list(p.max_claim)
                    
                    s_idx = self.script_indices.get(pid, 0)
                    has_more = (s_idx < len(p.scripted_requests)) or bool(p.current_request)
                    if has_more:
                        p.state = ProcessState.READY
                        self.log_event(
                            pid, "RELEASE",
                            f"Process {pid} completed burst and released resources {released}. Waiting for next scheduled burst. Available: {self.available_resources}."
                        )
                    else:
                        p.state = ProcessState.COMPLETED
                        self.log_event(
                            pid, "RELEASE",
                            f"Process {pid} completed burst and released resources {released}. Available: {self.available_resources}."
                        )
                        self.log_event(pid, "COMPLETE", f"Process {pid} reached COMPLETED state.")

        # 2. Update WAITING processes aging and waiting times
        for pid, p in self.processes.items():
            if p.state == ProcessState.WAITING:
                p.waiting_time += 1
                p.aging_score = min(1.0, round(p.waiting_time / float(self.starvation_threshold), 4))
                self.metrics_collector.record_process_wait(pid, p.waiting_time)
                self.log_event(
                    pid, "WAITING",
                    f"Process {pid} waiting for resources. Waiting time: {p.waiting_time}, Aging Score: {p.aging_score}."
                )

        # 3. Check for scripted or pending requests at current tick
        pending_requests: List[Tuple[str, List[int], int]] = []
        for pid, p in self.processes.items():
            if p.state in [ProcessState.READY, ProcessState.WAITING]:
                s_idx = self.script_indices.get(pid, 0)
                if not p.current_request and s_idx < len(p.scripted_requests):
                    next_req = p.scripted_requests[s_idx]
                    if next_req.tick <= self.tick:
                        p.current_request = list(next_req.request)
                        p.execution_time = next_req.burst
                        self.script_indices[pid] = s_idx + 1
                        pending_requests.append((pid, list(p.current_request), p.execution_time))
                        self.log_event(pid, "REQUEST", f"Process {pid} issued resource request {next_req.request}.")
                elif p.current_request:
                    # Unfulfilled pending request from previous tick
                    pending_requests.append((pid, list(p.current_request), p.execution_time))

        self.candidates = []
        self.last_selection = None
        
        # 4. Evaluate candidates
        if pending_requests:
            active_pids = self.get_active_pids()
            allocations = {p: self.processes[p].allocation for p in active_pids}
            needs = {p: self.processes[p].need for p in active_pids}
            
            evaluated_candidates: List[CandidateEvaluation] = []
            
            for pid, req, burst in pending_requests:
                proc = self.processes[pid]
                
                # Demand Monitoring & Estimator (Adaptive Banker)
                if self.algorithm == AlgorithmType.ADAPTIVE:
                    proc.request_history.append(req)
                    pred, est = calculate_ewma_prediction(
                        req, proc.predicted_demand, self.alpha, self.safety_margin
                    )
                    proc.predicted_demand = [round(x, 2) for x in pred]
                    proc.estimated_demand = est

                # Classical Banker Safety Evaluation
                self.metrics_collector.record_candidate_eval()
                self.metrics_collector.record_safety_check()
                
                cand_eval = evaluate_banker_request(
                    pid, req, self.available_resources, allocations, needs, active_pids
                )
                
                if cand_eval.is_safe:
                    self.log_event(
                        pid, "SAFE",
                        f"Banker Safety Test PASSED for {pid}. Safe sequence: {' -> '.join(cand_eval.safe_sequence)}."
                    )
                else:
                    self.log_event(
                        pid, "UNSAFE",
                        f"Banker Safety Test FAILED for {pid}. Reason: {cand_eval.reason}."
                    )
                    self.metrics_collector.record_deferred()
                    
                evaluated_candidates.append(cand_eval)

            # 5. Selection Policy (Classical vs Adaptive)
            if self.algorithm == AlgorithmType.ADAPTIVE:
                # Rank safe candidates using Starvation-Aware Scoring
                ranked_candidates = rank_safe_candidates(
                    evaluated_candidates, self.processes, self.starvation_threshold
                )
                self.candidates = ranked_candidates
                
                safe_candidates = [c for c in ranked_candidates if c.is_safe]
                if safe_candidates:
                    top_candidate = safe_candidates[0] # Highest score safe candidate
                    top_candidate.selected = True
                    self.last_selection = top_candidate
                    self.log_event(
                        top_candidate.pid, "RANKING",
                        f"Selected {top_candidate.pid} with highest Starvation-Aware Score {top_candidate.total_score}."
                    )
            else:
                # CLASSICAL BANKER (FCFS baseline selection)
                self.candidates = evaluated_candidates
                safe_candidates = [c for c in evaluated_candidates if c.is_safe]
                if safe_candidates:
                    top_candidate = safe_candidates[0] # First safe request
                    top_candidate.selected = True
                    self.last_selection = top_candidate
                    self.log_event(
                        top_candidate.pid, "GRANT",
                        f"Classical Banker selected {top_candidate.pid} (First Safe Request)."
                    )

            # 6. Allocate Selected Candidate
            if self.last_selection and self.last_selection.is_safe:
                sel_pid = self.last_selection.pid
                sel_req = self.last_selection.request
                proc = self.processes[sel_pid]
                
                # DOUBLE CHECK SAFETY (HARD GUARANTEE): Never grant if insufficient available!
                if not all(r <= a for r, a in zip(sel_req, self.available_resources)):
                    self.metrics_collector.record_safety_violation()
                    self.log_event(
                        sel_pid, "SAFETY_VIOLATION",
                        f"CRITICAL ERROR: Attempted to allocate {sel_req} to {sel_pid} when available is {self.available_resources}!"
                    )
                else:
                    # Allocate resources
                    self.available_resources = [a - r for a, r in zip(self.available_resources, sel_req)]
                    proc.allocation = [a + r for a, r in zip(proc.allocation, sel_req)]
                    proc.need = [m - a for m, a in zip(proc.max_claim, proc.allocation)]
                    proc.state = ProcessState.RUNNING
                    proc.remaining_execution_time = proc.execution_time
                    proc.waiting_time = 0
                    proc.aging_score = 0.0
                    proc.current_request = None # Request fulfilled
                    
                    self.log_event(
                        sel_pid, "GRANT",
                        f"Allocated {sel_req} to {sel_pid}. Available resources remaining: {self.available_resources}."
                    )

            # Mark all unselected processes to WAITING state
            for pid, req, burst in pending_requests:
                if not (self.last_selection and self.last_selection.pid == pid and self.last_selection.is_safe):
                    self.processes[pid].state = ProcessState.WAITING

        # 7. Record metrics
        allocated_curr = [
            sum(p.allocation[i] for p in self.processes.values())
            for i in range(len(self.total_resources))
        ]
        self.metrics_collector.record_resource_utilization(self.total_resources, allocated_curr)
        
        return self.get_state()

    def get_state(self) -> SimulationState:
        metrics = self.metrics_collector.calculate(
            self.tick, list(self.processes.values()), self.starvation_threshold
        )
        return SimulationState(
            tick=self.tick,
            algorithm=self.algorithm,
            scenario=self.scenario,
            total_resources=list(self.total_resources),
            available_resources=list(self.available_resources),
            resource_names=["R1", "R2", "R3"][:len(self.total_resources)],
            processes=list(self.processes.values()),
            candidates=list(self.candidates),
            last_selection=self.last_selection,
            events=list(self.events),
            metrics=metrics,
            is_running=self.is_running,
            alpha=self.alpha,
            safety_margin=self.safety_margin,
            starvation_threshold=self.starvation_threshold
        )
