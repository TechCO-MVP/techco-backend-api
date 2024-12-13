CHALLENGE_NAME = "CUSTOM_CHALLENGE"


def handler(event, _):
    """
    Define the custom challenge
    event: The event object, described like:
    {
        "request": {
            "session": [
                {
                    "challengeName": "CUSTOM_CHALLENGE",
                    "challengeResult": Boolean
                },
                ...
            ]
        }
    }
    """
    if not is_custom_challenge(event):
        event["response"]["issueTokens"] = False
        event["response"]["failAuthentication"] = True

    elif exceed_max_attempts(event):
        event["response"]["issueTokens"] = False
        event["response"]["failAuthentication"] = True

    elif is_correct_answer(event):
        event["response"]["issueTokens"] = True
        event["response"]["failAuthentication"] = False

    else:
        event["response"]["issueTokens"] = False
        event["response"]["failAuthentication"] = False
        event["response"]["challengeName"] = CHALLENGE_NAME

    return event


def is_custom_challenge(event):
    """
    Check if the current challenge is a custom challenge
    event: The event object, described like:
    {
        "request": {
            "session": [
                {
                    "challengeName": "CUSTOM_CHALLENGE",
                    "challengeResult": False
                },
                ...
            ]
        }
    }
    return: True if the current challenge is a custom challenge, False otherwise
    """
    session = event["request"]["session"]
    if not session:
        return True  # If there is no session, it is a new session

    is_custom_challenge = next(
        (True for attempt in session if attempt.get("challengeName") == CHALLENGE_NAME), False
    )
    return is_custom_challenge


def exceed_max_attempts(event):
    """
    Check if the user has exceeded the maximum number of attempts (3)
    event: The event object, described like:
    {
        "request": {
            "session": [
                {
                    "challengeName": "CUSTOM_CHALLENGE",
                    "challengeResult": False
                },
                ...
            ]
        }
    }
    """

    session = event["request"]["session"]
    if not session:
        return False  # If there is no session, it is a new session

    attempt_count = len(session)
    last_attempt_result = session[-1].get("challengeResult")

    return attempt_count >= 3 and not last_attempt_result


def is_correct_answer(event):
    """
    Check if the user has answered the challenge correctly
    event: The event object, described like:
    {
        "request": {
            "session": [
                {
                    "challengeName": "CUSTOM_CHALLENGE",
                    "challengeResult": False
                },
                ...
            ]
        }
    }
    return: True if the user has answered the challenge correctly, False otherwise
    """
    session = event["request"]["session"]
    if not session:
        return False

    last_attempt = session[-1]

    return (
        last_attempt.get("challengeResult") and last_attempt.get("ChallengeName") == CHALLENGE_NAME
    )
