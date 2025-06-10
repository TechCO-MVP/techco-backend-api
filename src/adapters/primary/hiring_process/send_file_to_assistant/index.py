import base64
import uuid
import json
import boto3

from src.constants.index import ENV, SERVICE_NAME
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.use_cases.hiring_process.send_files_to_assistnat import save_file_to_s3
from src.use_cases.hiring_process.processing_status import save_processing_status
from src.domain.hiring_process import FILE_PROCESSING_STATUS

logger = Logger()
app = APIGatewayRestResolver()
lambda_client = boto3.client('lambda')


@app.post("/hiring_process/send_file_to_assistant")
def send_file_to_assistant():
    """send file to assistant"""
    try:
        logger.info(f"Raw event: {app.current_event.raw_event}")
        logger.info(f"Headers: {app.current_event.headers}")
        body = app.current_event.body
        is_base64_encoded = app.current_event.raw_event.get("isBase64Encoded", False)

        if is_base64_encoded:
            body = base64.b64decode(body)
        else:
            if isinstance(body, str):
                body = body.encode('utf-8')

        content_type = app.current_event.headers.get('Content-Type', '')
        headers = app.current_event.headers
        process_id = str(uuid.uuid4())
        
        save_processing_status(process_id, None, None, "IN_PROGRESS")

        file_key, hiring_process_id, message, assistant_name = save_file_to_s3(body, content_type, headers)
        
        lambda_client.invoke(
            FunctionName=f"{SERVICE_NAME}-{ENV}-process_file_for_assistant",
            InvocationType='Event',
            Payload=json.dumps({
                'file_key': file_key,
                'hiring_process_id': hiring_process_id,
                'message': message,
                'assistant_name': assistant_name,
                'process_id': process_id
            })
        )

        return Response(
            status_code=202,
            body={
                "message": "File processing started",
                "process_id": process_id,
                "status": FILE_PROCESSING_STATUS.IN_PROGRESS.value
            },
            content_type=content_types.APPLICATION_JSON,
        )

    except ValueError as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )

    except Exception as e:
        logger.exception("An error occurred: %s", e)
        return Response(
            status_code=500,
            body={"message": "An error occurred: %s" % e},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    """
    Handler function for send file to assistant
    request: The request object, described like:
    {
        "body": {
            "UpdateHiringProcessCustomFieldsDTO"
        }
    }
    """

    return app.resolve(event, context)
