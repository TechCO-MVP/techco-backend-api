from typing import List
from pydantic import BaseModel


class ProfileFilterProcessQueryDTO(BaseModel):
    role: str
    seniority: str
    country: str
    city: str
    description: str
    responsabilities: List[str]
    skills: List[str]
