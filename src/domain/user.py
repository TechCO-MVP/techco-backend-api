from enum import Enum
from typing import Any, Dict, Optional, List, Literal

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator, model_validator

from src.domain.base_entity import BaseEntity
from src.domain.role import BusinessRole


class UserStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    PENDING = "pending"

class UserDTO(BaseModel):
    full_name: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9 \s]+$")
    email: EmailStr
    company_position: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    role: Optional[str] = Field("", pattern=r"^[a-zA-Z0-9 \s]+$")
    business_id: str = Field(default="", alias="business_id")
    status: Optional[UserStatus] = UserStatus.PENDING
    roles: List[BusinessRole] = Field(..., alias="roles", min_length=1)

    @field_validator("business_id", mode="before")
    def validate_and_convert_business_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            return v

        raise ValueError("Invalid business_id format. Must be a string or ObjectId.")


class UserEntity(BaseEntity[UserDTO]):
    pass


class GetUserQueryParams(BaseModel):
    business_id: str
    id: Optional[str] = None
    all: Optional[bool] = None

    @model_validator(mode="before")
    def check_id_or_all(cls, values):
        if not values.get("id") and not values.get("all"):
            raise ValueError("Either 'id' or 'all' query parameter is required")
        return values

    @classmethod
    def validate_params(cls, params):
        try:
            return cls(**params)
        except ValidationError as e:
            raise ValueError(f"Invalid query parameters: {e}")

class UpdateUserStatusDTO(BaseModel):
    user_id: str
    user_status: Literal[UserStatus.ENABLED, UserStatus.DISABLED]
    user_email: EmailStr
    
    @classmethod
    def validate_params(cls, params):
        try:
            return cls(**params)
        except ValidationError as e:
            raise ValueError(f"Invalid parameters: {e}")
