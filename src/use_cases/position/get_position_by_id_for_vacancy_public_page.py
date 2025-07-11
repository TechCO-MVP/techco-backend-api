from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.business_repository import BusinessRepository
from src.domain.position import PositionEntity
from src.domain.business import BusinessEntity
from typing import Dict, Any



def get_position_by_id_for_vacancy_public_page(params: dict) -> list[dict]:
    """get position by id for vacancy public page."""
    
    position_repository = PositionRepository()
    position: PositionEntity = position_repository.getById(params["position_id"])

    business_repository = BusinessRepository()
    business = business_repository.getById(position.props.business_id)

    response = build_response(business, position)

    return response


def build_response(business: BusinessEntity, position: PositionEntity) -> Dict[str, Any]:
    """Build the response data for the position."""   
    
    return {
        "business_name": business.props.name,
        "business_id": business.id,
        "business_logo": business.props.logo,
        "business_description": business.props.description,
        "position_entity": position.to_dto(flat=True),
    }
