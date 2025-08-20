DEFAULT_EVALUATION_WEIGHTS = [
    {"name": "Talent DNA", "criterion_type": "TALENT_DNA", "weight": 20.0},
    {
        "name": "Challenges and Behaviors",
        "criterion_type": "CHALLENGES_AND_BEHAVIORS_RESULT",
        "weight": 20.0,
    },
    {"name": "First Interview", "criterion_type": "FIRST_INTERVIEW", "weight": 20.0},
    {
        "name": "Business Case",
        "criterion_type": "BUSINESS_CASE_RESULT",
        "weight": 20.0,
    },
    {"name": "Final Interview", "criterion_type": "FINAL_INTERVIEW", "weight": 20.0},
]


DEFAULT_EVALUATION_WEIGHTS_MEDIUM = [
    {"name": "Talent DNA", "criterion_type": "TALENT_DNA", "weight": 33.3},
    {
        "name": "Challenges and Behaviors",
        "criterion_type": "CHALLENGES_AND_BEHAVIORS_RESULT",
        "weight": 33.3,
    },
    {"name": "Final Interview", "criterion_type": "FINAL_INTERVIEW", "weight": 33.4},
]

DEFAULT_EVALUATION_WEIGHTS_LOW = [
    {"name": "Talent DNA", "criterion_type": "TALENT_DNA", "weight": 33.3},
    {
        "name": "Business Case",
        "criterion_type": "BUSINESS_CASE_RESULT",
        "weight": 33.3,
    },
    {"name": "Final Interview", "criterion_type": "FINAL_INTERVIEW", "weight": 33.4},
]

EVALUATION_WEIGHTS = {
    "HIGH_PROFILE_FLOW": [weight for weight in DEFAULT_EVALUATION_WEIGHTS],
    "MEDIUM_PROFILE_FLOW": [weight for weight in DEFAULT_EVALUATION_WEIGHTS_MEDIUM],
    "LOW_PROFILE_FLOW": [weight for weight in DEFAULT_EVALUATION_WEIGHTS_LOW],
}


DEFAULT_BUSINESS_CONFIGURATION = {
    "evaluation_weights": {
        **EVALUATION_WEIGHTS,
    },
}
