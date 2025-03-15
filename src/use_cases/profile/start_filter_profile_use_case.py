import json
import os

import boto3

from src.domain.profile import (
    PROCESS_STATUS,
    PROCESS_TYPE,
    ProfileFilterProcessDTO,
    ProfileFilterProcessEntity,
    ProfileFilterProcessQueryDTO,
)

from src.repositories.document_db.client import DocumentDBClient
from src.repositories.document_db.profile_filter_process import ProfileFilterProcessRepository
from src.use_cases.user.get_user_by_mail import get_user_by_mail_use_case


def start_filter_profile_use_case(
    profile_filter_process_query_dto: ProfileFilterProcessQueryDTO,
    user_email: str,
    process_type: str = PROCESS_TYPE.PROFILES_SEARCH,
) -> dict:
    """Start filter profile use case."""

    document_db_client = DocumentDBClient()
    client = document_db_client.get_client()

    with client.start_session() as session:
        document_db_client.set_session(session)
        session.start_transaction()

        try:
            user = get_user_by_mail_use_case(user_email)

            profile_filter_process_entity = create_profile_filter_process_entity(
                profile_filter_process_query_dto,
                user.id,
                process_type,
            )

            profile_filter_process_entity = save_profile_filter_process_entity(
                profile_filter_process_entity
            )

            execution_arn = start_step_function_execution(profile_filter_process_entity)

            profile_filter_process_entity.props.execution_arn = execution_arn

            profile_filter_process_entity = update_profile_filter_process_entity(
                profile_filter_process_entity
            )

            session.commit_transaction()
            document_db_client.close_session()

            return {
                "profile_filter": profile_filter_process_entity.to_dto(flat=True),
                "execution_arn": execution_arn,
            }
        except Exception as e:
            document_db_client.abort_transaction()
            raise e


def create_profile_filter_process_entity(
    profile_filter_process_query_dto: ProfileFilterProcessQueryDTO, user_id: str, process_type: str
) -> ProfileFilterProcessEntity:
    profile_filter_process_dto = ProfileFilterProcessDTO(
        status=PROCESS_STATUS.IN_PROGRESS,
        type=process_type,
        user_id=user_id,
        position_id=profile_filter_process_query_dto.position_id,
        business_id=profile_filter_process_query_dto.business_id,
        process_filters=profile_filter_process_query_dto,
    )

    return ProfileFilterProcessEntity(props=profile_filter_process_dto)


def save_profile_filter_process_entity(
    profile_filter_process_entity: ProfileFilterProcessEntity,
) -> ProfileFilterProcessEntity:
    profile_filter_process_repository = ProfileFilterProcessRepository()
    return profile_filter_process_repository.create(profile_filter_process_entity)


def update_profile_filter_process_entity(
    profile_filter_process_entity: ProfileFilterProcessEntity,
) -> ProfileFilterProcessEntity:
    profile_filter_process_repository = ProfileFilterProcessRepository()
    return profile_filter_process_repository.update(
        profile_filter_process_entity.id, profile_filter_process_entity
    )


def start_step_function_execution(
    profile_filter_process_entity: ProfileFilterProcessEntity,
) -> str:
    step_functions = boto3.client("stepfunctions")
    state_machine_arn = os.environ.get("PROFILE_FILTER_PROCESS_ARN")

    response = step_functions.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps(profile_filter_process_entity.to_dto(flat=True)),
    )

    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception("Error starting state machine")

    return response["executionArn"]
