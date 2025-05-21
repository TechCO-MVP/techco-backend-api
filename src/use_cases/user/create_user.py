import boto3

from src.constants.index import REGION_NAME, EMAIL_OTP, UI_URI
from src.constants.auth.index import EMAIL_NEW_USER_TEMPLATE, LOGO_HEADER_URL, LOGO_BODY_URL
from src.domain.user import UserDTO, UserEntity, UserStatus
from src.repositories.document_db.business_repository import BusinessRepository
from src.repositories.document_db.client import DocumentDBClient
from src.repositories.document_db.user_repository import UserRepository
from src.utils.authorization import sign_up_user_cognito


def send_invitation_email(email: str, user_name: str, business_name: str, company_logo: str):
    """Send invitation email."""
    ses_client = boto3.client("ses", region_name=REGION_NAME)

    html_company_image = """<img src="[URL_DEL_LOGO_BODY]" alt="Talent Connect Logo">"""

    if company_logo:
        html_company_image = html_company_image.replace("[URL_DEL_LOGO_BODY]", company_logo)
    else:
        html_company_image = ""

    html_content = EMAIL_NEW_USER_TEMPLATE
    html_content = html_content.replace("{{name}}", user_name)
    html_content = html_content.replace("{{nombre de la empresa}}", business_name)
    html_content = html_content.replace("{{UI_URI}}", UI_URI)
    html_content = html_content.replace("[URL_DEL_LOGO_HEADER]", LOGO_HEADER_URL)
    email_template = html_content.replace('<img src="[URL_DEL_LOGO_BODY]" alt="Talent Connect Logo">', html_company_image)

    ses_client.send_email(
        Source=EMAIL_OTP,
        Destination={"ToAddresses": [email]},
        Message={
            "Subject": {"Data": "Invitation to join to TechCo"},
            "Body": {
                "Html": {"Data": email_template}
            },
        },
    )


def create_user_use_case(user_dto: UserDTO, business_id: str) -> dict:
    """Create user use case."""

    document_db_client = DocumentDBClient()
    client = document_db_client.get_client()

    with client.start_session() as session:
        document_db_client.set_session(session)
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
            send_invitation_email(user_dto.email, user_dto.full_name, business_entity.props.name, business_entity.props.logo)

            session.commit_transaction()
            document_db_client.close_session()

            return result
        except Exception as e:
            document_db_client.abort_transaction()
            raise e
