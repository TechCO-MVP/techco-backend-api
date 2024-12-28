from enum import Enum

from pydantic import BaseModel

from src.domain.base_entity import BaseEntity


class BUSINESS_SIZE(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class BusinessDTO(BaseModel):
    name: str
    is_admin: bool = False
    segment: str
    country_code: str
    size: BUSINESS_SIZE


class BusinessEntity(BaseEntity[BusinessDTO]):
    pass
