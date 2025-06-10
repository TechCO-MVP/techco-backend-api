import cgi
import io
import boto3

from datetime import datetime
from aws_lambda_powertools import Logger

from src.constants.index import ENV, REGION_NAME, S3_ASSESSMENTS_FILES_BUCKET_NAME
from src.repositories.s3.filter_profile import S3StorageRepository
from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter
from src.use_cases.hiring_process.get_hiring_process import get_hiring_process_use_case
from src.use_cases.business.get_business_only_with_id import get_business_only_with_id_use_case
from src.domain.business import BusinessEntity
from src.domain.hiring_process import HiringProcessEntity, FILE_PROCESSING_STATUS
from src.utils.files import create_temporal_file
from src.use_cases.hiring_process.processing_status import save_processing_status


logger = Logger()

def send_file_to_assistant_use_case(body: dict, content_type: str, headers: dict, process_id: str) -> str:
    """put hiring process custom fileds by id use case."""
    try:
        file_key, hiring_process_id, message, assistant_name = save_file_to_s3(body, content_type, headers)
        file_data = fetch_profiles_data(file_key)
        temp_file_path = create_temp_file(file_key.split("/")[-1], file_data)
        messages = prepare_messages(message)
        open_ai_adapter = set_open_ai_adapter(hiring_process_id, assistant_name)
        thread_id = open_ai_adapter.generate_response(messages, temp_file_path, return_run_id=True)
        save_processing_status(process_id, thread_id, FILE_PROCESSING_STATUS.COMPLETED.value)

        return thread_id
    except Exception as e:
        logger.exception("An error occurred: %s", e)
        save_processing_status(process_id, thread_id, FILE_PROCESSING_STATUS.FAILED)
        raise ValueError(f"An error occurred: {str(e)}")


def save_file_to_s3(body: dict, content_type: str, headers: dict) -> tuple:
    """save file to s3"""
    if 'boundary=' not in content_type:
        raise ValueError("No boundary found in Content-Type")
        
    body_io = io.BytesIO(body)
    environ = {
        'REQUEST_METHOD': 'POST',
        'CONTENT_TYPE': content_type,
        'CONTENT_LENGTH': str(len(body))
    }
    
    form = cgi.FieldStorage(
        fp=body_io,
        environ=environ,
        headers=headers,
        keep_blank_values=True
    )
    
    file_content = None
    file_type = 'pdf'
    hiring_process_id = None
    message = None
    assistant_name = None
    
    for key in form.keys():
        if key == 'hiring_process_id':
            hiring_process_id = form[key].value
        if key == 'assistant_name':
            assistant_name = form[key].value
        if key == 'message':
            message = form[key].value
        elif key == 'file':
            file_item = form[key]
            
            if file_item.file:
                file_content:str = file_item.file.read()
                file_type = file_item.type or 'application/pdf'

                if file_content.startswith(b'%PDF'):
                    logger.info("Content is a valid PDF file")
                else:
                    logger.warning("Content does not start with %PDF")
                    raise ValueError("Content does not start with %PDF")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_key = f"{hiring_process_id}/{timestamp}.{file_type.split('/')[-1]}"
    s3_client = boto3.client('s3')
    bucket_name = f"{ENV}-techco-assessments-files-{REGION_NAME}"
    
    try:
        logger.info("Uploading file to S3. Content length: %d", len(file_content))
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=file_content,
            ContentType=file_type
        )
        logger.info("File uploaded successfully to S3")
    except Exception as e:
        logger.error("Error uploading to S3: %s", str(e))
        raise ValueError(f"Error uploading to S3: {str(e)}")

    return file_key, hiring_process_id, message, assistant_name


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
