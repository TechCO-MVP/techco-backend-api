from pydantic import BaseModel, EmailStr, Field

from src.domain.base_entity import BaseEntity


class UserDTO(BaseModel):
    full_name: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    email: EmailStr
    company_position: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    rol: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    business: str = Field(..., pattern=r"^[a-zA-Z0-9 \s]+$")
    business_id: str = Field(..., pattern=r"^[a-zA-Z0-9 ]+$")


class UserEntity(BaseEntity[UserDTO]):
    pass
