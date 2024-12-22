""" this module is responsible for finish session for user """

import json
import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.constants.index import REGION_NAME

cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/auth/signout")
def sign_out():
    """send request to cognito to signout the user"""
    logger.info("Signing out user")
    logger.info(app.current_event)
    logger.info(app.current_event.headers)

    headers = app.current_event.headers or {}
    auth_header = headers.get("Authorization", "")
    status_code = 401
    body = {}
    success = False

    # if not auth_header.startswith("Bearer "):
    #     status_code = 401
    #     body["message"] = "Unauthorized: Missing or invalid Authorization header"
    #     return {"statusCode": status_code, "body": json.dumps(body), "success": success}

    # access_token = auth_header.split(" ")[1]

    try:
        cognito_client.global_sign_out(AccessToken=auth_header)
        status_code = 200
        body["message"] = "User successfully signed out."
        success = True

    except cognito_client.exceptions.NotAuthorizedException:
        status_code = 401
        body["message"] = "Unauthorized: Invalid or expired token."

    finally:
        return {"statusCode": status_code, "body": json.dumps(body), "success": success}


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
