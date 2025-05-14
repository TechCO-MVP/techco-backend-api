from src.domain.assistant import ASSISTANT_TYPE
from src.repositories.document_db.business_repository import BusinessRepository
from src.domain.position_configuration import (
    FLOW_TYPE,
    PHASE_TYPE,
    STATUS,
    Phase,
    PositionConfigurationEntity
)


def get_assistant_from_business(
    position_configuration_dto: PositionConfigurationEntity, phase_type: PHASE_TYPE
) -> str:
    """Get assistant."""
    business_repository = BusinessRepository()
    business = business_repository.getById(position_configuration_dto.props.business_id)
    if not business:
        raise ValueError("Business does not exist")

    assistant_type = assistant_phase_mapping.get(phase_type)
    if not assistant_type:
        raise ValueError("Assistant type does not exist")

    assistant = business.props.assistants[assistant_type]

    if not assistant:
        raise ValueError("Assistant does not exist")

    return assistant.assistant_id


def get_assistant_from_phase(
    _: PositionConfigurationEntity, phase_type: PHASE_TYPE
) -> str:
    """Get assistant."""
    phase_type_assistant_mapping = {
        PHASE_TYPE.SOFT_SKILLS: "asst_eX6Zf5YPjXXktU6YohqrFXk6",
        PHASE_TYPE.TECHNICAL_TEST: "asst_ZZM4FpbtxliIPenYEXRy07uD",
    }

    return phase_type_assistant_mapping.get(phase_type)


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
