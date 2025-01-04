from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.errors.entity_not_found import EntityNotFound
from src.use_cases.business.list_businesses import list_businesses_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.get("/business/list")
def list_businesses():
    try:
        # get user id from authorizer
        user = app.current_event.request_context.authorizer["claims"]
        user_id = user["sub"]

        # call use case to get business by id
        businesses = list_businesses_use_case(user_id)

        return Response(
            status_code=200,
            body={
                "message": "Business retrieved successfully",
                "body": [business.to_dto() for business in businesses],
            },
            content_type=content_types.APPLICATION_JSON,
        )

    except ValidationError as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )

    except ValueError as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )

    except EntityNotFound as e:
        logger.error(str(e))
        return Response(
            status_code=404, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )

    except Exception:
        logger.exception("An error occurred")
        return Response(
            status_code=500,
            body={"message": "An error occurred"},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    """
    Lambda handler to list businesses by user
    """
    return app.resolve(event, context)
