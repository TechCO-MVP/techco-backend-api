from pydantic import BaseModel, EmailStr

from src.domain.base_entity import BaseEntity


class UserDTO(BaseModel):
    business: str
    business_id: str
    full_name: str
    email: EmailStr
    company_position: str
    rol: str


class UserEntity(BaseEntity[UserDTO]):
    pass
