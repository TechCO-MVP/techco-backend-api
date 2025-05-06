from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.profile import ProfileFilterProcessQueryDTO
from src.use_cases.position_configuration.crete_position import create_position_use_case
from src.use_cases.profile.start_filter_profile_use_case import start_filter_profile_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/position_configuration/create/position")
def create_position():
    try:
        body = app.current_event.json_body
        logger.info(f"Received body: {body}")

        # Validate the body
        if not body.get("position_configuration_id"):
            raise ValueError("position_configuration_id is required")

        authorizer = app.current_event.request_context.authorizer["claims"]
        user_email = authorizer["email"]

        response = create_position_use_case(body["position_configuration_id"], user_email)
        logger.info(f"Response from use case: {response}")

        profile_filter_process = ProfileFilterProcessQueryDTO(
            role=response.props.role,
            seniority=response.props.seniority,
            country_code=response.props.country_code,
            city=response.props.city,
            description=response.props.description,
            responsabilities=response.props.responsabilities,
            skills=response.props.skills,
            business_id=response.props.business_id,
            position_id=response.id,
        )

        start_filter_profile_use_case(profile_filter_process, user_email)

        return Response(
            status_code=200,
            body={
                "message": "Position created successfully",
                "body": {
                    "data": response.to_dto(flat=True),
                },
            },
            content_type=content_types.APPLICATION_JSON,
        )
    except ValidationError as e:
        logger.error(str(e))
        return Response(
            status_code=422, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )
    except ValueError as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )
    except Exception as e:
        logger.error(f"Error in create_position handler: {str(e)}")
        return Response(
            status_code=500,
            body={"message": "Internal server error"},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def handler(event, context: LambdaContext):
    """
    Handler function to change to the next phase and update the current_phase.
    request: {
        "position_configuration_id": "string",
        "phase_type": "string",
    }
    """
    return app.resolve(event, context)
