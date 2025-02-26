import time

from src.repositories.document_db.profile_filter_process import ProfileFilterProcessRepository
from src.repositories.pipefy.pipe_repository import PipeRepository
from src.repositories.pipefy.card_repository import CardRepository
from src.repositories.pipefy.mapping.index import map_profile_bright_data_fields
from src.services.graphql.graphql_service import get_client
from src.constants.index import DEFAULT_PIPE_TEMPLATE_ID


def create_pipe_configuration_open_position(profile_filter_process_id: str):
    profile_filter_process_repository = ProfileFilterProcessRepository()
    profile_filter_process = profile_filter_process_repository.getById(profile_filter_process_id)

    if not profile_filter_process:
        raise Exception("Profile filter process not found")

    profiles = profile_filter_process.props.profiles

    # create pipe
    graphql_client = get_client()
    pipe_repository = PipeRepository(graphql_client)
    pipe_template_id = DEFAULT_PIPE_TEMPLATE_ID
    pipes = pipe_repository.clone_pipe(pipe_template_id)
    pipe_id = pipes["clonePipes"]["pipes"][0]["id"]

    # TODO: update position with pipe_id
    time.sleep(10)

    # create cards
    updated_profiles = []
    card_repository = CardRepository(graphql_client)
    for index, profile in enumerate(profiles):
        fields_attributes = map_profile_bright_data_fields(profile, DEFAULT_PIPE_TEMPLATE_ID)
        response = card_repository.create_card(pipe_id, profile.name, fields_attributes)
        profile.card_id = response["createCard"]["card"]["id"]

        updated_profiles.append(profile)

    profile_filter_process.props.profiles = updated_profiles
    profile_filter_process_repository.update(profile_filter_process_id, profile_filter_process)
