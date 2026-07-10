def create_scenario_input(base_input, budget_change=0, popularity_change=0, runtime_change=0, release_month_shift=0):
    scenario = dict(base_input)
    scenario["budget"] = base_input["budget"] + budget_change
    scenario["popularity_score"] = base_input["popularity_score"] + popularity_change
    scenario["runtime"] = base_input["runtime"] + runtime_change
    scenario["release_month"] = max(1, min(12, base_input["release_month"] + release_month_shift))
    return scenario
