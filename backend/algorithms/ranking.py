from typing import List, Dict
from models.state import CandidateEvaluation, ProcessModel

def compute_starvation_score(
    candidate: CandidateEvaluation,
    process: ProcessModel,
    max_wait_in_system: int,
    starvation_threshold: int = 10
) -> Dict[str, float]:
    """
    Calculates normalized scores for a safe candidate request:
    Score = 0.40 * WaitingScore + 0.20 * PriorityScore + 0.20 * EfficiencyScore + 0.20 * AgingScore
    """
    # 1. WaitingScore (0.0 to 1.0): normalized current waiting time
    if max_wait_in_system > 0:
        waiting_score = min(1.0, process.waiting_time / float(max_wait_in_system))
    else:
        waiting_score = 0.0

    # 2. PriorityScore (0.0 to 1.0): normalized process priority (1-10)
    priority_score = min(1.0, max(0.1, process.priority / 10.0))

    # 3. EfficiencyScore (0.0 to 1.0): requested resources relative to Need & Estimated Demand
    total_requested = sum(candidate.request)
    total_need = sum(process.need)
    
    if total_need > 0:
        need_efficiency = min(1.0, total_requested / float(total_need))
    else:
        need_efficiency = 1.0
        
    total_est_demand = sum(process.estimated_demand) if process.estimated_demand else total_requested
    if total_est_demand > 0:
        demand_efficiency = min(1.0, total_requested / float(total_est_demand))
    else:
        demand_efficiency = 1.0
        
    efficiency_score = round(0.5 * need_efficiency + 0.5 * demand_efficiency, 4)

    # 4. AgingScore (0.0 to 1.0): min(1.0, waiting_time / starvation_threshold)
    aging_score = min(1.0, process.waiting_time / float(starvation_threshold))

    # Total weighted score
    total_score = round(
        0.40 * waiting_score +
        0.20 * priority_score +
        0.20 * efficiency_score +
        0.20 * aging_score,
        4
    )

    scores = {
        "waiting_score": round(waiting_score, 4),
        "priority_score": round(priority_score, 4),
        "efficiency_score": round(efficiency_score, 4),
        "aging_score": round(aging_score, 4),
        "demand_efficiency": round(demand_efficiency, 4),
        "total_score": total_score
    }
    
    return scores

def rank_safe_candidates(
    candidates: List[CandidateEvaluation],
    processes_map: Dict[str, ProcessModel],
    starvation_threshold: int = 10
) -> List[CandidateEvaluation]:
    """
    Ranks safe candidates using Starvation-Aware scoring.
    Only SAFE candidates are given scores and ranked.
    Unsafe candidates retain total_score = 0.0 and selected = False.
    """
    safe_candidates = [c for c in candidates if c.is_safe]
    unsafe_candidates = [c for c in candidates if not c.is_safe]
    
    if not safe_candidates:
        return candidates

    # Find maximum waiting time among processes with safe candidates
    max_wait = max(processes_map[c.pid].waiting_time for c in safe_candidates)

    for c in safe_candidates:
        proc = processes_map[c.pid]
        scores = compute_starvation_score(c, proc, max_wait, starvation_threshold)
        c.scores = scores
        c.total_score = scores["total_score"]

    # Sort safe candidates by total_score descending
    safe_candidates.sort(key=lambda x: x.total_score, reverse=True)
    
    return safe_candidates + unsafe_candidates
