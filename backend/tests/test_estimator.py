import pytest
from algorithms.demand_estimator import calculate_ewma_prediction

def test_initial_ewma_prediction():
    req = [2, 1, 0]
    pred, est = calculate_ewma_prediction(req, prev_prediction=[], alpha=0.6, safety_margin=1.0)
    
    assert pred == [2.0, 1.0, 0.0]
    # ceil(2.0 + 1.0) = 3, ceil(1.0 + 1.0) = 2, ceil(0.0 + 1.0) = 1
    assert est == [3, 2, 1]

def test_updated_ewma_prediction():
    prev_pred = [2.0, 1.0, 0.0]
    new_req = [4, 2, 1]
    
    # Prediction = 0.6 * new + 0.4 * prev
    # R1: 0.6 * 4 + 0.4 * 2.0 = 2.4 + 0.8 = 3.2
    # R2: 0.6 * 2 + 0.4 * 1.0 = 1.2 + 0.4 = 1.6
    # R3: 0.6 * 1 + 0.4 * 0.0 = 0.6 + 0.0 = 0.6
    pred, est = calculate_ewma_prediction(new_req, prev_pred, alpha=0.6, safety_margin=1.0)
    
    assert round(pred[0], 2) == 3.2
    assert round(pred[1], 2) == 1.6
    assert round(pred[2], 2) == 0.6
    
    # ceil(3.2 + 1) = 5, ceil(1.6 + 1) = 3, ceil(0.6 + 1) = 2
    assert est == [5, 3, 2]
