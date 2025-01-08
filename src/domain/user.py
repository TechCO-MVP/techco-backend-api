from bson import ObjectId
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.domain.base_entity import BaseEntity


class UserStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    PENDING = "pending"


class UserDTO(BaseModel):
    full_name: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9 \s]+$")
    email: EmailStr
    company_position: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9 \s]+$")
    role: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    business_id: str = Field(default="", alias="business_id")
    status: Optional[UserStatus] = UserStatus.PENDING

    @field_validator("business_id", mode="before")
    def validate_and_convert_business_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            return v

        raise ValueError("Invalid business_id format. Must be a string or ObjectId.")


class UserEntity(BaseEntity[UserDTO]):
    pass
