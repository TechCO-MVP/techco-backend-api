from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field, ValidationError, model_validator

from src.domain.base_entity import BaseEntity


class UserStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    PENDING = "pending"


class UserDTO(BaseModel):
    full_name: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    email: EmailStr
    company_position: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    rol: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    business_id: str = Field(..., pattern=r"^[a-zA-Z0-9 ]+$")
    status: Optional[UserStatus] = UserStatus.PENDING


class UserEntity(BaseEntity[UserDTO]):
    def __init__(self, props: UserDTO):
        super().__init__(props=props)
        self.props.status = UserStatus.PENDING


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


def filter_user_dto_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    user_dto_fields = list(UserDTO.model_fields.keys())
    user_dto_fields.append("_id")
    return {key: value for key, value in data.items() if key in user_dto_fields}
