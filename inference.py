state = {
    "step": 0,
    "done": False
}

def reset_env():
    state["step"] = 0
    state["done"] = False
    return {
        "observation": "environment reset",
        "reward": 0.0,
        "done": False
    }

def step_env():
    if state["done"]:
        return {
            "observation": "already finished",
            "reward": 1.0,
            "done": True
        }

    state["step"] += 1
    state["done"] = True

    return {
        "observation": "code fixed successfully",
        "reward": 1.0,
        "done": True
    }
