import sys
sys.path.append('backend')
from simulation.engine import SimulationEngine
from models.state import AlgorithmType, ScenarioType

ec = SimulationEngine(scenario=ScenarioType.STARVATION, algorithm=AlgorithmType.CLASSICAL)
ea = SimulationEngine(scenario=ScenarioType.STARVATION, algorithm=AlgorithmType.ADAPTIVE)

print("=== CLASSICAL STEP BY STEP ===")
for t in range(1, 15):
    state = ec.step()
    print(f"--- TICK {t} --- Available: {state.available_resources}")
    for e in state.events:
        if e.tick == t and e.event_type in ('GRANT', 'RANKING', 'DEFERRED', 'UNSAFE', 'REQUEST'):
            print(f"  {e.pid}: {e.event_type} - {e.message}")
    if all(p.state == 'COMPLETED' for p in state.processes):
        break

print("\n=== ADAPTIVE STEP BY STEP ===")
for t in range(1, 15):
    state = ea.step()
    print(f"--- TICK {t} --- Available: {state.available_resources}")
    for e in state.events:
        if e.tick == t and e.event_type in ('GRANT', 'RANKING', 'DEFERRED', 'UNSAFE', 'REQUEST'):
            print(f"  {e.pid}: {e.event_type} - {e.message}")
    if all(p.state == 'COMPLETED' for p in state.processes):
        break
