def test_handler_is_correct_answer():
    from src.adapters.primary.auth.define_auth_challenge import handler

    event = {
        "request": {"session": [{"challengeResult": True, "challengeName": "CUSTOM_CHALLENGE"}]},
        "response": {},
    }
    response = handler(event, {})

    print(response)
    assert response["response"]["issueTokens"]
    assert not response["response"]["failAuthentication"]


def test_handler_is_incorrect_answer():
    from src.adapters.primary.auth.define_auth_challenge import handler

    event = {
        "request": {"session": [{"challengeResult": False, "challengeName": "CUSTOM_CHALLENGE"}]},
        "response": {},
    }
    response = handler(event, {})

    assert not response["response"]["issueTokens"]
    assert not response["response"]["failAuthentication"]
    assert response["response"]["challengeName"] == "CUSTOM_CHALLENGE"


def test_handler_exceed_max_attempts():
    from src.adapters.primary.auth.define_auth_challenge import handler

    event = {
        "request": {
            "session": [
                {"challengeResult": False},
                {"challengeResult": False},
                {"challengeResult": False},
            ]
        },
        "response": {},
    }
    response = handler(event, {})

    assert response["response"]["failAuthentication"]
    assert not response["response"]["issueTokens"]


def test_handler_is_not_custom_challenge():
    from src.adapters.primary.auth.define_auth_challenge import handler

    event = {"request": {"session": [{"challengeName": "NOT_CUSTOM_CHALLENGE"}]}, "response": {}}
    response = handler(event, {})
    assert response["response"]["failAuthentication"]
    assert not response["response"]["issueTokens"]


def test_is_custom_challenge_no_session():
    from src.adapters.primary.auth.define_auth_challenge import is_custom_challenge

    event = {"request": {"session": []}}
    assert is_custom_challenge(event)


def test_exceed_max_attempts_challenge_first_attempt():
    from src.adapters.primary.auth.define_auth_challenge import exceed_max_attempts

    event = {"request": {"session": [{"challengeResult": False}]}}
    assert not exceed_max_attempts(event)


def test_exceed_max_attempts_challenge_last_attempt_succeeded():
    from src.adapters.primary.auth.define_auth_challenge import exceed_max_attempts

    event = {
        "request": {
            "session": [
                {"challengeResult": False},
                {"challengeResult": False},
                {"challengeResult": True},
            ]
        }
    }
    assert not exceed_max_attempts(event)


def test_exceed_max_attempts_challenge_last_attempt_failed():
    from src.adapters.primary.auth.define_auth_challenge import exceed_max_attempts

    event = {
        "request": {
            "session": [
                {"challengeResult": False},
                {"challengeResult": False},
                {"challengeResult": False},
            ]
        }
    }
    assert exceed_max_attempts(event)


def test_exceed_max_attempts_challenge_max_attempts():
    from src.adapters.primary.auth.define_auth_challenge import exceed_max_attempts

    event = {
        "request": {
            "session": [
                {"challengeMetadata": "2"},
                {"challengeMetadata": "3"},
                {"challengeMetadata": "4"},
            ]
        }
    }
    assert exceed_max_attempts(event)


def test_exceed_max_attempts_no_session():
    from src.adapters.primary.auth.define_auth_challenge import exceed_max_attempts

    event = {"request": {"session": []}}
    assert not exceed_max_attempts(event)


def test_is_custom_challenge_challenge_name_custom():
    from src.adapters.primary.auth.define_auth_challenge import is_custom_challenge

    event = {"request": {"session": [{"challengeName": "CUSTOM_CHALLENGE"}]}}
    assert is_custom_challenge(event)


def test_is_correct_answer_challenge_name_not_custom():
    from src.adapters.primary.auth.define_auth_challenge import is_custom_challenge

    event = {"request": {"session": [{"challengeName": "NOT_CUSTOM_CHALLENGE"}]}}
    assert not is_custom_challenge(event)


def test_is_correct_answer_challenge_failed():
    from src.adapters.primary.auth.define_auth_challenge import is_correct_answer

    event = {"request": {"session": [{"challengeResult": False}]}}
    assert not is_correct_answer(event)


def test_is_correct_answer_no_session():
    from src.adapters.primary.auth.define_auth_challenge import is_custom_challenge

    event = {"request": {"session": []}}
    assert is_custom_challenge(event)
