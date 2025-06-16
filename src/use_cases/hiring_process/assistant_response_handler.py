from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.repositories.pipefy.card_repository import CardRepository
from src.use_cases.hiring_process.assistant_response import assistant_response_use_case
from src.domain.assistant import ASSISTANT_TYPE


def assistant_response_handler_use_case(
    hiring_process_id: str, run_id: str, thread_id: str, assistant_type: ASSISTANT_TYPE
) -> dict:
    response = assistant_response_use_case(hiring_process_id, run_id, thread_id, assistant_type)

    # save into custom phase
    hiring_repository = HiringProcessRepository()
    hiring_process_entity = hiring_repository.getById(hiring_process_id)

    current_phase = hiring_process_entity.props.phase_id
    current_phase_data = hiring_process_entity.props.phases.get(current_phase)

    if current_phase_data is None:
        hiring_process_entity.props.phases[current_phase] = {}

    current_phase_data = {**current_phase_data, "custom_fields": {"assistant_response": response}}
    hiring_process_entity.props.phases[current_phase] = current_phase_data
    hiring_repository.update(hiring_process_id, hiring_process_entity)

    # calculate calification as avg of all scores
    assesment_result = response.get("assessment_result", {})
    comportamientos = assesment_result.get("comportamientos", [])

    grade = 0
    for comportamiento in comportamientos:
        dimensions = comportamiento.get("dimensions", [])
        for dimension in dimensions:
            calificacion = dimension.get("calificacion", 0)
            grade += calificacion

    grade /= len(comportamientos) if comportamientos else 1
    grade = round(grade, 2)

    # save it in pipefy with graphql
    field_id = (
        "305713420_334220463_resultadodelaprueculturalst"
        if assistant_type == ASSISTANT_TYPE.SOFT_ASSESSMENT_ASSISTANT
        else "305713420_338699107_resultadodelapruebatecnicast"
    )

    card_repository = CardRepository()
    card_repository.update_card_field(
        hiring_process_entity.props.card_id,
        field_id,
        str(grade),
    )

    return {
        "assesment_response": response,
        "grade": grade,
    }
