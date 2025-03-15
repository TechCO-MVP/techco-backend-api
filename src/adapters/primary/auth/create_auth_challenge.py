import random

import boto3

from src.constants.index import EMAIL_OTP, REGION_NAME


def handler(event, _):
    """
    Create a custom challenge
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
    secret_code = generate_secret_code()

    email = event["request"]["userAttributes"]["email"]
    event["response"]["publicChallengeParameters"] = {"email": email}
    event["response"]["privateChallengeParameters"] = {"secretLoginCode": secret_code}
    event["response"]["challengeMetadata"] = f"CODE-{secret_code}"

    send_otp_email(email, secret_code)
    return event


def generate_secret_code() -> str:
    """
    Generate a secret code
    return: The secret code
    """
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


def send_otp_email(email, secret_code):
    """
    Send the OTP email
    email: The email address
    secret_code: The secret code
    """
    ses_client = boto3.client("ses", region_name=REGION_NAME)
    ses_client.send_email(
        Source=EMAIL_OTP,
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": "Your OTP Code"},
            "Body": {"Text": {"Data": f"Your OTP code is: {secret_code}"}},
        },
    )
