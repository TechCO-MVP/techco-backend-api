from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.errors.entity_not_found import EntityNotFound
from src.use_cases.business.get_business_by_id import get_business_by_id_use_case


logger = Logger()
app = APIGatewayRestResolver()


@app.get("/business/{id}")
def get_business_by_id():
    try:
        # get business id from path parameters
        business_id = app.current_event.path_parameters["id"]

        # call use case to get business by id
        business_entity = get_business_by_id_use_case(business_id)

        return Response(
            status_code=200,
            body={
                "message": "Business retrieved successfully",
                "body": business_entity.to_dto(),
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
    Lambda handler to get business by id, if the user that is calling bellongs to the same business
    """
    return app.resolve(event, context)
