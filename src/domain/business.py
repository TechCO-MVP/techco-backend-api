from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel

from src.domain.assistant import Assistant
from src.domain.base_entity import BaseEntity


class BUSINESS_SIZE(str, Enum):
    SMALL = "A"
    MEDIUM = "B"
    LARGE = "C"
    ENTERPRISE = "D"


class BusinessDTO(BaseModel):
    name: str
    country_code: str
    company_size: BUSINESS_SIZE
    is_admin: bool = False
    logo: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    linkedin_url: Optional[str] = None
    segment: Optional[str] = None
    industry: Optional[str] = None
    parent_business_id: Optional[str] = None
    assistants: Dict[str, Assistant] = {}


class BusinessEntity(BaseEntity[BusinessDTO]):
    def get_parent_business_id(self) -> str:
        if self.props.is_admin:
            return self.id

        return self.props.parent_business_id
