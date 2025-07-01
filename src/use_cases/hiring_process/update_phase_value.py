from aws_lambda_powertools import Logger

from src.domain.hiring_process import HiringProcessPhase, HiringProcessPhaseField
from src.errors.entity_not_found import EntityNotFound
from src.models.pipefy.webhook import CardFieldUpdateEvent
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository

logger = Logger("UpdatePhaseValue")


def update_phase_value(field_update_dto: CardFieldUpdateEvent):
    logger.info(f"Updating phase value for card {field_update_dto.card.id}")
    logger.info(f"Field: {field_update_dto.field.id}")
    logger.info(f"New value: {field_update_dto.new_value}")

    hiring_process_repository = HiringProcessRepository()
    hiring_process = hiring_process_repository.getByCardId(str(field_update_dto.card.id))

    if not hiring_process:
        logger.error(f"Hiring process not found for card {field_update_dto.card.id}")
        raise EntityNotFound("HiringProcess", field_update_dto.card.id)

    phase_id = hiring_process.props.phase_id

    if not hiring_process.props.phases:
        hiring_process.props.phases = {}

    if phase_id not in hiring_process.props.phases:
        fields = {
            field_update_dto.field.id: HiringProcessPhaseField(
                field_id=field_update_dto.field.id,
                value=field_update_dto.new_value,
                label=field_update_dto.field.label,
            )
        }

        hiring_process.props.phases[phase_id] = HiringProcessPhase(
            phase_id=phase_id,
            fields=fields,
        )
    else:
        fields = hiring_process.props.phases[phase_id].fields
        fields[field_update_dto.field.id] = HiringProcessPhaseField(
            field_id=field_update_dto.field.id,
            value=field_update_dto.new_value,
            label=field_update_dto.field.label,
        )

    hiring_process_repository.update(hiring_process.id, hiring_process)

    logger.info(f"Phase value updated for card {field_update_dto.card.id}")
