import uuid
from typing import Dict

import boto3

from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter
from src.constants.index import CLIENT_ID, ENV, REGION_NAME
from src.domain.assistant import ASSISTANT_TYPE
from src.domain.business import BusinessDTO, BusinessEntity
from src.domain.user import UserDTO, UserEntity
from src.repositories.document_db.business_repository import BusinessRepository
from src.repositories.document_db.client import DocumentDBClient
from src.repositories.document_db.user_repository import UserRepository


def validate_business_dto(business_dto: BusinessDTO):
    if not business_dto.is_admin:
        raise ValueError("Businesses must be created as admin")
    if business_dto.parent_business_id:
        raise ValueError("Businesses must not have a parent business")


def create_business_and_user(business_dto: BusinessDTO, user_dto: UserDTO):
    assistants = create_assistants_for_business()
    business_dto.assistants = assistants

    business_repository = BusinessRepository()
    business_entity = BusinessEntity(props=business_dto)
    business_entity = business_repository.create(business_entity)

    user_repository = UserRepository()
    user_dto.business_id = str(business_entity.id)
    user_dto.roles[0].business_id = str(business_entity.id)
    user_entity = UserEntity(props=user_dto)

    user_entity = user_repository.create(user_entity)

    return business_entity, user_entity


def authenticate_user_with_cognito(user_dto: UserDTO, otp: str, cognito_session: str):
    if ENV == "local":
        return {"IdToken": "mock_id", "AccessToken": "mock_access", "RefreshToken": "mock_refresh"}

    cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)
    response = cognito_client.respond_to_auth_challenge(
        ClientId=CLIENT_ID,
        ChallengeName="CUSTOM_CHALLENGE",
        ChallengeResponses={"USERNAME": user_dto.email, "ANSWER": otp},
        Session=cognito_session,
    )

    if "AuthenticationResult" not in response:
        raise ValueError("Invalid OTP code")

    return response["AuthenticationResult"]


def crete_admin_business_use_case(
    business_dto: BusinessDTO, user_dto: UserDTO, otp: str, cognito_session: str
):
    document_db_client = DocumentDBClient()
    client = document_db_client.get_client()

    with client.start_session() as session:
        document_db_client.set_session(session)
        session.start_transaction()

        try:
            validate_business_dto(business_dto)
            business_entity, user_entity = create_business_and_user(business_dto, user_dto)
            auth_result = authenticate_user_with_cognito(user_dto, otp, cognito_session)

            result = {
                "idToken": auth_result["IdToken"],
                "accessToken": auth_result["AccessToken"],
                "refreshToken": auth_result["RefreshToken"],
                "user": user_entity,
                "business": business_entity.to_dto(),
            }
            session.commit_transaction()
            document_db_client.close_session()
            return result

        except Exception as e:
            document_db_client.abort_transaction()
            raise e


def create_assistants_for_business() -> Dict[str, Dict]:
    unique_identifier = str(uuid.uuid4())

    open_ai_adapter = OpenAIAdapter()
    assistant = open_ai_adapter.create_assistant(
        unique_identifier, ASSISTANT_TYPE.POSITION_ASSISTANT
    )

    return {
        ASSISTANT_TYPE.POSITION_ASSISTANT: {
            "assistant_id": assistant.id,
            "assistant_type": ASSISTANT_TYPE.POSITION_ASSISTANT,
        }
    }
