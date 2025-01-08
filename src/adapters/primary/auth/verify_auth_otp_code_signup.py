from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError

from src.domain.business import BusinessDTO
from src.domain.user import UserDTO, UserStatus
from src.use_cases.business.create_admin_business import crete_admin_business_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/auth/verify_auth_otp_code_signup")
def verify_auth_otp_code_signup():
    """
    send request to cognito to verify the otp code authentication process
    """
    body = app.current_event.json_body
    print(body)
    email = body["email"]
    otp = body["otp"]
    session = body["session"]
    status_code = 400
    response_body = {}

    try:
        user_dto = UserDTO(
            email=email,
            role=body["role"],
            business_id="",
            status=UserStatus.ENABLED,
        )

        business_dto = BusinessDTO(
            name=body["company_name"],
            country_code=body["country_code"],
            company_size=body["company_size"],
            is_admin=True,
        )

        result = crete_admin_business_use_case(business_dto, user_dto, otp, session)

        status_code = 200
        response_body = {
            "message": "Successfully authenticated.",
            "body": result,
        }
    except ValueError as e:
        response_body["error"] = str(e)

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        response_body["error"] = f"Error validating OTP code: {error_message}"

    except Exception as e:
        status_code = 500
        response_body = {"error": f"Unexpected error: {str(e)}"}

    finally:
        return Response(
            status_code, body=response_body, content_type=content_types.APPLICATION_JSON
        )


@logger.inject_lambda_context
def handler(event, context: LambdaContext) -> dict:
    """
    Handler function for verifying the OTP code for signup
    this event should create the business, the user and should return a session token
    event: The request object, described like:
    {
        "body": {
            "session": "string"
            "otp": "string",
            "email": "string",
            "company_name": "string",
            "country_code": "string",
            "company_size": "string",
            "role": "string"
        }
    }
    """
    return app.resolve(event, context)
