WELCOME_MESSAGE = """👋 Hello! I'm the CineMind AI Assistant.

I can help you understand:

• Movie Success Prediction
• Explainable AI
• Dataset
• Random Forest
• Machine Learning
• Feature Importance
• Evaluation Metrics
• This Application

Ask me anything related to CineMind AI."""


OUT_OF_SCOPE_RESPONSE = """I'm the CineMind AI Assistant.

I can only answer questions related to:

• Movie Success Prediction
• Machine Learning
• Dataset
• Explainable AI
• CineMind AI

Please ask a question about the application."""


TOPICS = {
    "movie_prediction": {
        "keywords": [
            "prediction",
            "predict",
            "predicted",
            "hit",
            "flop",
            "average",
            "success",
            "probability",
            "box office",
            "movie outcome",
        ],
        "response": (
            "CineMind AI predicts movie success as Hit, Average, or Flop using the "
            "movie's genre, budget, runtime, release month, and popularity score. "
            "The trained model compares those values with patterns learned from "
            "historical movie data, then returns the most likely class and its "
            "prediction probability."
        ),
    },
    "explainable_ai": {
        "keywords": [
            "explainable",
            "xai",
            "explain",
            "why",
            "feature importance",
            "importance",
            "influenced",
            "influence",
            "contribution",
        ],
        "response": (
            "Explainable AI shows which input features had the strongest effect on "
            "the prediction. In CineMind AI, feature importance helps explain how "
            "genre, budget, runtime, release month, and popularity contributed to "
            "the final result."
        ),
    },
    "budget": {
        "keywords": ["budget", "production cost", "cost", "spending"],
        "response": (
            "Budget matters because production spending often affects scale, cast, "
            "marketing potential, and audience reach. The model uses budget as one "
            "signal, but it does not decide success by budget alone."
        ),
    },
    "popularity": {
        "keywords": ["popularity", "popular", "audience interest", "hype", "demand"],
        "response": (
            "Popularity represents audience interest or market attention. A higher "
            "popularity score can increase the model's confidence because movies "
            "with stronger audience demand often perform better."
        ),
    },
    "machine_learning": {
        "keywords": [
            "machine learning",
            "ml",
            "classification",
            "supervised",
            "algorithm",
            "model",
        ],
        "response": (
            "Machine learning lets the application learn patterns from historical "
            "movie data. CineMind AI uses supervised classification because the "
            "training examples include known success labels: Hit, Average, and Flop."
        ),
    },
    "random_forest": {
        "keywords": [
            "random forest",
            "forest",
            "rf",
            "why did you choose it",
            "why choose it",
            "better",
        ],
        "response": (
            "Random Forest is an ensemble algorithm that combines many decision "
            "trees. It is useful here because it can model non-linear patterns, "
            "handle mixed feature types after preprocessing, and usually gives more "
            "stable predictions than a single decision tree."
        ),
    },
    "decision_tree": {
        "keywords": ["decision tree", "tree model", "tree"],
        "response": (
            "A Decision Tree makes predictions through a sequence of feature-based "
            "rules. It is easy to understand, but a single tree can overfit, which "
            "is why Random Forest often performs more reliably."
        ),
    },
    "logistic_regression": {
        "keywords": ["logistic regression", "logistic"],
        "response": (
            "Logistic Regression is a classification algorithm that estimates class "
            "probabilities from weighted input features. It is simple and useful as "
            "a baseline model for comparing more flexible algorithms."
        ),
    },
    "dataset": {
        "keywords": [
            "dataset",
            "data",
            "features",
            "columns",
            "target",
            "genre",
            "runtime",
            "release month",
        ],
        "response": (
            "The dataset is a structured movie dataset. CineMind AI uses five input "
            "features: genre, budget, runtime, release month, and popularity score. "
            "The target variable is movie success, represented as Hit, Average, or Flop."
        ),
    },
    "evaluation": {
        "keywords": [
            "accuracy",
            "precision",
            "recall",
            "f1",
            "f1 score",
            "confusion matrix",
            "metrics",
            "evaluation",
        ],
        "response": (
            "Model evaluation measures how well the classifier performs. Accuracy "
            "shows overall correctness, precision measures how reliable positive "
            "predictions are, recall measures how many true cases are found, F1 Score "
            "balances precision and recall, and the confusion matrix shows correct "
            "and incorrect predictions by class."
        ),
    },
    "what_if": {
        "keywords": [
            "what-if",
            "what if",
            "simulator",
            "simulation",
            "change budget",
            "change popularity",
            "improve",
        ],
        "response": (
            "The What-If Simulator lets you change movie inputs and compare the new "
            "prediction with the original one. It is useful for testing how budget, "
            "popularity, runtime, genre, or release month may affect the predicted outcome."
        ),
    },
    "application": {
        "keywords": [
            "cinemind",
            "application",
            "app",
            "technologies",
            "technology",
            "who should use",
            "problem",
            "limitations",
        ],
        "response": (
            "CineMind AI helps students, analysts, producers, and decision-makers "
            "explore movie success prediction with machine learning. It is built with "
            "Python, Streamlit, scikit-learn, Pandas, NumPy, and Plotly. Its limitation "
            "is that predictions depend on the available historical data and selected features."
        ),
    },
}


CONTEXT_HINTS = {
    "random_forest": {"it", "that model", "why did you choose it", "why is it better"},
    "movie_prediction": {"why", "why this", "why that", "what happened"},
}
