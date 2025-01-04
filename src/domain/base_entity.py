import json
from datetime import datetime
from typing import Generic, TypeVar, Union

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class BaseEntity(BaseModel, Generic[T]):
    id: str = Field(default="", alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Union[datetime, None] = None
    props: T

    class Config:
        validate_assignment = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dto(self, flat=False) -> dict:
        if not flat:
            data = json.loads(self.model_dump_json())
            return {
                "_id": self.id,
                **data,
            }

        return {
            "_id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            **json.loads(self.props.model_dump_json()),
        }
