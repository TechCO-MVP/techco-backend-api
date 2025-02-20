""" this module is responsible for veryfy otp code for the authentication passwordless process """

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError

from src.use_cases.user.get_user_by_mail import get_user_by_mail_use_case
from src.domain.user import UserDTO, UserStatus
from src.domain.role import BusinessRole, Role
from src.domain.user import UpdateUserStatusDTO
from src.use_cases.user.update_user_status import put_user_status_use_case
from src.constants.index import CLIENT_ID, REGION_NAME

cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/auth/verify_auth_otp_code")
def verify_auth_otp_code():
    """
    send request to cognito to verify the otp code authentication process
    """
    body = app.current_event.json_body
    user_email = body["email"]
    otp_code = body["otp"]
    session = body["session"]
    status_code = 400
    body = {}

    try:
        user = get_user_by_mail_use_case(user_email)

        if user.props.status == UserStatus.PENDING:
            user_update_dto = UpdateUserStatusDTO(
                user_id=user.id,
                user_status=UserStatus.ENABLED,
                user_email=user_email
            )
            put_user_status_use_case(user_update_dto)

        response = cognito_client.respond_to_auth_challenge(
            ClientId=CLIENT_ID,
            ChallengeName="CUSTOM_CHALLENGE",
            ChallengeResponses={"USERNAME": user_email, "ANSWER": otp_code},
            Session=session,
        )

        if "AuthenticationResult" in response:
            body = {
                "message": "Successfully authenticated.",
                "idToken": response["AuthenticationResult"]["IdToken"],
                "accessToken": response["AuthenticationResult"]["AccessToken"],
                "refreshToken": response["AuthenticationResult"]["RefreshToken"],
            }
            status_code = 200
        else:
            body = {"message": "Invalid OTP code."}

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        body["error"] = f"Error validating OTP code: {error_message}"

    except Exception as e:
        status_code = 500
        body = {"error": f"Unexpected error: {str(e)}"}

    finally:
        return Response(status_code, body=body, content_type=content_types.APPLICATION_JSON)


@logger.inject_lambda_context
def lambda_handler(event, context: LambdaContext) -> dict:
    """
    Handler function
    event: The event object, described like:
    {
        "httpMethod": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": {"email": "test", "otp": "123456", "session": "session"}
    }
    """
    return app.resolve(event, context)
