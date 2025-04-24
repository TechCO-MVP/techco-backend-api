from src.domain.assistant import ASSISTANT_TYPE
from src.domain.hiring_process import Assistant

hiring_process_assistants_configuration = {
    "assistants": [
        Assistant(
            assistant_type=ASSISTANT_TYPE.POSITION_ASSISTANT.value,
            thread_id="",
            data={},
        ),
        Assistant(
            assistant_type=ASSISTANT_TYPE.TECHNICAL_ASSESSMENT_ASSISTANT.value,
            thread_id="",
            data={},
        )
    ]
}
