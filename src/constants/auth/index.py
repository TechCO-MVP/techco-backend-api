EMAIL_OTP_TEMPLATE = """
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
        text-align: center;
        }
        .logo {
        height: 40px;
        display: block;
        margin: 0 auto;
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

LOGO_HEADER_URL = "https://dev-techco-public-data-us-east-1.s3.us-east-1.amazonaws.com/Talent_connect_white_logo.png"
