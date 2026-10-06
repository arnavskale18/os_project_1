import math
from typing import List, Tuple

def calculate_ewma_prediction(
    current_request: List[int],
    prev_prediction: List[float],
    alpha: float = 0.6,
    safety_margin: float = 1.0
) -> Tuple[List[float], List[int]]:
    """
    Calculates EWMA predicted demand and estimated demand with safety margin.
    
    Prediction(t) = alpha * Observation(t) + (1 - alpha) * Prediction(t-1)
    EstimatedDemand = ceil(Prediction + SafetyMargin)
    """
    if not prev_prediction or len(prev_prediction) != len(current_request):
        # Initial prediction is current request float values
        new_prediction = [float(r) for r in current_request]
    else:
        new_prediction = [
            alpha * float(req) + (1.0 - alpha) * prev_pred
            for req, prev_pred in zip(current_request, prev_prediction)
        ]
        
    estimated_demand = [
        math.ceil(pred + safety_margin)
        for pred in new_prediction
    ]
    
    return new_prediction, estimated_demand
