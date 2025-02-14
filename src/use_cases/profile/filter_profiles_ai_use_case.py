from typing import List
from src.utils.files import create_temporal_file

from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter
from src.constants.index import S3_DEPURATED_PROFILE_DATA_IA_BUCKET_NAME
from src.domain.profile import ProfileFilterProcessDTO
from src.repositories.s3.filter_profile import S3StorageRepository

from src.domain.profile_evaluation import ProfileClusteringResponse
from src.models.openai.index import OpenAIMessage, OpenAITool


def query_profiles_ai_use_case(process_id: str, profile_filters: ProfileFilterProcessDTO) -> dict:
    """Query profiles AI use case."""
    s3_storage_repository = S3StorageRepository(S3_DEPURATED_PROFILE_DATA_IA_BUCKET_NAME)
    profiles_data: bytes = s3_storage_repository.get_file(process_id)

    temp_file_path = f"/tmp/{process_id}.json"
    create_temporal_file(profiles_data, temp_file_path)

    open_ai_adapter = OpenAIAdapter()

    messages: List[OpenAIMessage] = [{"role": "system", "content": ""}]
    profile_clustering_schema: OpenAITool = {
        "name": "profile_clustering",
        "description": (
            "Clasifica a los candidatos en cuatro grupos de coincidencia "
            "según su ajuste al cargo."
        ),
        "parameters": ProfileClusteringResponse.model_json_schema(),
    }
    tools = [profile_clustering_schema]
    tool_choice = "profile_clustering"

    open_ai_adapter.generate_response(messages, tools, tool_choice, temp_file_path)

    return {"profiles": []}
