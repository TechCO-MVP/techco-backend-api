""" this module is responsible for veryfy otp code for the authentication passwordless process """

import json

import boto3
from botocore.exceptions import ClientError

from src.constants.index import CLIENT_ID, REGION_NAME

cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)


def lambda_handler(event, context):
    """
    send request to cognito to verify the otp code authentication process
    """
    body = json.loads(event["body"])
    user_email = body["email"]
    otp_code = body["otp"]
    session = body["session"]
    status_code = 400
    success = False
    body = {}

    try:
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
            success = True
        else:
            body = {"message": "Invalid OTP code."}

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        body["error"] = f"Error validating OTP code: {error_message}"

    except Exception as e:
        status_code = 500
        body = {"error": f"Unexpected error: {str(e)}"}

    finally:
        return {"statusCode": status_code, "body": json.dumps(body), "success": success}
