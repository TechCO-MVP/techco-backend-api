from aws_lambda_powertools import Logger

from src.constants.index import S3_ASSESSMENTS_FILES_BUCKET_NAME
from src.repositories.s3.filter_profile import S3StorageRepository
from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter
from src.use_cases.hiring_process.get_hiring_process import get_hiring_process_use_case
from src.use_cases.business.get_business_only_with_id import get_business_only_with_id_use_case
from src.domain.business import BusinessEntity
from src.domain.hiring_process import HiringProcessEntity, FILE_PROCESSING_STATUS
from src.utils.files import create_temporal_file
from src.use_cases.hiring_process.processing_status import save_processing_status


logger = Logger()

def send_file_to_assistant_use_case(
        file_key: str, hiring_process_id: str, message: str, assistant_name: str, process_id: str
    ) -> tuple[str, str]:
    """put hiring process custom fileds by id use case."""
    try:
        file_data = fetch_profiles_data(file_key)
        temp_file_path = create_temp_file(file_key.split("/")[-1], file_data)
        messages = prepare_messages(message)
        open_ai_adapter = set_open_ai_adapter(hiring_process_id, assistant_name)
        run = open_ai_adapter.generate_response(messages, temp_file_path, return_run=True)
        run_id = run.id
        thread_id = run.thread_id

        save_processing_status(process_id, thread_id, run_id, FILE_PROCESSING_STATUS.COMPLETED.value)

        return run_id, thread_id
    except Exception as e:
        logger.exception("An error occurred: %s", e)
        save_processing_status(process_id, None, None, FILE_PROCESSING_STATUS.FAILED.value)
        raise ValueError(f"An error occurred: {str(e)}")


def fetch_profiles_data(file_key: str) -> bytes:
    s3_storage_repository = S3StorageRepository(S3_ASSESSMENTS_FILES_BUCKET_NAME)
    return s3_storage_repository.get_file(file_key)


def create_temp_file(file_key: str, file_data: bytes) -> str:
    temp_file_path = f"/tmp/{file_key}"
    create_temporal_file(file_data, temp_file_path)
    return temp_file_path


def prepare_messages(message: str) -> list:
    return [
        {
            "role": "assistant",
            "content": message,
        }
    ]


def set_open_ai_adapter(hiring_process_id: str, assistant_name: str) -> OpenAIAdapter:
    hiring_entity: HiringProcessEntity = get_hiring_process_use_case({"hiring_process_id": hiring_process_id})
    business_entity: BusinessEntity = get_business_only_with_id_use_case(hiring_entity.props.business_id)
    assistant_id = business_entity.props.assistants[assistant_name].assistant_id

    context = {"business_id": business_entity.id}
    open_ai_adapter = OpenAIAdapter(context)
    open_ai_adapter.assistant_id = assistant_id

    return open_ai_adapter
