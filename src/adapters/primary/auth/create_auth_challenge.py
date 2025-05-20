import random

import boto3

from src.constants.index import EMAIL_OTP, REGION_NAME
from src.use_cases.user.get_user_by_mail import get_user_by_mail_use_case


LOGO_HEADER_URL = "data:image/png;base64,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"  # Reemplazar con tu URL real
LOGO_BODY_URL = "data:image/png;base64,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"     # Reemplazar con tu URL real


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
    html_content = emil_template_otp.replace("{{OTP}}", secret_code)
    html_content = html_content.replace("{{name}}", user_name)
    html_content = html_content.replace("[URL_DEL_LOGO_HEADER]", LOGO_HEADER_URL)
    html_content = html_content.replace("[URL_DEL_LOGO_BODY]", LOGO_BODY_URL)
    
    ses_client.send_email(
        Source=EMAIL_OTP,
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": "Tu Código OTP - Talent Connect"},
            "Body": {
                "Html": {"Data": html_content},
                "Text": {"Data": f"Tu código OTP es: {secret_code}"}
            },
        },
    )

emil_template_otp = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Talent Connect - Tu Código OTP</title>
    <style>
        body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f5f5f5;
        }
        .container {
        max-width: 600px;
        margin: 0 auto;
        background-color: #ffffff;
        }
        .header {
        position: relative;
        height: 64px;
        background: linear-gradient(90deg, #004D40, #00695C, #00796B);
        }
        .header-line {
        height: 4px;
        background-color: #FFC107;
        }
        .logo-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        }
        .logo {
        height: 40px;
        }
        .body {
        padding: 32px;
        }
        .content {
        max-width: 400px;
        margin: 0 auto;
        }
        .centered-logo {
        text-align: center;
        margin-bottom: 32px;
        }
        .centered-logo img {
        height: 28px;
        }
        .greeting {
        font-size: 18px;
        font-weight: 500;
        margin-bottom: 24px;
        }
        .otp-container {
        background-color: #f5f5f5;
        padding: 24px;
        border-radius: 6px;
        text-align: center;
        margin-bottom: 24px;
        }
        .otp-label {
        font-size: 14px;
        color: #666666;
        margin-bottom: 8px;
        }
        .otp-code {
        font-size: 28px;
        font-weight: bold;
        letter-spacing: 2px;
        color: #00796B;
        }
        .message {
        color: #333333;
        line-height: 1.5;
        }
        .message p {
        margin-bottom: 16px;
        }
        .footer {
        height: 48px;
        background: linear-gradient(90deg, #004D40, #00695C, #00796B);
        display: flex;
        justify-content: center;
        align-items: center;
        }
        .footer-text {
        color: white;
        font-size: 12px;
        }
        .bold {
        font-weight: bold;
        }
    </style>
    </head>
    <body>
    <div class="container">
        <div class="header">
        <div class="logo-container">
            <img src="[URL_DEL_LOGO_HEADER]" alt="Talent Connect Logo" class="logo">
        </div>
        </div>
        <div class="header-line"></div>
        <div class="body">
        <div class="content">
            <div class="centered-logo">
            <img src="[URL_DEL_LOGO_BODY]" alt="Talent Connect Logo">
            </div>
            
            <div class="greeting">¡Ey, <span class="bold">{{name}}</span>! Todo listo para volver 👇</div>
            
            <div class="otp-container">
            <div class="otp-label">Tu código OTP es:</div>
            <div class="otp-code">{{OTP}}</div>
            </div>
            
            <div class="message">
            <p>Escríbelo y en segundos estarás de vuelta al mando de tus vacantes.</p>
            
            <p>¿No fuiste tú quien solicitó el código? Ignora este mensaje 😉</p>
            
            <p>¡Nos encanta verte de nuevo!</p>
            
            <p class="bold">Equipo Talent Connect</p>
            </div>
        </div>
        </div>
        <div class="footer">
        <div class="footer-text">© 2025 Talent Connect. Todos los derechos reservados.</div>
        </div>
    </div>
    </body>
    </html>
"""