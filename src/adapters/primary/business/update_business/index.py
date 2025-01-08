from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.business import BusinessDTO
from src.errors.entity_not_found import EntityNotFound
from src.use_cases.business.update_business import update_business_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.put("/business/update/<business_id>")
def update_business(business_id: str):
    try:
        # validate body is not empty
        body = app.current_event.json_body
        if not body:
            raise ValueError("Request body is empty")

        # create DTO (once create pydantic validates the data)
        business_dto = BusinessDTO(**body)

        # call use case to update business
        business_entity = update_business_use_case(business_id, business_dto)

        return Response(
            status_code=200,
            body={
                "message": "Business updated successfully",
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
    """ "
    Handler function for business update
    request: The request object, described like:
    {
        "path": "/business/update/{id}",
        "httpMethod": "PUT",
        "headers": {"Authorization": "fake-access-token"},
        "body": BusinessDTO,
        "pathParameters": {"id": "123"}
    """

    return app.resolve(event, context)
