from src.scenario_simulator import create_scenario_input


def test_create_scenario_input_adjusts_budget_and_popularity():
    base_input = {
        "genre": "Action",
        "budget": 50000000,
        "runtime": 120,
        "release_month": 6,
        "popularity_score": 50,
    }

    scenario = create_scenario_input(
        base_input,
        budget_change=10000000,
        popularity_change=10,
        runtime_change=10,
        release_month_shift=1,
    )

    assert scenario["budget"] == 60000000
    assert scenario["popularity_score"] == 60.0
    assert scenario["runtime"] == 130
    assert scenario["release_month"] == 7
