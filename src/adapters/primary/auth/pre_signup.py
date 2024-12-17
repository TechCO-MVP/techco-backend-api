def handler(event, _):
    """
    Pre-signup
    event: The event object, described like:
    {
        "request": {
            "userAttributes": {
                "username": "username",
                "email": "email"
            }
        }
    }
    """
    event["response"]["autoConfirmUser"] = True
    event["response"]["autoVerifyEmail"] = False
    return event
