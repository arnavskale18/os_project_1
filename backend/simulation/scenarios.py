from typing import List, Dict, Tuple
from models.state import ProcessModel, ScenarioType, ScriptedRequest, ProcessState

def get_scenario_data(scenario: ScenarioType) -> Tuple[List[int], List[ProcessModel]]:
    """
    Returns (total_resources, list_of_process_models) for a given scenario.
    """
    if scenario == ScenarioType.NORMAL:
        total_resources = [10, 8, 6]
        processes = [
            ProcessModel(
                pid="P1", priority=5, max_claim=[7, 5, 3], allocation=[0, 1, 0], need=[7, 4, 3],
                execution_time=3,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[2, 1, 1], burst=3),
                    ScriptedRequest(tick=6, request=[3, 1, 1], burst=3),
                    ScriptedRequest(tick=11, request=[2, 1, 1], burst=2)
                ]
            ),
            ProcessModel(
                pid="P2", priority=7, max_claim=[3, 2, 2], allocation=[2, 0, 0], need=[1, 2, 2],
                execution_time=3,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[1, 1, 1], burst=2),
                    ScriptedRequest(tick=5, request=[0, 1, 1], burst=3)
                ]
            ),
            ProcessModel(
                pid="P3", priority=3, max_claim=[9, 0, 2], allocation=[3, 0, 2], need=[6, 0, 0],
                execution_time=4,
                scripted_requests=[
                    ScriptedRequest(tick=2, request=[2, 0, 0], burst=4),
                    ScriptedRequest(tick=8, request=[4, 0, 0], burst=3)
                ]
            ),
            ProcessModel(
                pid="P4", priority=8, max_claim=[2, 2, 2], allocation=[2, 1, 1], need=[0, 1, 1],
                execution_time=2,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[0, 1, 1], burst=2)
                ]
            ),
            ProcessModel(
                pid="P5", priority=4, max_claim=[4, 3, 3], allocation=[0, 0, 2], need=[4, 3, 1],
                execution_time=3,
                scripted_requests=[
                    ScriptedRequest(tick=3, request=[2, 2, 1], burst=3),
                    ScriptedRequest(tick=9, request=[2, 1, 0], burst=2)
                ]
            )
        ]
        
    elif scenario == ScenarioType.HIGH_CONTENTION:
        total_resources = [7, 6, 5]
        processes = [
            ProcessModel(
                pid="P1", priority=5, max_claim=[5, 4, 3], allocation=[0, 0, 0], need=[5, 4, 3],
                execution_time=4,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[2, 2, 1], burst=4),
                    ScriptedRequest(tick=7, request=[2, 1, 2], burst=3)
                ]
            ),
            ProcessModel(
                pid="P2", priority=6, max_claim=[4, 3, 3], allocation=[0, 0, 0], need=[4, 3, 3],
                execution_time=3,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[2, 1, 1], burst=3),
                    ScriptedRequest(tick=6, request=[1, 1, 1], burst=3)
                ]
            ),
            ProcessModel(
                pid="P3", priority=4, max_claim=[5, 3, 4], allocation=[0, 0, 0], need=[5, 3, 4],
                execution_time=3,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[2, 2, 1], burst=3),
                    ScriptedRequest(tick=6, request=[1, 1, 2], burst=3)
                ]
            ),
            ProcessModel(
                pid="P4", priority=7, max_claim=[3, 4, 2], allocation=[0, 0, 0], need=[3, 4, 2],
                execution_time=2,
                scripted_requests=[
                    ScriptedRequest(tick=2, request=[1, 2, 1], burst=2)
                ]
            ),
            ProcessModel(
                pid="P5", priority=3, max_claim=[4, 4, 3], allocation=[0, 0, 0], need=[4, 4, 3],
                execution_time=4,
                scripted_requests=[
                    ScriptedRequest(tick=2, request=[2, 2, 1], burst=4)
                ]
            )
        ]

    elif scenario == ScenarioType.STARVATION:
        total_resources = [7, 6, 5]
        # P1 has lower priority and requests larger chunk.
        # P2, P3, P4 have higher priority and make smaller quick requests.
        # Classical Banker FCFS order grants P2 and P3 continuously while P1 starves.
        # Adaptive Banker elevates P1's score due to aging and grants P1 safely.
        processes = [
            ProcessModel(
                pid="P2", priority=6, max_claim=[3, 2, 2], allocation=[0, 0, 0], need=[3, 2, 2],
                execution_time=2,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[2, 1, 1], burst=2),
                    ScriptedRequest(tick=4, request=[2, 1, 1], burst=2),
                    ScriptedRequest(tick=7, request=[2, 1, 1], burst=2),
                    ScriptedRequest(tick=10, request=[1, 1, 1], burst=2)
                ]
            ),
            ProcessModel(
                pid="P3", priority=7, max_claim=[4, 3, 2], allocation=[0, 0, 0], need=[4, 3, 2],
                execution_time=2,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[2, 2, 1], burst=2),
                    ScriptedRequest(tick=4, request=[2, 2, 1], burst=2),
                    ScriptedRequest(tick=7, request=[2, 2, 1], burst=2)
                ]
            ),
            ProcessModel(
                pid="P1", priority=2, max_claim=[7, 5, 4], allocation=[0, 0, 0], need=[7, 5, 4],
                execution_time=4,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[5, 4, 3], burst=4)
                ]
            ),
            ProcessModel(
                pid="P4", priority=8, max_claim=[3, 2, 2], allocation=[0, 0, 0], need=[3, 2, 2],
                execution_time=2,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[1, 1, 1], burst=2),
                    ScriptedRequest(tick=5, request=[1, 1, 1], burst=2)
                ]
            ),
            ProcessModel(
                pid="P5", priority=4, max_claim=[2, 2, 2], allocation=[0, 0, 0], need=[2, 2, 2],
                execution_time=3,
                scripted_requests=[
                    ScriptedRequest(tick=2, request=[1, 1, 1], burst=3)
                ]
            )
        ]

    elif scenario == ScenarioType.DYNAMIC_DEMAND:
        total_resources = [10, 8, 6]
        processes = [
            ProcessModel(
                pid="P1", priority=5, max_claim=[8, 6, 5], allocation=[0, 0, 0], need=[8, 6, 5],
                execution_time=3,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[1, 1, 0], burst=2),
                    ScriptedRequest(tick=5, request=[4, 3, 2], burst=3),
                    ScriptedRequest(tick=10, request=[2, 1, 2], burst=2)
                ]
            ),
            ProcessModel(
                pid="P2", priority=6, max_claim=[5, 4, 3], allocation=[0, 0, 0], need=[5, 4, 3],
                execution_time=3,
                scripted_requests=[
                    ScriptedRequest(tick=1, request=[3, 2, 1], burst=3),
                    ScriptedRequest(tick=6, request=[1, 1, 1], burst=2),
                    ScriptedRequest(tick=10, request=[1, 1, 1], burst=2)
                ]
            ),
            ProcessModel(
                pid="P3", priority=4, max_claim=[6, 4, 4], allocation=[0, 0, 0], need=[6, 4, 4],
                execution_time=3,
                scripted_requests=[
                    ScriptedRequest(tick=2, request=[2, 1, 1], burst=3),
                    ScriptedRequest(tick=7, request=[3, 2, 2], burst=3)
                ]
            ),
            ProcessModel(
                pid="P4", priority=7, max_claim=[3, 3, 2], allocation=[0, 0, 0], need=[3, 3, 2],
                execution_time=2,
                scripted_requests=[
                    ScriptedRequest(tick=2, request=[1, 1, 1], burst=2),
                    ScriptedRequest(tick=6, request=[2, 1, 1], burst=2)
                ]
            ),
            ProcessModel(
                pid="P5", priority=5, max_claim=[4, 3, 3], allocation=[0, 0, 0], need=[4, 3, 3],
                execution_time=3,
                scripted_requests=[
                    ScriptedRequest(tick=3, request=[2, 1, 1], burst=3)
                ]
            )
        ]
        
    else:
        total_resources = [10, 8, 6]
        processes = []

    return total_resources, processes
