from src.domain.position import (
    PositionDTO,
    PositionEntity,
    Skill,
    Languages,
    LEVEL,
    POSITION_STATUS,
    Salary,
)
from src.domain.position_configuration import PHASE_TYPE, Phase, PositionConfigurationEntity, STATUS
from src.repositories.document_db.position_configuration_repository import (
    PositionConfigurationRepository,
)
from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.user_repository import UserRepository
from src.repositories.document_db.business_repository import BusinessRepository


def create_position_use_case(
    position_configuration_id: str,
    user_email: str,
) -> PositionEntity:
    """
    Use case to create a position based on a position configuration.
    """
    position_configuration_repository = PositionConfigurationRepository()
    position_configuration_entity = position_configuration_repository.getById(
        position_configuration_id
    )

    if not position_configuration_entity:
        raise ValueError("Position configuration not found")

    if position_configuration_entity.props.current_phase not in [
        PHASE_TYPE.FINAL_INTERVIEW,
        PHASE_TYPE.READY_TO_PUBLISH,
    ]:
        raise ValueError("Position configuration is not in a valid phase to create a position")

    user_repository = UserRepository()
    user_entity = user_repository.getByEmail(user_email)
    if not user_entity:
        raise ValueError("User not found")

    business_id = position_configuration_entity.props.business_id
    role = next((r for r in user_entity.props.roles if r.business_id == business_id), None)
    if not role:
        raise ValueError("Role not found for the given business id")

    position_repository = PositionRepository()
    position_entity = position_repository.getAll(
        {position_configuration_id: position_configuration_id}
    )
    if position_entity:
        raise ValueError("Position already exists for this configuration")

    phase_function_map = {
        PHASE_TYPE.SOFT_SKILLS: create_soft_skills_assistant,
        PHASE_TYPE.TECHNICAL_TEST: create_soft_skills_assistant,
    }

    position_dto: PositionDTO = None
    for phase in position_configuration_entity.props.phases:
        if phase.type == PHASE_TYPE.DESCRIPTION:
            position_dto = create_position(phase, position_configuration_entity)
        else:
            _f = phase_function_map.get(phase.type)
            if not _f:
                continue

            position_dto = _f(phase, position_dto)

    if not position_dto:
        raise ValueError("Position DTO was not able to be created")

    position_dto.owner_position_user_id = user_entity.id

    position_repository = PositionRepository()
    position_entity = PositionEntity(props=position_dto)
    position_entity = position_repository.create(position_entity)

    if not position_entity:
        raise ValueError("Position entity was not able to be created")

    position_configuration_entity.props.status = STATUS.COMPLETED
    position_configuration_repository.update(
        position_configuration_id, position_configuration_entity
    )

    return position_entity


def create_position(
    phase: Phase, position_configuration: PositionConfigurationEntity
) -> PositionDTO:
    """
    Create a position based on the given phase.
    """
    business_id = position_configuration.props.business_id
    if not business_id:
        raise ValueError("Business ID is required in the position configuration")

    business_repository = BusinessRepository()
    business = business_repository.getById(business_id)
    if not business:
        raise ValueError("Business does not exist")

    data = phase.data
    if not data:
        raise ValueError("No data found in the description phase")

    skills = [Skill(name=skill.get("name"), required=False) for skill in data.get("skills", [])]
    if data.get("languages"):
        languages = [
            Languages(name=language.get("name"), level=language.get("level"))
            for language in data.get("languages", [])
        ]
    else:
        languages = []

    salary = Salary(
        currency=data.get("salary", {}).get("currency", None),
        salary=data.get("salary", {}).get("salary", None),
        salary_range=data.get("salary", {}).get("salary_range", None),
        disclosed=data.get("salary", {}).get("disclosed", True),
    )

    if salary.salary is None and salary.salary_range is None:
        salary = None

    position_flow = business.props.position_flows.get(position_configuration.props.flow_type)
    if not position_flow:
        raise ValueError(
            f"Position flow for type {position_configuration.props.flow_type} not found in business"
        )

    position_dto = PositionDTO(
        position_configuration_id=position_configuration.id,
        business_id=business_id,
        owner_position_user_id="",
        recruiter_user_id=data.get("recruiter_user_id", ""),
        responsible_users=data.get("responsible_users"),
        flow_type=position_configuration.props.flow_type,
        role=data.get("role"),
        seniority=data.get("seniority"),
        country_code=data.get("country_code"),
        city=data.get("city"),
        description=data.get("description"),
        responsabilities=data.get("responsabilities"),
        skills=skills,
        languages=languages,
        hiring_priority=data.get("hiring_priority", LEVEL.MEDIUM),
        work_mode=data.get("work_mode"),
        status=POSITION_STATUS.ACTIVE,
        benefits=data.get("benefits", []),
        salary=salary,
        position_flow=position_flow,
        education=data.get("education", []),
        business_configuration=business.props.business_configuration,
    )
    return position_dto


def create_soft_skills_assistant(phase: Phase, position_dto: PositionDTO) -> PositionDTO:
    """
    Create a soft skills assistant for the given position.
    """
    return position_dto


def create_technical_test_assistant(phase: Phase, position_dto: PositionDTO) -> PositionDTO:
    """
    Create a technical test assistant for the given position.
    """
    return position_dto
