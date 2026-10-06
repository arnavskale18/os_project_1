from typing import List, Dict, Tuple
from models.state import CandidateEvaluation, ProcessState

def is_vector_less_equal(v1: List[int], v2: List[int]) -> bool:
    """Check if all elements of v1 are <= corresponding elements of v2."""
    if len(v1) != len(v2):
        return False
    return all(a <= b for a, b in zip(v1, v2))

def validate_request_bounds(request: List[int], need: List[int], available: List[int]) -> Tuple[bool, str]:
    """
    Check basic preconditions for Banker's Algorithm:
    1. Request <= Need
    2. Request <= Available
    """
    if any(r < 0 for r in request):
        return False, "Invalid negative resource request."
        
    if not is_vector_less_equal(request, need):
        return False, f"Request {request} exceeds remaining Need {need}."
        
    if not is_vector_less_equal(request, available):
        return False, f"Request {request} exceeds currently Available resources {available}."
        
    return True, "Request satisfies Need and Available bounds."

def run_safety_algorithm(
    available: List[int],
    allocations: Dict[str, List[int]],
    needs: Dict[str, List[int]],
    pids: List[str]
) -> Tuple[bool, List[str]]:
    """
    Classical Banker's Safety Algorithm.
    Returns (is_safe, safe_sequence).
    """
    work = list(available)
    finish = {pid: False for pid in pids}
    safe_sequence = []
    
    # Process loop until no more processes can finish
    changed = True
    while changed:
        changed = False
        for pid in pids:
            if not finish[pid]:
                # Check if Need[pid] <= Work
                if is_vector_less_equal(needs[pid], work):
                    # Simulate allocation return
                    work = [w + alloc for w, alloc in zip(work, allocations[pid])]
                    finish[pid] = True
                    safe_sequence.append(pid)
                    changed = True
                    break
                    
    is_safe = all(finish.values())
    if is_safe:
        return True, safe_sequence
    else:
        return False, []

def evaluate_banker_request(
    pid: str,
    request: List[int],
    available: List[int],
    allocations: Dict[str, List[int]],
    needs: Dict[str, List[int]],
    active_pids: List[str]
) -> CandidateEvaluation:
    """
    Evaluates a single process request using Classical Banker Algorithm.
    Temporarily allocates resources, performs safety check, and rolls back state.
    """
    # 1. Bounds check
    valid, reason = validate_request_bounds(request, needs[pid], available)
    if not valid:
        return CandidateEvaluation(
            pid=pid,
            request=request,
            is_safe=False,
            safe_sequence=[],
            reason=reason,
            selected=False
        )
        
    # 2. Temporary allocation
    temp_available = [a - r for a, r in zip(available, request)]
    temp_allocations = {p: list(allocations[p]) for p in active_pids}
    temp_needs = {p: list(needs[p]) for p in active_pids}
    
    temp_allocations[pid] = [a + r for a, r in zip(temp_allocations[pid], request)]
    temp_needs[pid] = [n - r for n, r in zip(temp_needs[pid], request)]
    
    # 3. Safety check
    is_safe, safe_sequence = run_safety_algorithm(
        temp_available,
        temp_allocations,
        temp_needs,
        active_pids
    )
    
    if is_safe:
        return CandidateEvaluation(
            pid=pid,
            request=request,
            is_safe=True,
            safe_sequence=safe_sequence,
            reason="State is SAFE after hypothetical allocation.",
            selected=False
        )
    else:
        return CandidateEvaluation(
            pid=pid,
            request=request,
            is_safe=False,
            safe_sequence=[],
            reason="State becomes UNSAFE after hypothetical allocation (Deadlock risk).",
            selected=False
        )
