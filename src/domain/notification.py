from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from src.domain.base_entity import BaseEntity


class NotificationStatus(str, Enum):
    READ = "READ"
    UNREAD = "UNREAD"


class NotificationDTO(BaseModel):
    user_id: str = Field(default="", alias="user_id")
    business_id: str = Field(default="", alias="business_id")
    process: Optional[str]
    message: str
    status: NotificationStatus = NotificationStatus.UNREAD


class NotificationEntity(BaseEntity[NotificationDTO]):
    pass
