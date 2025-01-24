import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError

from src.constants.index import CLIENT_ID, REGION_NAME


cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)

logger = Logger()
app = APIGatewayRestResolver()

@app.post("/auth/refresh_tokens")
def refresh_tokens():
    """
    Lambda function to refresh Cognito tokens using the refresh token.
    """
    json_body = app.current_event.json_body
    refresh_token = json_body["refresh_token"]
    status_code = 200
    body = {}
    
    try:
        response = cognito_client.initiate_auth(
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token
            },
            ClientId=CLIENT_ID,
        )

        body = {
            "message": "Tokens refreshed successfully",
            "body": {
                "id_token": response["AuthenticationResult"]["IdToken"],
                "access_token": response["AuthenticationResult"]["AccessToken"],
                "expires_in": response["AuthenticationResult"]["ExpiresIn"],
            }
        }

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        status_code = 500
        body = {"message": f"Failed to refresh tokens: {error_message}"}
    
    finally:
        return Response(status_code, body=body, content_type=content_types.APPLICATION_JSON)


@logger.inject_lambda_context
def lambda_handler(request: dict, context: LambdaContext) -> dict:
    """
    Handler function
    request: The request object, described like:
    {
        "httpMethod": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": {"refresh_token": "refresh-token"}
    }
    context: LambdaContext object
    """
    return app.resolve(request, context)