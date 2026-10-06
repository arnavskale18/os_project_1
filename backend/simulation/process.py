from typing import List, Optional
from models.state import ProcessModel, ProcessState, ScriptedRequest

class Process:
    """Helper wrapper around ProcessModel for simulation logic."""
    def __init__(self, model: ProcessModel):
        self.model = model

    @property
    def pid(self) -> str:
        return self.model.pid

    @property
    def state(self) -> ProcessState:
        return self.model.state

    @state.setter
    def state(self, value: ProcessState):
        self.model.state = value

    def reset(self):
        self.model.allocation = [0] * len(self.model.max_claim)
        self.model.need = list(self.model.max_claim)
        self.model.waiting_time = 0
        self.model.execution_time = 3
        self.model.remaining_execution_time = 0
        self.model.request_history = []
        self.model.predicted_demand = []
        self.model.estimated_demand = []
        self.model.aging_score = 0.0
        self.model.state = ProcessState.READY
        self.model.current_request = None
