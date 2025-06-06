from datetime import datetime
from typing import Dict, Any
import base64
import urllib.parse
import cgi
import io

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from src.constants.index import ENV, REGION_NAME

from src.use_cases.hiring_process.send_files_to_assistnat import send_file_to_assistant_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/hiring_process/send_file_to_assistant")
def send_file_to_assistant():
    """send file to assistant"""
    try:
        body = app.current_event.body
        is_base64_encoded = app.current_event.raw_event.get("isBase64Encoded", False)

        if is_base64_encoded:
            body = base64.b64decode(body)
        else:
            if isinstance(body, str):
                body = body.encode('utf-8')


        content_type = app.current_event.headers.get('Content-Type', '')
        headers = app.current_event.headers
        thread_id = send_file_to_assistant_use_case(body, content_type, headers)
        
        # if 'boundary=' not in content_type:
        #     return Response(
        #         status_code=400,
        #         body={"message": "No boundary found in Content-Type"},
        #         content_type=content_types.APPLICATION_JSON,
        #     )
            
        # body_io = io.BytesIO(body)
        # environ = {
        #     'REQUEST_METHOD': 'POST',
        #     'CONTENT_TYPE': content_type,
        #     'CONTENT_LENGTH': str(len(body))
        # }
        
        # form = cgi.FieldStorage(
        #     fp=body_io,
        #     environ=environ,
        #     headers=app.current_event.headers,
        #     keep_blank_values=True
        # )
        
        # file_content = None
        # file_type = 'pdf'
        # hiring_process_id = None
        
        # for key in form.keys():
            
        #     if key == 'hiring_process_id':
        #         hiring_process_id = form[key].value
        #     elif key == 'file':
        #         file_item = form[key]
                
        #         if file_item.file:
        #             file_content = file_item.file.read()
        #             file_type = file_item.type or 'application/pdf'

        #             if file_content.startswith(b'%PDF'):
        #                 logger.info("Content is a valid PDF file")
        #             else:
        #                 logger.warning("Content does not start with %PDF")
        #                 raise ValueError("Content does not start with %PDF")

        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # file_key = f"{hiring_process_id}/{timestamp}.{file_type.split('/')[-1]}"
        # s3_client = boto3.client('s3')
        # bucket_name = f"{ENV}-techco-assessments-files-{REGION_NAME}"
        
        # try:
        #     logger.info("Uploading file to S3. Content length: %d", len(file_content))
        #     s3_client.put_object(
        #         Bucket=bucket_name,
        #         Key=file_key,
        #         Body=file_content,
        #         ContentType=file_type
        #     )
        #     logger.info("File uploaded successfully to S3")
        # except Exception as e:
        #     logger.error("Error uploading to S3: %s", str(e))
        #     return Response(
        #         status_code=500,
        #         body={"message": f"Error uploading to S3: {str(e)}"},
        #         content_type=content_types.APPLICATION_JSON,
        #     )

        # # Generar la URL del archivo
        # file_url = f"https://{bucket_name}.s3.{REGION_NAME}.amazonaws.com/{file_key}"

        return Response(
            status_code=200,
            body={
                "message": "File uploaded successfully",
                "therad_id": thread_id
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
