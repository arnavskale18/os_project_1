from typing import List, Dict
from models.state import SimulationMetrics, ProcessModel, ProcessState

class MetricsCollector:
    """Collects and calculates live simulation metrics."""
    def __init__(self):
        self.reset()

    def reset(self):
        self.safety_checks = 0
        self.candidate_evaluations = 0
        self.deferred_requests = 0
        self.safety_violations = 0
        self.process_wait_history: Dict[str, int] = {}
        self.utilization_history: List[float] = []

    def record_safety_check(self):
        self.safety_checks += 1

    def record_candidate_eval(self):
        self.candidate_evaluations += 1

    def record_deferred(self):
        self.deferred_requests += 1

    def record_safety_violation(self):
        self.safety_violations += 1

    def record_process_wait(self, pid: str, current_wait: int):
        if pid not in self.process_wait_history or current_wait > self.process_wait_history[pid]:
            self.process_wait_history[pid] = current_wait

    def record_resource_utilization(self, total: List[int], allocated: List[int]):
        sum_total = max(1, sum(total))
        sum_alloc = sum(allocated)
        util_pct = (sum_alloc / float(sum_total)) * 100.0
        self.utilization_history.append(util_pct)

    def calculate(
        self,
        tick: int,
        processes: List[ProcessModel],
        starvation_threshold: int = 10
    ) -> SimulationMetrics:
        total_procs = len(processes)
        completed_procs = sum(1 for p in processes if p.state == ProcessState.COMPLETED)
        
        # Update process_wait_history for currently waiting processes
        for p in processes:
            self.record_process_wait(p.pid, p.waiting_time)

        all_waits = list(self.process_wait_history.values()) if self.process_wait_history else [0]
        avg_wait = round(sum(all_waits) / float(total_procs), 2) if total_procs > 0 else 0.0
        max_wait = max(all_waits) if all_waits else 0
        
        starvation_count = sum(1 for w in all_waits if w >= starvation_threshold)
        
        avg_util = (
            round(sum(self.utilization_history) / float(len(self.utilization_history)), 2)
            if self.utilization_history else 0.0
        )
        
        throughput = (
            round((completed_procs / float(tick)) * 100.0, 2)
            if tick > 0 else 0.0
        )

        return SimulationMetrics(
            avg_waiting_time=avg_wait,
            max_waiting_time=max_wait,
            resource_utilization=avg_util,
            throughput=throughput,
            starvation_count=starvation_count,
            deferred_requests=self.deferred_requests,
            completed_processes=completed_procs,
            total_processes=total_procs,
            simulation_duration=tick,
            safety_checks=self.safety_checks,
            candidate_evaluations=self.candidate_evaluations,
            safety_violations=self.safety_violations
        )
