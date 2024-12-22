""" this module is responsible for finish session for user """

import json
import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.constants.index import REGION_NAME

cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/auth/sign_out")
def sign_out():
    """send request to cognito to signout the user"""
    logger.info("Signing out user")
    status_code = 401
    body = {}

    json_body = app.current_event.json_body
    access_token = json_body.get("access_token")

    try:
        cognito_client.global_sign_out(AccessToken=access_token)
        status_code = 200
        body["message"] = "User successfully signed out."

    except cognito_client.exceptions.NotAuthorizedException as e:
        logger.info(e)
        status_code = 401
        body["message"] = "Unauthorized: Invalid or expired token."

    except Exception:
        logger.exception("An error occurred")
        status_code = 500
        body["message"] = "An error occurred"

    finally:
        return Response(status_code, content_type="application/json", body=body)


@logger.inject_lambda_context
def lambda_handler(request: dict, context: LambdaContext) -> dict:
    """
    Handler function
    request: The request object, described like:
    {
        "httpMethod": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": {"access_token": "token"}
    }
    context: LambdaContext object
    """
    return app.resolve(request, context)
