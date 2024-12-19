""" this module is responsible for finish session for user """

import json

import boto3

from src.constants.index import REGION_NAME

cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)


def lambda_handler(event, context):
    """ send request to cognito to signout the user """
    body = json.loads(event["body"])
    access_token = body["access_token"]
    status_code = 401
    body = {}
    success = False
    
    try:
        cognito_client.global_sign_out(
            AccessToken=access_token
        )
        status_code = 200
        body["message"] = "User successfully signed out."
        success = True

    except cognito_client.exceptions.NotAuthorizedException:
        status_code = 401
        body["message"] = "Unauthorized: Invalid or expired token."

    finally:
        return {"statusCode": status_code, "body": json.dumps(body), "success": success}
