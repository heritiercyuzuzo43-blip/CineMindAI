from app.components.ai_processing_engine import build_engine_steps


def test_build_engine_steps_contains_expected_pipeline_stages():
    steps = build_engine_steps()

    assert [step["console"] for step in steps] == [
        "Loading trained Random Forest model...",
        "Validating user input...",
        "Encoding categorical features...",
        "Preparing numerical features...",
        "Running prediction model...",
        "Calculating prediction probabilities...",
        "Building Explainable AI report...",
    ]
    assert [step["progress"] for step in steps] == [10, 25, 40, 55, 70, 85, 100]
