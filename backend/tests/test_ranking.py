import pytest
from models.state import CandidateEvaluation, ProcessModel, ProcessState
from algorithms.ranking import rank_safe_candidates, compute_starvation_score

def test_aging_score_growth():
    p = ProcessModel(pid="P1", priority=5, max_claim=[5, 5, 5], allocation=[0, 0, 0], need=[5, 5, 5], waiting_time=5)
    cand = CandidateEvaluation(pid="P1", request=[1, 1, 1], is_safe=True, reason="SAFE")
    
    scores = compute_starvation_score(cand, p, max_wait_in_system=10, starvation_threshold=10)
    
    # waiting_time = 5 / threshold 10 -> aging = 0.5
    assert scores["aging_score"] == 0.5
    assert scores["waiting_score"] == 0.5

    p.waiting_time = 12
    scores_aged = compute_starvation_score(cand, p, max_wait_in_system=12, starvation_threshold=10)
    assert scores_aged["aging_score"] == 1.0

def test_safe_candidate_ranking():
    # Process P1 waited longer (wait=8) vs Process P2 (wait=1)
    p1 = ProcessModel(pid="P1", priority=4, max_claim=[5, 5, 5], allocation=[0, 0, 0], need=[5, 5, 5], waiting_time=8)
    p2 = ProcessModel(pid="P2", priority=6, max_claim=[3, 3, 3], allocation=[0, 0, 0], need=[3, 3, 3], waiting_time=1)
    
    cand1 = CandidateEvaluation(pid="P1", request=[2, 2, 2], is_safe=True, reason="SAFE")
    cand2 = CandidateEvaluation(pid="P2", request=[1, 1, 1], is_safe=True, reason="SAFE")
    cand3 = CandidateEvaluation(pid="P3", request=[4, 4, 4], is_safe=False, reason="UNSAFE")
    
    processes = {"P1": p1, "P2": p2}
    ranked = rank_safe_candidates([cand2, cand1, cand3], processes, starvation_threshold=10)
    
    # P1 should rank first due to higher waiting time and aging score
    assert ranked[0].pid == "P1"
    assert ranked[0].is_safe is True
    # Unsafe candidate cand3 should be at the end and marked unsafe
    assert ranked[-1].pid == "P3"
    assert ranked[-1].is_safe is False
