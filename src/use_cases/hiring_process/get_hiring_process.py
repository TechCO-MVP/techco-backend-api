from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.domain.hiring_process import HiringProcessEntity

def get_hiring_process_use_case(params: dict) -> HiringProcessEntity:
    """get position by token use case."""
    hiring_process_id = params.get("hiring_process_id")
    hiring_repository = HiringProcessRepository()

    return hiring_repository.getById(hiring_process_id)
