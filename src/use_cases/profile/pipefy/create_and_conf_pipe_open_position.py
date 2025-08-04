import time
from aws_lambda_powertools import Logger

from src.constants.index import API_URL

from src.domain.position_configuration import PHASE_TYPE
from src.domain.position import POSITION_STATUS, Assessments


from src.repositories.document_db.profile_filter_process import ProfileFilterProcessRepository
from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.pipefy.pipe_repository import PipeRepository
from src.repositories.pipefy.webhook_repository import WebhookRepository
from src.repositories.document_db.position_configuration_repository import (
    PositionConfigurationRepository,
)


from src.errors.entity_not_found import EntityNotFound
from src.services.graphql.graphql_service import get_client


logger = Logger()


def create_and_config_pipe_open_position(
    profile_filter_process_id: str, position_id: str, business_id: str
) -> dict:
    """
    Create a pipe configuration for an open position and set up webhooks.
    """
    logger.info("Creating pipe configuration for open position")
    profile_filter_process_repository = ProfileFilterProcessRepository()
    profile_filter_process = profile_filter_process_repository.getById(profile_filter_process_id)
    if profile_filter_process is None:
        raise EntityNotFound("Profile filter process not found")

    position_repository = PositionRepository()
    position = position_repository.getById(position_id)
    if position is None:
        raise EntityNotFound("Position not found")

    graphql_client = get_client()
    pipe_repository = PipeRepository(graphql_client)
    pipe_template_id = str(position.props.position_flow.pipe_id)
    pipes = pipe_repository.clone_pipe(pipe_template_id)
    pipe_id = pipes["clonePipes"]["pipes"][0]["id"]

    max_retries = 5
    delay = 3  # initial delay in seconds

    for attempt in range(max_retries):
        try:
            pipe = pipe_repository.get_pipe_by_id(pipe_id)
            if pipe is not None and "pipe" in pipe and "id" in pipe["pipe"]:
                break

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise e  # Raise the exception if max retries reached

    time.sleep(20)  # wait for the pipe to be created

    # create webhook
    webhook_repository = WebhookRepository(graphql_client)
    webhook_name = "Webhook"
    actions = ["card.field_update", "card.move"]
    webhook_repository.create_webhook(pipe_id, f"{API_URL}/pipefy/webhook", webhook_name, actions)

    # update profile
    profile_filter_process.props.pipe_id = pipe_id
    profile_filter_process_repository.update(profile_filter_process.id, profile_filter_process)

    # update position
    position.props.pipe_id = pipe_id
    position.props.status = POSITION_STATUS.ACTIVE

    position_configuration_repository = PositionConfigurationRepository()
    position_configuration = position_configuration_repository.getById(
        position.props.position_configuration_id
    )

    for phase in position_configuration.props.phases:
        if phase.type in [PHASE_TYPE.TECHNICAL_TEST, PHASE_TYPE.SOFT_SKILLS]:
            position.props.assessments.append(Assessments(data=phase.data, type=phase.type))

    position_repository.update(position_id, position)

    return profile_filter_process.to_dto(flat=True)
