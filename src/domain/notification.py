from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from src.domain.base_entity import BaseEntity
from src.domain.business import PHASE_CLASSIFICATION


class NotificationStatus(str, Enum):
    NEW = "NEW"
    READ = "READ"
    REVIEWED = "REVIEWED"


class NotificationType(str, Enum):
    PHASE_CHANGE = "PHASE_CHANGE"
    TAGGED_IN_COMMENT = "TAGGED_IN_COMMENT"
    PROFILE_FILTER_PROCESS = "PROFILE_FILTER_PROCESS"


class PHASE_NAME(str, Enum):
    SUGGESTED_CANDIDATES = "Candidatos sugeridos"
    OFFER_SENT = "Oferta enviada"
    INITIAL_FILTER = "Filtro inicial"
    FIRST_INTERVIEW_REQUESTED = "Primera entrevista solicitada"
    FIRST_INTERVIEW_SCHEDULED = "Primera entrevista programada"
    FIRST_INTERVIEW_FEEDBACK = "Feedback primera entrevista"
    FIRST_INTERVIEW_RESULT = "Resultado primer entrevista"
    CULTURAL_FIT_TEST = "Test de fit Cultural"
    CULTURAL_FIT_TEST_RESULT = "Resultado test Fit Cultural"
    FINAL_INTERVIEW_REQUESTED = "Entrevista final solicitada"
    FINAL_INTERVIEW_SCHEDULED = "Entrevista final programada"
    FINAL_INTERVIEW_FEEDBACK = "Feedback entrevista final "
    FINAL_INTERVIEW_RESULT = "Resultado entrevista final"
    FINALISTS = "Finalistas"
    SELECTED_CANDIDATE = "Candidato seleccionado"

class NotificationDTO(BaseModel):
    user_id: str = Field(default="", alias="user_id")
    business_id: str = Field(default="", alias="business_id")
    message: str
    notification_type: NotificationType
    status: NotificationStatus = NotificationStatus.NEW
    process: Optional[str] = Field(default="", alias="process")
    position_id: Optional[str] = Field(default="", alias="position_id")
    hiring_process_id: Optional[str] = Field(default="", alias="hiring_process_id")
    read_at: Optional[str] = Field(default=None, alias="read_at")
    phase_id: Optional[str] = Field(default="", alias="phase_id")
    phase_name: Optional[str] = Field(default="", alias="phase_name")
    phase_type: Optional[PHASE_CLASSIFICATION] = Field(default="", alias="phase_type")


class UpdateNotificationStatusDTO(BaseModel):
    notification_id: str
    status: NotificationStatus


class NotificationEntity(BaseEntity[NotificationDTO]):
    pass
