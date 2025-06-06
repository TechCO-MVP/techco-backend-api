from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.use_cases.hiring_process.assistant_response import assistant_response_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/hiring_process/assistant/response")
def hiring_process_assistant_response():
    try:
        body = app.current_event.json_body
        logger.info(f"Received body: {body}")

        # Validate the body
        if not body.get("hiring_process_id"):
            raise ValueError("hiring_process_id is required")
        if not body.get("run_id"):
            raise ValueError("run_id is required")
        if not body.get("assistant_type"):
            raise ValueError("assistant_type is required")

        response = assistant_response_use_case(
            body["hiring_process_id"], body["run_id"], body["assistant_type"]
        )

        return Response(
            status_code=200,
            body={
                "message": "Assistant response processed successfully",
                "data": response,
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
            "hiring_process_id": "string",
            "run_id": "string",
            "assistan_type": "string"
        }
    }
    """
    return app.resolve(event, context)
