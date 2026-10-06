import pytest
from algorithms.banker import (
    validate_request_bounds,
    run_safety_algorithm,
    evaluate_banker_request
)
from models.state import ProcessModel, ProcessState

def test_request_validation():
    # Need = [4, 3, 2], Available = [3, 3, 2]
    # Request [2, 1, 1] <= Need and <= Available -> Valid
    valid, reason = validate_request_bounds([2, 1, 1], [4, 3, 2], [3, 3, 2])
    assert valid is True

    # Request [5, 1, 1] > Need -> Invalid
    valid, reason = validate_request_bounds([5, 1, 1], [4, 3, 2], [3, 3, 2])
    assert valid is False
    assert "exceeds remaining Need" in reason

    # Request [3, 3, 2] <= Need [4, 4, 2] but > Available [3, 2, 2] -> Invalid
    valid, reason = validate_request_bounds([3, 3, 2], [4, 4, 2], [3, 2, 2])
    assert valid is False
    assert "exceeds currently Available" in reason

def test_safe_banker_state():
    available = [3, 3, 2]
    allocations = {
        "P1": [0, 1, 0],
        "P2": [2, 0, 0],
        "P3": [3, 0, 2],
        "P4": [2, 1, 1],
        "P5": [0, 0, 2]
    }
    needs = {
        "P1": [7, 4, 3],
        "P2": [1, 2, 2],
        "P3": [6, 0, 0],
        "P4": [0, 1, 1],
        "P5": [4, 3, 1]
    }
    pids = ["P1", "P2", "P3", "P4", "P5"]

    is_safe, sequence = run_safety_algorithm(available, allocations, needs, pids)
    assert is_safe is True
    assert len(sequence) == 5
    assert "P2" in sequence

def test_unsafe_banker_state():
    # Tight available resource where no process can finish
    available = [0, 0, 0]
    allocations = {
        "P1": [1, 0, 0],
        "P2": [0, 1, 0]
    }
    needs = {
        "P1": [2, 1, 1],
        "P2": [1, 2, 1]
    }
    pids = ["P1", "P2"]

    is_safe, sequence = run_safety_algorithm(available, allocations, needs, pids)
    assert is_safe is False
    assert sequence == []

def test_unsafe_request_is_rejected():
    """CRITICAL MANDATORY TEST: Attempt to grant an unsafe request MUST NOT BE GRANTED."""
    available = [1, 0, 0]
    allocations = {"P1": [2, 1, 1], "P2": [2, 0, 0]}
    needs = {"P1": [3, 2, 2], "P2": [1, 3, 3]}
    pids = ["P1", "P2"]

    eval_res = evaluate_banker_request(
        pid="P1",
        request=[1, 0, 0],
        available=available,
        allocations=allocations,
        needs=needs,
        active_pids=pids
    )

    assert eval_res.is_safe is False
    assert eval_res.selected is False
    assert "UNSAFE" in eval_res.reason
