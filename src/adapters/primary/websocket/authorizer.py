"""Function to authorize connections to websockets API"""

import boto3
from botocore.exceptions import ClientError
from src.constants.index import REGION_NAME
from src.use_cases.user.get_user_by_mail import get_user_by_mail_use_case

cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)


def lambda_handler(event, context):
    """Authorize connections to websockets API."""
    method_arn = event["methodArn"]
    token = event["queryStringParameters"]["token"]
    try:
        cognito_user = cognito_client.get_user(AccessToken=token)
        email = [
            attr["Value"] for attr in cognito_user["UserAttributes"] if attr["Name"] == "email"
        ][0]
        user = get_user_by_mail_use_case(email)

        response = generate_policy("Allow", method_arn)
        response["context"] = {"client_id": user.id, "email": user.props.email}
        context.logger.info("Permission Allowed.")
        return response
    except ClientError as e:
        context.logger.error(e)
        if e.response["Error"]["Code"] == "NotAuthorizedException":
            context.logger.info("Permission Denied.")
            return generate_policy("Deny", method_arn)


def generate_policy(effect, resource):
    """Generate policy to allow or deny access to resource."""
    return {
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource,
                }
            ],
        },
    }
