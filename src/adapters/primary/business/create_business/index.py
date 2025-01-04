from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.business import BusinessDTO
from src.use_cases.business.create_business import create_business_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/business/create")
def create_business():
    try:

        # validate body is not empty
        body = app.current_event.json_body
        if not body:
            raise ValueError("Request body is empty")

        # create DTO (once create pydantic validates the data)
        business_dto = BusinessDTO(**body)

        # call use case to create business
        business_entity = create_business_use_case(business_dto)

        return Response(
            status_code=200,
            body={
                "message": "Business created successfully",
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
    Handler function for creating a business
    request: The request object, described like:
    {
        "body": {
            "name": "string",
            "segment": "string",
            "country_code": "string",
            "size": "string"
        }
    }
    """

    return app.resolve(event, context)
