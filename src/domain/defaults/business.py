from src.domain.business import CRITERION_TYPE

DEFAULT_EVALUATION_WEIGHTS = [
    {"name": "Talent DNA", "criterion_type": CRITERION_TYPE.TALENT_DNA, "weight": 20.0},
    {
        "name": "Challenges and Behaviors",
        "criterion_type": CRITERION_TYPE.CHALLENGES_AND_BEHAVIORS_RESULT,
        "weight": 20.0,
    },
    {"name": "First Interview", "criterion_type": CRITERION_TYPE.FIRST_INTERVIEW, "weight": 20.0},
    {
        "name": "Business Case",
        "criterion_type": CRITERION_TYPE.BUSINESS_CASE_RESULT,
        "weight": 20.0,
    },
    {"name": "Final Interview", "criterion_type": CRITERION_TYPE.FINAL_INTERVIEW, "weight": 20.0},
]
