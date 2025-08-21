from src.domain.assistant import ASSISTANT_TYPE
from src.repositories.document_db.business_repository import BusinessRepository
from src.domain.position_configuration import (
    FLOW_TYPE,
    PHASE_TYPE,
    STATUS,
    Phase,
    PositionConfigurationEntity,
)


def get_assistant_from_business(
    position_configuration: PositionConfigurationEntity, phase_type: PHASE_TYPE
) -> str:
    """Get assistant."""
    business_repository = BusinessRepository()
    business = business_repository.getById(position_configuration.props.business_id)
    if not business:
        raise ValueError("Business does not exist")

    assistant_type = assistant_phase_mapping.get(phase_type)
    if not assistant_type:
        raise ValueError("Assistant type does not exist")

    assistant = business.props.assistants[assistant_type]

    if not assistant:
        raise ValueError("Assistant does not exist")

    return assistant.assistant_id


def get_assistant_from_phase(_: PositionConfigurationEntity, phase_type: PHASE_TYPE) -> str:
    """Get assistant."""
    phase_type_assistant_mapping = {
        PHASE_TYPE.SOFT_SKILLS: "asst_eX6Zf5YPjXXktU6YohqrFXk6",
        PHASE_TYPE.TECHNICAL_TEST: "asst_5R3qT8lExjOWwDOZtck7gJhd",
    }

    return phase_type_assistant_mapping.get(phase_type)


def get_phase_data(
    position_configuration: PositionConfigurationEntity, phase_type: PHASE_TYPE
) -> dict:
    """Get position data."""
    index, phase = next(
        (
            (idx, phase)
            for idx, phase in enumerate(position_configuration.props.phases)
            if phase.type == phase_type
        ),
        (None, None),
    )

    if index is None:
        raise ValueError(f"{phase_type} phase not found")

    data = phase.data
    if not data:
        raise ValueError(f"{phase_type} phase data not found")

    return data


def get_initial_message_soft_skills(position_configuration: PositionConfigurationEntity) -> str:
    """Get initial message for soft skills."""
    business_repository = BusinessRepository()
    business = business_repository.getById(position_configuration.props.business_id)
    if not business:
        raise ValueError("Business does not exist")

    position_data = get_phase_data(position_configuration, PHASE_TYPE.DESCRIPTION)

    responsabilities = ", ".join(position_data.get("responsabilities", []))
    skills = ", ".join(skill.get("name", "") for skill in position_data.get("skills", []))

    message = f"""
    Hola!
    Descripción de la empresa: {business.props.description}
    Rol: {position_data.get("role", "No especificado")}
    Seniority: {position_data.get("seniority", "No especificado")}
    Descripción de la posición: {position_data.get("description", "No especificado")}
    Responsabilidades: {responsabilities}
    Habilidades: {skills}
    """

    return message


def get_initial_message_technical_test(position_configuration: PositionConfigurationEntity) -> str:
    """Get initial message for technical test."""
    business_repository = BusinessRepository()
    business = business_repository.getById(position_configuration.props.business_id)
    if not business:
        raise ValueError("Business does not exist")

    position_data = get_phase_data(position_configuration, PHASE_TYPE.DESCRIPTION)

    responsabilities = ", ".join(position_data.get("responsabilities", []))
    skills = ", ".join(skill.get("name", "") for skill in position_data.get("skills", []))

    soft_skills_data = get_phase_data(position_configuration, PHASE_TYPE.SOFT_SKILLS)

    is_lead_position = soft_skills_data.get("is_lead_position", False)
    how_much_autonomy = soft_skills_data.get("how_much_autonomy", "No especificado")
    challenges_of_the_position = soft_skills_data.get(
        "challenges_of_the_position", "No especificado"
    )

    message = f"""
    Hola!
    Descripción de la empresa: {business.props.description}
    Rol: {position_data.get("role", "No especificado")}
    Seniority: {position_data.get("seniority", "No especificado")}
    Descripción de la posición: {position_data.get("description", "No especificado")}
    Responsabilidades: {responsabilities}
    Habilidades: {skills}
    Es una posición de liderazgo: {"Sí" if is_lead_position else "No"}
    Cuánto nivel de autonomía tiene la posición: {how_much_autonomy}
    Cuáles son los desafíos de la posición: {challenges_of_the_position}
    """

    return message


