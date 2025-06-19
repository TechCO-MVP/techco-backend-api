from src.domain.assistant import ASSISTANT_TYPE
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.repositories.pipefy.card_repository import CardRepository
from src.services.graphql.graphql_service import get_client
from src.use_cases.hiring_process.assistant_response import assistant_response_use_case


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

    current_phase_data = {
        **current_phase_data.model_dump(),
        "custom_fields": {"assistant_response": response},
    }
    hiring_process_entity.props.phases[current_phase] = current_phase_data
    hiring_repository.update(hiring_process_id, hiring_process_entity)

    # calculate calification as avg of all scores
    assesment_result = response.get("assessment_result", {})
    if assistant_type == ASSISTANT_TYPE.TECHNICAL_ASSESSMENT_ASSISTANT:
        grade = calculate_technical_test_grade(assesment_result)
    else:
        grade = calculate_cultural_fit_grade(assesment_result)

    # save it in pipefy with graphql
    field_id = (
        "305713420_334220463_resultadodelaprueculturaln"
        if assistant_type == ASSISTANT_TYPE.SOFT_ASSESSMENT_ASSISTANT
        else "305713420_338699107_resultadodelapruebatecnicasn"
    )

    graphql_client = get_client()
    card_repository = CardRepository(graphql_client)
    card_repository.update_card_field(
        hiring_process_entity.props.card_id,
        field_id,
        grade,
    )

    return {
        "assesment_response": response,
        "grade": grade,
    }


def calculate_technical_test_grade(technical_test_response: dict) -> float:
    """Calculate the grade for the technical test based on the response."""
    dimensions = technical_test_response.get("dimensiones", [])
    total_score = sum(dimension.get("calificacion", 0) for dimension in dimensions)
    return round(total_score / len(dimensions), 2) if dimensions else 0.0


def calculate_cultural_fit_grade(cultural_fit_response: dict) -> float:
    """Calculate the grade for the cultural fit based on the response."""
    behaviors = cultural_fit_response.get("comportamientos", [])
    total_score = sum(
        dimension.get("calificacion", 0)
        for behavior in behaviors
        for dimension in behavior.get("dimensions", [])
    )
    return round(total_score / len(behaviors), 2) if behaviors else 0.0
