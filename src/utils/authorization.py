import boto3

from functools import wraps
from typing import List
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response
from botocore.exceptions import ClientError


from src.constants.index import REGION_NAME, CLIENT_ID
from src.repositories.document_db.user_repository import UserRepository
from src.domain.user import UserEntity


logger = Logger()


def role_required(
    app: APIGatewayRestResolver, required_roles: List[str], business_id_location: str = "path"
):
    """Decorator to check if user has required role."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                authorizer = app.current_event.request_context.authorizer

                if not authorizer or "claims" not in authorizer:
                    return _unauthorized_response("Unauthorized")

                user = authorizer["claims"]

                if not user or "email" not in user:
                    return _unauthorized_response("Unauthorized")

                user_repository = UserRepository()
                user_entity = user_repository.getByEmail(user["email"])

                business_id = _get_business_id(app, business_id_location)
                if not business_id:
                    return _unauthorized_response(
                        "Unauthorized: No business_id in path or query string"
                    )

                role = _get_user_role(user_entity, business_id)
                if role is None or role not in required_roles:
                    return _unauthorized_response("Unauthorized")

                return func(*args, **kwargs)
            except Exception as e:
                logger.exception("An error occurred", exc_info=e)
                return _unauthorized_response("Unauthorized")

        return wrapper

    return decorator


def _unauthorized_response(message: str) -> Response:
    return Response(status_code=403, body={"message": message})


def _get_business_id(app: APIGatewayRestResolver, business_id_location: str) -> str:
    if business_id_location == "path":
        return (
            app.current_event.path_parameters.get("business_id", None)
            if app.current_event.path_parameters
            else None
        )

    query_string_parameters = app.current_event.query_string_parameters
    return query_string_parameters.get("business_id", None) if query_string_parameters else None


def _get_user_role(user_entity: UserEntity, business_id: str):
    roles = user_entity.props.roles
    return next((r.role for r in roles if r.business_id == business_id), None)


def create_random_password():
    import random
    import string

    password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    return password


def sign_up_user_cognito(email: str):
    """Sign up user cognito."""
    try:
        cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)

        cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=create_random_password(),
            UserAttributes=[{"Name": "email", "Value": email}],
        )
    except Exception as e:
        logger.exception("An error occurred", exc_info=e)
        raise ClientError("Could not sign up user", e)