position_configuration = {
    "phases": [
        Phase(
            name="Description",
            thread_id="",
            status=STATUS.IN_PROGRESS,
            data={},
            type=PHASE_TYPE.DESCRIPTION,
        ),
        Phase(
            name="Soft Skills",
            thread_id="",
            status=STATUS.DRAFT,
            data={},
            type=PHASE_TYPE.SOFT_SKILLS,
        ),
        Phase(
            name="Technical Test",
            thread_id="",
            status=STATUS.DRAFT,
            data={},
            type=PHASE_TYPE.TECHNICAL_TEST,
        ),
        Phase(
            name="Final Interview",
            thread_id="",
            status=STATUS.DRAFT,
            data={},
            type=PHASE_TYPE.FINAL_INTERVIEW,
        ),
        Phase(
            name="Ready to Publish",
            thread_id="",
            status=STATUS.DRAFT,
            data={},
            type=PHASE_TYPE.READY_TO_PUBLISH,
        ),
    ],
    "flow_type": {
        FLOW_TYPE.HIGH_PROFILE_FLOW: [
            Phase(
                name="Description",
                thread_id="",
                status=STATUS.DRAFT,
                data={},
                type=PHASE_TYPE.DESCRIPTION,
            ),
            Phase(
                name="Soft Skills",
                thread_id="",
                status=STATUS.DRAFT,
                data={},
                type=PHASE_TYPE.SOFT_SKILLS,
            ),
            Phase(
                name="Technical Test",
                thread_id="",
                status=STATUS.DRAFT,
                data={},
                type=PHASE_TYPE.TECHNICAL_TEST,
            ),
            Phase(
                name="Ready to Publish",
                thread_id="",
                status=STATUS.DRAFT,
                data={},
                type=PHASE_TYPE.READY_TO_PUBLISH,
            ),
        ],
        FLOW_TYPE.MEDIUM_PROFILE_FLOW: [
            Phase(
                name="Description",
                thread_id="",
                status=STATUS.DRAFT,
                data={},
                type=PHASE_TYPE.DESCRIPTION,
            ),
            Phase(
                name="Technical Test",
                thread_id="",
                status=STATUS.DRAFT,
                data={},
                type=PHASE_TYPE.TECHNICAL_TEST,
            ),
            Phase(
                name="Ready to Publish",
                thread_id="",
                status=STATUS.DRAFT,
                data={},
                type=PHASE_TYPE.READY_TO_PUBLISH,
            ),
        ],
        FLOW_TYPE.LOW_PROFILE_FLOW: [
            Phase(
                name="Description",
                thread_id="",
                status=STATUS.DRAFT,
                data={},
                type=PHASE_TYPE.DESCRIPTION,
            ),
            Phase(
                name="Soft Skills",
                thread_id="",
                status=STATUS.DRAFT,
                data={},
                type=PHASE_TYPE.SOFT_SKILLS,
            ),
            Phase(
                name="Ready to Publish",
                thread_id="",
                status=STATUS.DRAFT,
                data={},
                type=PHASE_TYPE.READY_TO_PUBLISH,
            ),
        ],
    },
}


assistant_phase_mapping = {
    PHASE_TYPE.DESCRIPTION: ASSISTANT_TYPE.POSITION_ASSISTANT,
    PHASE_TYPE.SOFT_SKILLS: None,
    PHASE_TYPE.TECHNICAL_TEST: None,
    PHASE_TYPE.FINAL_INTERVIEW: None,
    PHASE_TYPE.READY_TO_PUBLISH: None,
}


get_assistant_for_phase = {
    PHASE_TYPE.DESCRIPTION: get_assistant_from_business,
    PHASE_TYPE.SOFT_SKILLS: get_assistant_from_phase,
    PHASE_TYPE.TECHNICAL_TEST: get_assistant_from_phase,
}

get_initial_message_for_phase: dict[PHASE_TYPE, callable] = {
    PHASE_TYPE.DESCRIPTION: lambda _: "Hola!",
    PHASE_TYPE.SOFT_SKILLS: get_initial_message_soft_skills,
    PHASE_TYPE.TECHNICAL_TEST: get_initial_message_technical_test,
}
