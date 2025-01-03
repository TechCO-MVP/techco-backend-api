from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from src.domain.base_entity import BaseEntity


class UserStatus(str, Enum):
    ENABLE = "enable"
    DISABLE = "disable"
    PENDING = "pending"
class UserDTO(BaseModel):
    full_name: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    email: EmailStr
    company_position: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    rol: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    business_id: str = Field(..., pattern=r"^[a-zA-Z0-9 ]+$")
    status: Optional[str] = UserStatus


class UserEntity(BaseEntity[UserDTO]):
    def __init__(self, props: UserDTO):
        super().__init__(props=props)
        self.props.status = UserStatus.PENDING
