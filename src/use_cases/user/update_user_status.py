import boto3

from src.repositories.document_db.user_repository import UserRepository
from src.domain.user import UpdateUserEntity, UserEntity

def put_user_status_use_case(user_dto: UserEntity) -> UpdateUserEntity:
    """put user status use case."""
    user_repository = UserRepository()

    user_data_db = user_repository.getByEmail(user_dto.email)
    user_data_db.status = user_dto.status
    user_id = user_dto.id
    user_repository.update(user_id, user_data_db)

    if user_dto.status == "disabled":
        user_sign_out(user_dto.email)

    return user_repository.update(user_id, user_data_db)

def user_sign_out(email: str):
    """Sign out user."""

    client = boto3.client('cognito-idp')
    user_pool_id = 'your_user_pool_id'  # Reemplaza con tu User Pool ID

    # Obtén el sub (identificador único) del usuario usando su correo electrónico
    response = client.list_users(
        UserPoolId=user_pool_id,
        Filter=f'email = "{email}"'
    )
    
    if not response['Users']:
        raise ValueError("User not found")

    user_sub = response['Users'][0]['Attributes'][0]['Value']

    # Desloguea al usuario globalmente
    client.admin_user_global_sign_out(
        UserPoolId=user_pool_id,
        Username=user_sub
    )