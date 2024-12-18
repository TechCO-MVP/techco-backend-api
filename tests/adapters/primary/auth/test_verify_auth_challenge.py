def test_handler_is_incorrect_answer():
    from src.adapters.primary.auth.verify_auth_challenge import handler

    event = {
        "request": {
            "privateChallengeParameters": {"secretLoginCode": "123456"},
            "challengeAnswer": "123457",
        }
    }
    response = handler(event)

    assert not response


def test_handler_is_correct_answer():
    from src.adapters.primary.auth.verify_auth_challenge import handler

    event = {
        "request": {
            "privateChallengeParameters": {"secretLoginCode": "123456"},
            "challengeAnswer": "123456",
        }
    }
    response = handler(event)

    assert response
