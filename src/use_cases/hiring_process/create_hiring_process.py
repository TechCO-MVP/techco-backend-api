from src.domain.hiring_process import HiringProcessDTO, HiringProcessEntity
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository


def create_hiring_process_use_case(hiring_process_dto: HiringProcessDTO):
    hiring_process_entity = HiringProcessEntity(props=hiring_process_dto)
    hiring_process_repository = HiringProcessRepository()

    return hiring_process_repository.create(hiring_process_entity)
