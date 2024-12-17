def test_handler():
    from src.adapters.primary.auth.pre_signup import handler

    event = {
        "request": {"userAttributes": {"username": "username", "email": "email"}},
        "response": {},
    }
    response = handler(event, {})

    assert response["response"]["autoConfirmUser"]
    assert not response["response"]["autoVerifyEmail"]
    assert response == {
        "request": {"userAttributes": {"username": "username", "email": "email"}},
        "response": {"autoConfirmUser": True, "autoVerifyEmail": False},
    }
