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


DEFAULT_BUSINESS_CONFIGURATION = {
    "evaluation_weights": DEFAULT_EVALUATION_WEIGHTS,
}
