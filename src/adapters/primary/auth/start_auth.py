""" this module is responsible for starting the authentication passwordless process """

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError

from src.constants.index import CLIENT_ID, REGION_NAME
from src.use_cases.user.get_user_by_mail import get_user_by_mail_use_case
from src.domain.user import UserStatus
from src.errors.entity_not_found import EntityNotFound

cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/auth/start_auth")
def start_auth():
    """
    send request to cognito to start the authentication process
    """
    logger.info("User strat authentication")
    json_body = app.current_event.json_body
    user_email = json_body["email"]
    client_id = CLIENT_ID
    status_code = 400
    body = {}

    try:
        user = get_user_by_mail_use_case(user_email)

        if user.props.status == UserStatus.DISABLED:
            body = {"message": "User is not enabled."}
            return

        status_code, body = initiate_auth(user_email, client_id)

    except EntityNotFound as e:
        logger.info(f"{str(e)} in DB")
        status_code, body = initiate_auth(user_email, client_id)

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        body = {"error": f"Failed to start authentication: {error_message}"}

    except Exception as e:
        status_code = 500
        body = {"error": f"Unexpected error: {str(e)}"}

    finally:
        return Response(status_code, body=body, content_type=content_types.APPLICATION_JSON)

def initiate_auth(user_email: str, client_id: str):
    response = cognito_client.initiate_auth(
        AuthFlow="CUSTOM_AUTH", AuthParameters={"USERNAME": user_email}, ClientId=client_id
    )
    session = response["Session"]
    status_code = 200
    body = {"message": "OTP sent successfully.", "body": {"session": session}}

    return status_code, body

@logger.inject_lambda_context
def lambda_handler(request: dict, context: LambdaContext) -> dict:
    """
    Handler function
    request: The request object, described like:
    {
        "httpMethod": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": {"email": "fake@mail.com"}
    }
    context: LambdaContext object
    """
    return app.resolve(request, context)
