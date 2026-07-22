import re
from typing import Dict, Iterable, List, Optional

try:
    from knowledge.cinemind_knowledge import OUT_OF_SCOPE_RESPONSE, TOPICS
except ModuleNotFoundError:
    from app.knowledge.cinemind_knowledge import OUT_OF_SCOPE_RESPONSE, TOPICS


def normalize_question(question: str) -> str:
    lowered = question.lower().strip()
    return re.sub(r"\s+", " ", lowered)


def _contains_any(text: str, keywords: Iterable[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _last_assistant_topic(messages: Optional[List[Dict[str, str]]]) -> Optional[str]:
    if not messages:
        return None
    for message in reversed(messages):
        topic = message.get("topic")
        if message.get("role") == "assistant" and topic:
            return topic
    return None


def _resolve_follow_up_topic(question: str, messages: Optional[List[Dict[str, str]]]) -> Optional[str]:
    follow_up_terms = {"it", "that", "this", "why", "why did you choose it", "why is it better"}
    if _contains_any(question, follow_up_terms):
        return _last_assistant_topic(messages)
    return None


def find_topic(question: str, messages: Optional[List[Dict[str, str]]] = None) -> Optional[str]:
    normalized = normalize_question(question)

    contextual_topic = _resolve_follow_up_topic(normalized, messages)
    if contextual_topic:
        return contextual_topic

    priority_order = [
        "random_forest",
        "logistic_regression",
        "decision_tree",
        "what_if",
        "evaluation",
        "dataset",
        "budget",
        "popularity",
        "movie_prediction",
        "machine_learning",
        "explainable_ai",
        "application",
    ]
    for topic in priority_order:
        data = TOPICS[topic]
        if _contains_any(normalized, data["keywords"]):
            return topic
    return None


def _format_money(value) -> str:
    try:
        return f"${float(value) / 1_000_000:.1f}M"
    except (TypeError, ValueError):
        return "the submitted budget"


def _latest_prediction_response(question: str, latest_prediction: Optional[Dict]) -> Optional[str]:
    normalized = normalize_question(question)
    contextual_terms = [
        "why",
        "what influenced",
        "influenced",
        "improve",
        "what can i improve",
        "how can i improve",
        "my prediction",
        "my movie",
    ]
    if not _contains_any(normalized, contextual_terms):
        return None

    if not latest_prediction:
        return (
            "Please make a movie prediction first. After that, I can explain why "
            "the result happened, what influenced it, and what you can improve."
        )

    input_data = latest_prediction.get("input_data", {})
    prediction = latest_prediction.get("prediction", "the predicted class")
    probability = latest_prediction.get("probability", 0)
    confidence = latest_prediction.get("confidence", "Unknown")
    probabilities = latest_prediction.get("probabilities", {})

    probability_text = f"{float(probability) * 100:.1f}%" if isinstance(probability, (int, float)) else str(probability)
    genre = input_data.get("genre", "the selected genre")
    budget = _format_money(input_data.get("budget"))
    runtime = input_data.get("runtime", "the submitted runtime")
    release_month = input_data.get("release_month", "the selected release month")
    popularity = input_data.get("popularity_score", "the submitted popularity score")

    if "improve" in normalized:
        return (
            f"Your latest movie was predicted as {prediction} with {probability_text} probability "
            f"and {confidence} confidence. To improve the predicted outcome, experiment in the "
            f"What-If Simulator with higher popularity, a stronger budget, a suitable runtime, "
            f"and a release month that historically performs well for {genre} movies."
        )

    probability_lines = ""
    if probabilities:
        formatted = [f"{label}: {float(score) * 100:.1f}%" for label, score in probabilities.items()]
        probability_lines = " Class probabilities were " + ", ".join(formatted) + "."

    return (
        f"Your latest movie was predicted as {prediction} with {probability_text} probability "
        f"and {confidence} confidence. The model considered Genre: {genre}, Budget: {budget}, "
        f"Runtime: {runtime} minutes, Release Month: {release_month}, and Popularity: {popularity}."
        f"{probability_lines} The Explainable AI section shows which of these features contributed most."
    )


def get_chatbot_response(
    question: str,
    messages: Optional[List[Dict[str, str]]] = None,
    latest_prediction: Optional[Dict] = None,
) -> Dict[str, Optional[str]]:
    if not question or not question.strip():
        return {"answer": "Please type a CineMind AI question so I can help.", "topic": None}

    latest_prediction_answer = _latest_prediction_response(question, latest_prediction)
    if latest_prediction_answer:
        return {"answer": latest_prediction_answer, "topic": "movie_prediction"}

    topic = find_topic(question, messages)
    if topic:
        return {"answer": TOPICS[topic]["response"], "topic": topic}

    return {"answer": OUT_OF_SCOPE_RESPONSE, "topic": None}
