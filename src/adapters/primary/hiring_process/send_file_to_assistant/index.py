import base64
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext

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
        
        return Response(
            status_code=200,
            body={
                "message": "File uploaded successfully",
                "body":{
                    "data":{
                        "thread_id": thread_id
                    }
                }
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
