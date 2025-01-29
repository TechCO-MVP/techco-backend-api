import boto3

from src.constants.index import REGION_NAME, EMAIL_OTP, UI_URI
from src.domain.user import UserDTO, UserEntity, UserStatus
from src.repositories.document_db.business_repository import BusinessRepository
from src.repositories.document_db.client import DocumentDBClient
from src.repositories.document_db.user_repository import UserRepository
from src.utils.authorization import sign_up_user_cognito


def send_invitation_email(email: str):
    """Send invitation email."""
    ses_client = boto3.client("ses", region_name=REGION_NAME)
    ses_client.send_email(
        Source=EMAIL_OTP,
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": "Invitation to join to TechCo"},
            "Body": {
                "Text": {
                    "Data": (
                        "You have been invited to join TechCo, "
                        "you can login with your email to the next link: "
                        f"{UI_URI}"
                    )
                }
            },
        },
    )


def create_user_use_case(user_dto: UserDTO, business_id: str) -> dict:
    """Create user use case."""

    documebt_db_client = DocumentDBClient()
    client = documebt_db_client.get_client()

    with client.start_session() as session:
        documebt_db_client.set_session(session)
        session.start_transaction()

        try:
            business_repository = BusinessRepository()
            business_entity = business_repository.getById(business_id)

            if business_entity is None:
                raise ValueError("Business not found")

            if not business_entity.props.is_admin:
                business_id = business_entity.props.parent_business_id

            user_dto.business_id = business_id

            user_repository = UserRepository()
            user_dto.status = UserStatus.PENDING
            user_entity = UserEntity(props=user_dto)

            result = user_repository.create(user_entity)
            sign_up_user_cognito(user_dto.email, user_dto.full_name)
            send_invitation_email(user_dto.email)

            session.commit_transaction()
            documebt_db_client.close_session()

            return result
        except Exception as e:
            session.abort_transaction()
            raise e
