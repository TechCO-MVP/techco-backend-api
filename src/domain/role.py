from bson import ObjectId
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class Role(str, Enum):
    SUPER_ADMIN = "super_admin"
    BUSINESS_ADMIN = "business_admin"
    POSITION_OWNER = "position_owner"
    RECRUITER = "recruiter"


class BusinessRole(BaseModel):
    business_id: str = Field(default="", alias="business_id")
    role: Role = Field(..., alias="role")

    @field_validator("business_id", mode="before")
    def validate_and_convert_business_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            return v

        raise ValueError("Invalid business_id format. Must be a string or ObjectId.")
