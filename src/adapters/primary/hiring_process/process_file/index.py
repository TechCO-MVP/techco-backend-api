from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from src.use_cases.hiring_process.send_files_to_assistnat import send_file_to_assistant_use_case
from src.use_cases.hiring_process.processing_status import save_processing_status
from src.domain.hiring_process import FILE_PROCESSING_STATUS

logger = Logger()

def process_file(event: dict, context: LambdaContext) -> dict:
    """process file for send to assistant"""
    try:
        logger.info(f"Event: {event}")

        file_key = event['file_key']
        hiring_process_id = event['hiring_process_id']
        message = event['message']
        assistant_name = event['assistant_name']
        process_id = event['process_id']

        run_id, thread_id = send_file_to_assistant_use_case(
            file_key, hiring_process_id, message, assistant_name, process_id
        )

        save_processing_status(process_id, thread_id, run_id, FILE_PROCESSING_STATUS.COMPLETED.value)
        logger.info(f"file processed successfully: {run_id}")
        
        return 
    except Exception as e:
        logger.exception("Error processing file: %s", e)
        save_processing_status(process_id, None, None, FILE_PROCESSING_STATUS.FAILED.value)
        raise e


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    return process_file(event, context)