import time

from src.constants.index import API_URL, DEFAULT_PIPE_TEMPLATE_ID
from src.domain.hiring_process import HiringProcessDTO
from src.domain.profile_brightdata import ProfileBrightDataDTO
from src.domain.profile import PROCESS_STATUS
from src.errors.entity_not_found import EntityNotFound
from src.repositories.document_db.profile_filter_process import ProfileFilterProcessRepository
from src.repositories.pipefy.card_repository import CardRepository
from src.repositories.pipefy.mapping.index import map_profile_bright_data_fields
from src.repositories.pipefy.pipe_repository import PipeRepository
from src.repositories.pipefy.webhook_repository import WebhookRepository
from src.services.graphql.graphql_service import get_client
from src.use_cases.hiring_process.create_hiring_process import create_hiring_process_use_case


def create_hiring_proces_for_profile(
    position_id: str, business_id: str, phase_id: int, profile: ProfileBrightDataDTO
):
    hiring_process_dto = HiringProcessDTO(
        position_id=position_id,
        business_id=business_id,
        card_id=profile.card_id,
        phase_id=phase_id,
        profile=profile,
    )

    return create_hiring_process_use_case(hiring_process_dto)


def create_pipe_configuration_open_position(
    profile_filter_process_id: str, position_id: str, business_id: str
):
    profile_filter_process_repository = ProfileFilterProcessRepository()
    profile_filter_process = profile_filter_process_repository.getById(profile_filter_process_id)
    if profile_filter_process is None:
        raise EntityNotFound("Profile filter process not found")

    profiles = profile_filter_process.props.profiles

    # create pipe
    graphql_client = get_client()
    pipe_repository = PipeRepository(graphql_client)
    pipe_template_id = DEFAULT_PIPE_TEMPLATE_ID
    pipes = pipe_repository.clone_pipe(pipe_template_id)
    pipe_id = pipes["clonePipes"]["pipes"][0]["id"]

    # TODO: update position with pipe_id

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

    # create cards
    updated_profiles = []
    card_repository = CardRepository(graphql_client)
    for _, profile in enumerate(profiles):
        fields_attributes = map_profile_bright_data_fields(profile, DEFAULT_PIPE_TEMPLATE_ID)

        response = card_repository.create_card(pipe_id, profile.name, fields_attributes)
        card_id = response["createCard"]["card"]["id"]
        phase_id = response["createCard"]["card"]["current_phase"]["id"]

        profile.card_id = card_id
        create_hiring_proces_for_profile(position_id, business_id, phase_id, profile)

        updated_profiles.append(profile)

    # create webhook
    webhook_repository = WebhookRepository(graphql_client)

    webhook_name = "Webhook"
    actions = ["card.field_update", "card.move"]
    webhook_repository.create_webhook(pipe_id, f"{API_URL}/pipefy/webhook", webhook_name, actions)

    # update profile
    profile_filter_process.props.pipe_id = pipe_id
    profile_filter_process.props.status = PROCESS_STATUS.COMPLETED
    profile_filter_process.props.profiles = updated_profiles
    profile_filter_process_repository.update(profile_filter_process_id, profile_filter_process)
