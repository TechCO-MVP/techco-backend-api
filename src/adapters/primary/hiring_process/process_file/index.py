from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from src.use_cases.hiring_process.send_files_to_assistnat import (
    fetch_profiles_data,
    create_temp_file,
    prepare_messages,
    set_open_ai_adapter
)
from src.use_cases.hiring_process.processing_status import save_processing_status
from src.domain.hiring_process import FILE_PROCESSING_STATUS

logger = Logger()

def process_file(event: dict, context: LambdaContext) -> dict:
    """
    Procesa el archivo de forma asíncrona
    """
    try:
        logger.info("Iniciando procesamiento de archivo")
        logger.info(f"Event: {event}")

        file_key = event['file_key']
        hiring_process_id = event['hiring_process_id']
        message = event['message']
        assistant_name = event['assistant_name']
        process_id = event['process_id']

        file_data = fetch_profiles_data(file_key)
        temp_file_path = create_temp_file(file_key.split("/")[-1], file_data)
        messages = prepare_messages(message)
        open_ai_adapter = set_open_ai_adapter(hiring_process_id, assistant_name)
        run = open_ai_adapter.generate_response(messages, temp_file_path, return_run=True)
        run_id = run.id
        thread_id = run.thread_id

        save_processing_status(process_id, thread_id, run_id, FILE_PROCESSING_STATUS.COMPLETED.value)
        logger.info(f"Archivo procesado con éxito: {run_id}")
        
        return 
    except Exception as e:
        logger.exception("Error procesando archivo: %s", e)
        save_processing_status(process_id, None, None, FILE_PROCESSING_STATUS.FAILED.value)
        raise e


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    return process_file(event, context)