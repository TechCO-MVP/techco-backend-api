import boto3
import os

from src.repositories.document_db.user_repository import UserRepository
from src.domain.user import UserEntity, UpdateUserStatusDTO

def put_user_status_use_case(user_dto: UpdateUserStatusDTO) -> UserEntity:
    """put user status use case."""
    user_repository = UserRepository()

    if user_dto.user_status == "disabled":
        user_sign_out(user_dto.email)

    user_data_db = user_repository.getByEmail(user_dto.user_email)
    user_data_db.props.status = user_dto.user_status
    return user_repository.update(user_dto.user_id, user_data_db)


def user_sign_out(email: str):
    """Sign out user."""

    cognito_client = boto3.client("cognito-idp", region_name=os.getenv("REGION_NAME"))
    user_pool_id = os.getenv("COGNITO_USER_POOL_ID")

    response = cognito_client.list_users(
            UserPoolId=user_pool_id,
            Filter=f'email = "{email}"',
            Limit=1
        )
    
    if not response['Users']:
        raise ValueError("User not found")

    user_sub = response['Users'][0]['Attributes'][0]['Value']

    cognito_client.admin_user_global_sign_out(
        UserPoolId=user_pool_id,
        Username=user_sub
    )
