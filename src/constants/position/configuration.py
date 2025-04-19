from src.domain.assistant import ASSISTANT_TYPE
from src.domain.position_configuration import PHASE_TYPE, STATUS, Phase

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
    ]
}


assistant_phase_mapping = {
    PHASE_TYPE.DESCRIPTION: ASSISTANT_TYPE.POSITION_ASSISTANT,
    PHASE_TYPE.SOFT_SKILLS: None,
    PHASE_TYPE.TECHNICAL_TEST: None,
    PHASE_TYPE.FINAL_INTERVIEW: None,
    PHASE_TYPE.READY_TO_PUBLISH: None,
}
