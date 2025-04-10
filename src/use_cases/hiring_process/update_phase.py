from aws_lambda_powertools import Logger

from src.errors.entity_not_found import EntityNotFound
from src.models.pipefy.webhook import CardMoveEvent
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.repositories.document_db.position_repository import PositionRepository
from src.domain.hiring_process import HiringProcessPhaseHistory, PhaseMove, HiringProcessEntity
from src.domain.notification import NotificationDTO, NotificationType, NotificationStatus
from src.utils.send_notification_by_websocket import send_notification_by_websocket


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

    hiring_process.props.phase_id = str(card_move_dto.to.id)

    if not hiring_process.props.phase_history:
        hiring_process.props.phase_history = []

    hiring_process.props.phase_history.append(create_hiring_process_phase_history(card_move_dto))

    hiring_process_repository.update(hiring_process.id, hiring_process)
    
    build_message_to_websocket(hiring_process)

    logger.info(f"Phase updated for card {card_move_dto.card.id}")

def build_message_to_websocket(hiring_process: HiringProcessEntity):
    """ Build message to send to WebSocket connection
    """
    position_repository = PositionRepository()
    position = position_repository.getById(hiring_process.props.position_id)
    user_to_notify = [
        position.props.owner_position_user_id,
        position.props.recruiter_user_id,
        ]
    responsible_users = [user.user_id for user in position.props.responsible_users]
    user_to_notify.extend(responsible_users)
    
    for user in set(user_to_notify):
        notification = NotificationDTO(
            user_id=user,
            business_id=hiring_process.props.business_id,
            message=f"El condidato cambio de la fase {hiring_process.props.phase_history[-1].from_phase.name} a {hiring_process.props.phase_history[-1].to_phase.name}",
            notification_type=NotificationType.PHASE_CHANGE,
            status=NotificationStatus.NEW,
            hiring_process_id=hiring_process.id,
            phase_id=hiring_process.props.phase_id,
        )
        
        send_notification_by_websocket(notification)
