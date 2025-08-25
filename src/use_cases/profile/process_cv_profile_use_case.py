import json
import re
from typing import List

from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter
from src.constants.index import S3_PROFILE_FILTER_CV_FILES_BUCKET_NAME
from src.constants.prompts.profile_filter import prompts
from src.domain.profile import ProfileFilterProcessDTO
from src.domain.profile import ProfileInfo, Experience, PROCESS_TYPE
from src.domain.profile_evaluation import ProfileClusteringResponse
from src.repositories.s3.filter_profile import S3StorageRepository
from src.repositories.document_db.profile_filter_process import ProfileFilterProcessRepository

from src.utils.files import create_temporal_file
from src.utils.prompt import format_prompts_placeholders


def process_cv_profile_use_case(
    process_id: str, profile_filter_process: ProfileFilterProcessDTO
) -> dict:
    temp_file_path = create_temp_file(process_id, profile_filter_process)
    messages = prepare_messages(profile_filter_process)
    profile_clustering_response = get_assistance_response(messages, temp_file_path)
    profile_infos = build_profile_info(profile_clustering_response, profile_filter_process)

    return update_profile_filter_process(process_id, profile_infos)


def create_temp_file(process_id: str, profile_filter_process: ProfileFilterProcessDTO) -> str:
    cv_file_key = profile_filter_process.process_filters.cv_file_key

    if not cv_file_key:
        raise ValueError("The cv_file_key is required in process_filters")

    s3_storage_repository = S3StorageRepository(S3_PROFILE_FILTER_CV_FILES_BUCKET_NAME)
    file_content = s3_storage_repository.get_file(cv_file_key.split(".pdf")[0], "pdf")

    temp_file_path = f"/tmp/{process_id}.pdf"
    create_temporal_file(file_content, temp_file_path)

    return temp_file_path


def prepare_messages(profile_filter_process: ProfileFilterProcessDTO) -> List[dict]:
    messages = prompts["profile_filter"]
    position = profile_filter_process.process_filters.model_dump_json(
        exclude={"business_id", "position_id", "snapshot_id"}, indent=1
    )
    placeholders = [{"position": position}]
    return format_prompts_placeholders(messages, placeholders)


def get_assistance_response(messages: List[dict], temp_file_path: str) -> ProfileClusteringResponse:
    open_ai_adapter = OpenAIAdapter()
    open_ai_adapter.assistant_id = "asst_eGYG0QGlShVAx4iYY8ph8lR7"
    messages_thread = open_ai_adapter.generate_response(messages, temp_file_path)
    response = json.loads(
        re.sub(r"^```json\n|```$", "", messages_thread.strip(), flags=re.MULTILINE)
    )

    profile_clustering_response = ProfileClusteringResponse.model_validate(response)
    if len(profile_clustering_response.evaluations) == 0:
        raise ValueError("The response does not contain evaluations")

    return profile_clustering_response


def build_profile_info(
    profile_clustering_response: ProfileClusteringResponse,
    profile_filter_process: ProfileFilterProcessDTO,
) -> List[ProfileInfo]:
    position = profile_filter_process.process_filters.role

    profile_infos = []
    for evaluation in profile_clustering_response.evaluations:
        experience = list(
            map(
                lambda exp: Experience.model_validate(exp.model_dump()),
                evaluation.candidate.experience,
            )
        )

        profile_info = ProfileInfo(
            name=evaluation.candidate.name,
            country_code=evaluation.candidate.country_code,
            city=evaluation.candidate.city,
            position=position,
            about=evaluation.candidate.about,
            linkedin_url=evaluation.candidate.url_linkedin,
            url=evaluation.candidate.url_linkedin,
            profile_evaluation=evaluation,
            experience=experience,
            email=evaluation.candidate.email,
            source=PROCESS_TYPE.PROFILES_CV_SEARCH.value,
        )
        profile_infos.append(profile_info)
    return profile_infos


def update_profile_filter_process(
    process_id: str,
    profile_infos: List[ProfileInfo],
):
    profile_filter_process_repository = ProfileFilterProcessRepository()
    profile_filter_process = profile_filter_process_repository.getById(process_id)
    if profile_filter_process is None:
        raise ValueError("Profile filter process not found")

    profile_filter_process.props.profiles = profile_infos
    profile_filter_process_repository.update(process_id, profile_filter_process)

    return profile_filter_process.to_dto(flat=True)
