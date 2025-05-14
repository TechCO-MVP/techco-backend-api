from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from src.domain.base_entity import BaseEntity


class NotificationStatus(str, Enum):
    NEW = "NEW"
    READ = "READ"
    REVIEWED = "REVIEWED"


class NotificationType(str, Enum):
    PHASE_CHANGE = "PHASE_CHANGE"
    TAGGED_IN_COMMENT = "TAGGED_IN_COMMENT"
    PROFILE_FILTER_PROCESS = "PROFILE_FILTER_PROCESS"


class PHASE_TYPE(str, Enum):
    INFORMATIVE = "Informativa"
    ACTION_CALL = "Llamado a la acción"


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
    phase_type: Optional[PHASE_TYPE] = Field(default="", alias="phase_type")


class UpdateNotificationStatusDTO(BaseModel):
    notification_id: str
    status: NotificationStatus


class NotificationEntity(BaseEntity[NotificationDTO]):
    pass
