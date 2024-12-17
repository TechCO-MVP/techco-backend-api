import boto3

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.constants.index import CLIENT_ID

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/auth/signup")
def sign_up():
    try:
        body = app.current_event.json_body
        password = create_random_password()  # password not required so we can generate a random one

        cognito_client = boto3.client("cognito-idp")
        result = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=body.get("email"),
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": body.get("email")},
                {"Name": "name", "Value": body.get("name")},
            ],
        )

        if result.get("ResponseMetadata").get("HTTPStatusCode") != 200:
            return {
                "statusCode": 400,
                "body": {"message": "User sign up failed"},
            }

        return {
            "statusCode": 200,
            "body": {
                "message": "User signed up successfully",
                "data": result,
            },
        }
    except cognito_client.exceptions.UsernameExistsException:
        return {
            "statusCode": 400,
            "body": {"message": "User already exists"},
        }
    except Exception:
        logger.exception("An error occurred")
        return {
            "statusCode": 500,
            "body": {"message": "An error occurred"},
        }


@logger.inject_lambda_context
def handler(request: dict, context: LambdaContext) -> dict:
    """
    Handler function
    request: The request object, described like:
    {
        "body": {
            "email": "email"
        }
    }
    """
    return app.resolve(request, context)


def create_random_password():
    import random
    import string

    password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    return password