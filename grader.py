def grade_survival(history) -> float:
    # Goal: survive 30 steps
    steps = len(history)
    if steps == 0:
        return 0.0
    return min(1.0, steps / 30.0)

def grade_growth(history) -> float:
    # Goal: reach 1000 users
    if not history:
        return 0.0
    final_state = history[-1]["state"]
    users = final_state.get("users", 0)
    return min(1.0, users / 1000.0)

def grade_scaling(history) -> float:
    # Goal: maximize profit efficiency
    # Simple metric: compare final cash vs starting cash (50000) with a target profit.
    if not history:
        return 0.0
    final_state = history[-1]["state"]
    cash = final_state.get("cash", 0)
    profit = cash - 50000.0
    # Target profit of 50,000 to get a perfect score
    if profit <= 0:
        return 0.0
    return min(1.0, profit / 50000.0)


def evaluate(task_name: str, history: list) -> float:
    if task_name == "survival":
        return grade_survival(history)
    elif task_name == "growth":
        return grade_growth(history)
    elif task_name == "scaling":
        return grade_scaling(history)
    return 0.0
