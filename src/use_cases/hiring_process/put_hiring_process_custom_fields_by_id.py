from aws_lambda_powertools import Logger
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.domain.base_entity import from_dto_to_entity
from src.domain.hiring_process import HiringProcessEntity, UpdateHiringProcessCustomFieldsDTO


logger = Logger()

def put_hiring_process_custom_fields_by_id_use_case(body: dict) -> tuple:
    """put hiring process custom fileds by id use case."""
    UpdateHiringProcessCustomFieldsDTO(**body)
    hiring_repository = HiringProcessRepository()
    hiring = hiring_repository.getById(body.get("id"))
    hiring_dto, changes_made = updat_hiring_data(hiring, body)
    message = "Hiring process updated successfully"

    if changes_made:
        hiring_entity = from_dto_to_entity(HiringProcessEntity, hiring_dto)
        hiring_repository.update(hiring.id, hiring_entity)
    else:
        message = "No changes made to the hiring process"
        logger.info(message)

    return hiring_dto, message


def updat_hiring_data(hiring: HiringProcessEntity, body: dict) -> tuple:
    """update hiring data - custom fields."""
    hiring_dto = hiring.to_dto(flat=True)
    current_phases = hiring_dto["phases"]
    changes_made = False
    
    for phase_id, fields in body.get("phases", {}).items():
        if phase_id not in current_phases:
            logger.info(f"Phase ID '{phase_id}' not found in current phases.")
            logger.info(f"insert new phase '{phase_id}'")
            new_phase = {
                str(phase_id): {
                    "phase_id": phase_id,
                    "fields": {},
                    "custom_fields": fields.get("custom_fields", {}),
                },
            }
            hiring_dto["phases"].update(new_phase)
            changes_made = True
            continue

        current_custom_fields = current_phases[phase_id].get("custom_fields", {})

        if current_custom_fields != fields.get("custom_fields", {}):
            logger.info(f"Custom fields for phase '{phase_id}' updated from '{current_custom_fields}' to '{fields['custom_fields']}'")
            hiring_dto["phases"][phase_id]["custom_fields"] = fields.get("custom_fields")
            changes_made = True

    return hiring_dto, changes_made
