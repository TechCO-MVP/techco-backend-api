import json
import re
from typing import List

from src.adapters.secondary.documentdb.profile_filter_process_db_adapter import (
    ProfileFilterProcessDocumentDBAdapter,
)
from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter
from src.constants.index import (
    S3_DEPURATED_PROFILE_DATA_IA_BUCKET_NAME,
    S3_REFINED_PROFILE_DATA_IA_BUCKET_NAME,
)
from src.constants.prompts.profile_filter import prompts
from src.domain.profile import ProfileFilterProcessDTO
from src.domain.profile_brightdata import ProfileBrightDataDTO
from src.domain.profile_evaluation import PROFILE_GROUP, ProfileClusteringResponse
from src.repositories.s3.filter_profile import S3StorageRepository
from src.utils.files import create_temporal_file
from src.utils.prompt import format_prompts_placeholders


def query_profiles_ai_use_case(
    process_id: str, profile_filter_process: ProfileFilterProcessDTO
) -> dict:
    """Query profiles AI use case."""
    profiles_data = fetch_profiles_data(process_id)
    temp_file_path = create_temp_file(process_id, profiles_data)
    messages = prepare_messages(profile_filter_process)
    profile_clustering_response = get_profile_clustering_response(messages, temp_file_path)
    profiles = load_profiles(process_id)
    clusters = cluster_profiles(profile_clustering_response, profiles)
    selected_profiles = select_top_profiles(clusters, len(profiles))
    update_profile_filter_process(process_id, selected_profiles)
    save_s3_cluster_profiles(process_id, clusters)
    return get_profile_filter_process_dto(process_id)


def fetch_profiles_data(process_id: str) -> bytes:
    s3_storage_repository = S3StorageRepository(S3_DEPURATED_PROFILE_DATA_IA_BUCKET_NAME)
    return s3_storage_repository.get_file(process_id, "json")


def create_temp_file(process_id: str, profiles_data: bytes) -> str:
    temp_file_path = f"/tmp/{process_id}.json"
    create_temporal_file(profiles_data, temp_file_path)
    return temp_file_path


def prepare_messages(profile_filter_process: ProfileFilterProcessDTO) -> List[dict]:
    messages = prompts["profile_filter"]
    position = profile_filter_process.process_filters.model_dump_json(
        exclude={"business_id", "position_id", "snapshot_id"}, indent=1
    )
    placeholders = [{"position": position}]
    return format_prompts_placeholders(messages, placeholders)


def get_profile_clustering_response(
    messages: List[dict], temp_file_path: str
) -> ProfileClusteringResponse:
    open_ai_adapter = OpenAIAdapter()
    messages_thread = open_ai_adapter.generate_response(messages, temp_file_path)
    response = json.loads(
        re.sub(r"^```json\n|```$", "", messages_thread.strip(), flags=re.MULTILINE)
    )
    profile_clustering_response = ProfileClusteringResponse(**response)
    if len(profile_clustering_response.evaluations) == 0:
        raise Exception("No profiles found")
    return profile_clustering_response


def load_profiles(process_id: str) -> dict[str, ProfileBrightDataDTO]:
    s3_storage_repository = S3StorageRepository(S3_DEPURATED_PROFILE_DATA_IA_BUCKET_NAME)
    profiles = s3_storage_repository.get(process_id, "json")
    return {profile["linkedin_num_id"]: ProfileBrightDataDTO(**profile) for profile in profiles}


def cluster_profiles(
    profile_clustering_response: ProfileClusteringResponse,
    profiles: dict[str, ProfileBrightDataDTO],
) -> dict[str, List[ProfileBrightDataDTO]]:
    clusters = {
        PROFILE_GROUP.HIGH.value: [],
        PROFILE_GROUP.MID_HIGH.value: [],
        PROFILE_GROUP.MID.value: [],
        PROFILE_GROUP.LOW.value: [],
    }
    for evaluation in profile_clustering_response.evaluations:
        cluster = clusters[evaluation.group]
        profile = profiles[evaluation.id]
        profile.profile_evaluation = evaluation
        cluster.append(profile)
    return clusters


def save_s3_cluster_profiles(
    process_id: str, clusters: dict[str, List[ProfileBrightDataDTO]]
) -> None:
    s3_storage_repository = S3StorageRepository(S3_REFINED_PROFILE_DATA_IA_BUCKET_NAME)

    _clusters = {}
    for key, profiles in clusters.items():
        _profiles = [profile.model_dump() for profile in profiles]
        _clusters[key] = _profiles

    s3_storage_repository.put(process_id, _clusters)


def select_top_profiles(clusters: dict, total_profiles: int) -> List[ProfileBrightDataDTO]:
    for cluster in clusters.values():
        cluster.sort(key=lambda x: x.profile_evaluation.score, reverse=True)
    selected_profiles = []
    number_of_candidates = min(30, total_profiles)
    for key in [
        PROFILE_GROUP.HIGH.value,
        PROFILE_GROUP.MID_HIGH.value,
        PROFILE_GROUP.MID.value,
        PROFILE_GROUP.LOW.value,
    ]:
        if number_of_candidates <= 0:
            break
        candidates_by_group = min(len(clusters[key]), number_of_candidates)
        selected_profiles.extend(clusters[key][:candidates_by_group])
        number_of_candidates -= candidates_by_group
    return selected_profiles


def update_profile_filter_process(
    process_id: str, selected_profiles: List[ProfileBrightDataDTO]
) -> None:
    profile_filter_process_adapter = ProfileFilterProcessDocumentDBAdapter()
    profile_filter_process_entity = profile_filter_process_adapter.getById(process_id)
    profile_filter_process_entity.props.profiles = selected_profiles
    profile_filter_process_adapter.update(process_id, profile_filter_process_entity)


def get_profile_filter_process_dto(process_id: str) -> dict:
    profile_filter_process_adapter = ProfileFilterProcessDocumentDBAdapter()
    profile_filter_process_entity = profile_filter_process_adapter.getById(process_id)
    return profile_filter_process_entity.to_dto(flat=True)
