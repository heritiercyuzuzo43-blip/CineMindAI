from app.services.chatbot_engine import get_chatbot_response


def test_chatbot_answers_random_forest_synonyms():
    result = get_chatbot_response("Tell me about Random Forest.")

    assert result["topic"] == "random_forest"
    assert "ensemble" in result["answer"]


def test_chatbot_prioritizes_specific_model_topic_over_generic_explain_wording():
    result = get_chatbot_response("Explain Random Forest.")

    assert result["topic"] == "random_forest"


def test_chatbot_refuses_unrelated_questions():
    result = get_chatbot_response("Who is Cristiano Ronaldo?")

    assert result["topic"] is None
    assert "I can only answer questions related to" in result["answer"]


def test_chatbot_uses_latest_prediction_context():
    latest_prediction = {
        "prediction": "Hit",
        "probability": 0.82,
        "confidence": "High",
        "input_data": {
            "genre": "Action",
            "budget": 80000000,
            "runtime": 140,
            "release_month": 7,
            "popularity_score": 78,
        },
        "probabilities": {"Hit": 0.82, "Average": 0.12, "Flop": 0.06},
    }

    result = get_chatbot_response("Why?", latest_prediction=latest_prediction)

    assert result["topic"] == "movie_prediction"
    assert "Hit" in result["answer"]
    assert "82.0%" in result["answer"]
