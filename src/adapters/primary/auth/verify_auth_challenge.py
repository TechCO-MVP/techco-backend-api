def handler(event, _):
    """
    Verify the custom challenge
    event: The event object, described like:
    {
        "request": {
            "privateChallengeParameters": {
                "secretLoginCode": "123456"
            },
            "challengeAnswer": "123456"
        }
    }
    """
    expected_otp = event["request"]["privateChallengeParameters"]["secretLoginCode"]
    answer = event["request"]["challengeAnswer"]
    event["response"]["answerCorrect"] = expected_otp == answer

    return event
