import random

import boto3

from src.constants.index import EMAIL_OTP, REGION_NAME
from src.constants.auth.index import EMAIL_OTP_TEMPLATE, LOGO_HEADER_URL, LOGO_BODY_URL
from src.use_cases.user.get_user_by_mail import get_user_by_mail_use_case


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
    user_entity = get_user_by_mail_use_case(email)
    user_name = user_entity.props.full_name

    send_otp_email(email, user_name, secret_code)
    return event


def generate_secret_code() -> str:
    """
    Generate a secret code
    return: The secret code
    """
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


def send_otp_email(email, user_name, secret_code):
    """
    Send the OTP email
    email: The email address
    secret_code: The secret code
    """
    ses_client = boto3.client("ses", region_name=REGION_NAME)

    # Reemplazar las variables en el template
    html_company_image = """<img src="[URL_DEL_LOGO_BODY]" alt="Talent Connect Logo">"""
    company_image = LOGO_BODY_URL

    if company_image:
        html_company_image = html_company_image.replace("[URL_DEL_LOGO_BODY]", company_image)
    else:
        html_company_image = ""

    email_template = EMAIL_OTP_TEMPLATE
    email_template = email_template.replace("{{OTP}}", secret_code)
    email_template = email_template.replace("{{name}}", user_name)
    email_template = email_template.replace("[URL_DEL_LOGO_HEADER]", LOGO_HEADER_URL)
    html_content = email_template.replace('<img src="[URL_DEL_LOGO_BODY]" alt="Talent Connect Logo">', html_company_image)
    
    ses_client.send_email(
        Source=EMAIL_OTP,
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": "Tu Código OTP - Talent Connect"},
            "Body": {
                "Html": {"Data": html_content}
            },
        },
    )
