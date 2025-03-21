from aws_lambda_powertools import Logger

from src.errors.entity_not_found import EntityNotFound
from src.models.pipefy.webhook import CardMoveEvent
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.domain.hiring_process import HiringProcessPhaseHistory, PhaseMove

logger = Logger("CardMoveEvent")


def create_hiring_process_phase_history(card_move_dto: CardMoveEvent) -> HiringProcessPhaseHistory:
    phase_from_move = PhaseMove(phase_id=card_move_dto.from_.id, name=card_move_dto.from_.name)
    phase_to_move = PhaseMove(phase_id=card_move_dto.to.id, name=card_move_dto.to.name)
    return HiringProcessPhaseHistory(from_phase=phase_from_move, to_phase=phase_to_move)


def update_phase(card_move_dto: CardMoveEvent):
    logger.info(f"Updating phase for card {card_move_dto.card.id}")
    logger.info(f"From phase: {card_move_dto.from_.id}")
    logger.info(f"To phase: {card_move_dto.to.id}")

    hiring_process_repository = HiringProcessRepository()
    hiring_process = hiring_process_repository.getByCardId(str(card_move_dto.card.id))

    if not hiring_process:
        logger.error(f"Hiring process not found for card {card_move_dto.card.id}")
        raise EntityNotFound("HiringProcess", card_move_dto.card.id)

    hiring_process.props.phase_id = card_move_dto.to.id

    if not hiring_process.props.phase_history:
        hiring_process.props.phase_history = []

    hiring_process.props.phase_history.append(create_hiring_process_phase_history(card_move_dto))

    hiring_process_repository.update(hiring_process.id, hiring_process)

    logger.info(f"Phase updated for card {card_move_dto.card.id}")
