from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.position import UpdatePositionDTO
from src.use_cases.position.update_position import update_position_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.put("/position/update")
def update_position():
    """Update position."""
    try:
        body = app.current_event.json_body
        logger.info(f"Received body: {body}")

        # Validate the body
        if not body.get("_id"):
            raise ValueError("_id is required")

        update_position_dto = UpdatePositionDTO(**body)

        response = update_position_use_case(update_position_dto)
        return Response(
            status_code=200,
            body={
                "message": "Position updated successfully",
                "body": {
                    "data": response,
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
        logger.exception("An error occurred: %s", e)
        return Response(
            status_code=500,
            body={"message": "An error occurred: %s" % e},
            content_type=content_types.APPLICATION_JSON,
        )


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """
    Handler function for put position status
    request: The request object, described like:
    {
        "body": {
          "_id": "position_id",
          "deleted_at": null,
          "position_configuration_id": "68962331a0c7a40ca8cc0ba3",
          "business_id": "6890a1b67c95128ec5ea4ad7",
          "owner_position_user_id": "68910d10e7396527ac7de6c5",
          "recruiter_user_id": "68910d10e7396527ac7de6c5",
          "responsible_users": [],
          "flow_type": "HIGH_PROFILE_FLOW",
          "role": "Gerente de ventas",
          "seniority": "Debe tener como mínimo 5 años en el sector de consumo masivo",
          "country_code": "PE",
          "city": "Lima",
          "description": "",
          "responsabilities": [
            "Desarrollar y ejecutar la estrategia comercial de ventas",
            "Liderar y motivar al equipo de ventas",
          ],
          "education": [
          "Especialización en Ventas",
          "Maestría en Dirección de Ventas y/o Comercial (Deseable)"
          ],
          "skills": [
          {
              "name": "Microsoft Excel Nivel Avanzado (Indispensable)",
              "required": false
          },
          {
              "name": "Microsoft Office Nivel Intermedio (Indispensable)",
              "required": false
          }
          ],
          "languages": [
          {
              "name": "Inglés",
              "level": "Básico"
          }
          ],
          "hiring_priority": "high",
          "work_mode": "ON_SITE",
          "status": "ACTIVE",
          "benefits": [
          "Posibilidad de realizar línea de carrera"
          ],
          "salary": null,
          "pipe_id": "306590552",
          "assistants": {},
        }
    }
    """
    return app.resolve(event, context)
