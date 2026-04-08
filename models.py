from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Action(BaseModel):
    action_type: str  # e.g., "fix_code", "add_test", "run_tests"
    code: Optional[str] = None
    test_case: Optional[str] = None

class Observation(BaseModel):
    output: str
    passed: bool
    error_message: Optional[str] = None
    reward: float

class State(BaseModel):
    episode_id: str
    step_count: int
    is_done: bool
    history: List[Dict[str, Any]]
