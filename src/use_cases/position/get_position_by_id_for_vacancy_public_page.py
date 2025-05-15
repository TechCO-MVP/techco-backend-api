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
        "position_id": position.id,
        "position_role": position.props.role,
        "position_country": position.props.country_code,
        "position_city": position.props.city,
        "position_work_mode": position.props.work_mode,
        "position_description": position.props.description,
        "position_responsabilities": position.props.responsabilities,
        "position_skills": [{'name': skill.name, 'required': skill.required} for skill in position.props.skills],
        "position_benefits": position.props.benefits or None,
        "position_salary_range": position.props.salary or None,
    }
