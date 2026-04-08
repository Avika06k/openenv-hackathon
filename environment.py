import subprocess
import uuid
import os
import tempfile
from typing import Dict, Any, List
from models import Action, Observation, State

class CodeFixEnv:
    def __init__(self, task_name: str, buggy_code: str, test_cases: List[str]):
        self.task_name = task_name
        self.buggy_code = buggy_code
        self.test_cases = test_cases
        self.current_code = buggy_code
        self.episode_id = str(uuid.uuid4())
        self.step_count = 0
        self.is_done = False
        self.history = []

    def reset(self) -> Observation:
        self.current_code = self.buggy_code
        self.step_count = 0
        self.is_done = False
        self.history = []
        return Observation(
            output="Environment reset. Buggy code initialized.",
            passed=False,
            reward=0.0
        )

    def _run_tests(self, code: str) -> (bool, str, str):
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "solution.py")
            with open(script_path, "w") as f:
                f.write(code + "\n\n")
                # Append test runner
                f.write("import unittest\n")
                f.write("class TestSolution(unittest.TestCase):\n")
                for i, test in enumerate(self.test_cases):
                    f.write(f"    def test_{i}(self):\n")
                    f.write(f"        {test}\n")
                f.write("\nif __name__ == '__main__':\n")
                f.write("    unittest.main(exit=False)\n")

            try:
                result = subprocess.run(
                    ["python3", script_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                passed = result.returncode == 0
                return passed, result.stdout, result.stderr
            except subprocess.TimeoutExpired:
                return False, "", "Execution timed out."
            except Exception as e:
                return False, "", str(e)

    def step(self, action: Action) -> Observation:
        self.step_count += 1
        
        if action.action_type == "fix_code" and action.code:
            self.current_code = action.code
        
        passed, stdout, stderr = self._run_tests(self.current_code)
        
        reward = 1.0 if passed else -0.1
        if passed:
            self.is_done = True
            
        error_msg = stderr if not passed else None
        
        obs = Observation(
            output=stdout,
            passed=passed,
            error_message=error_msg,
            reward=reward
        )
        
        self.history.append({
            "step": self.step_count,
            "action": action.dict(),
            "observation": obs.dict()
        })
        
        return obs

    @property
    def state(self) -> State:
        return State(
            episode_id=self.episode_id,
            step_count=self.step_count,
            is_done=self.is_done,
            history=self.history
        )
