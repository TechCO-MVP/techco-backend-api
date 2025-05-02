from aws_lambda_powertools import Logger
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.domain.base_entity import from_dto_to_entity
from src.domain.hiring_process import HiringProcessEntity, UpdateHiringProcessDTO


logger = Logger()

def put_hiring_process_by_id_use_case(body: dict) -> tuple:
    """put hiring process by id use case."""
    UpdateHiringProcessDTO(**body)
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
    """update hiring data."""
    hiring_dto = hiring.to_dto(flat=True)
    current_phases = hiring_dto["phases"]
    changes_made = False
    
    for key, new_value in body.items():
        if (
            hiring_dto.get(key)
            and (current_value := hiring_dto.get(key)) != new_value
            and key in UpdateHiringProcessDTO.model_fields
        ):
            hiring_dto[key] = new_value
            changes_made = True
            logger.info(f"Field '{key}' updated from '{current_value}' to '{new_value}'")
        
        if key == "phases" and changes_made:
            for phase in hiring_dto[key]:
                hiring_dto[key][phase]["custom_fileds"] = current_phases[phase].get("custom_fields", {})

    return hiring_dto, changes_made
