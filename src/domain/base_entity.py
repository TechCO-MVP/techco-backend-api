import json
from datetime import datetime
from typing import Generic, TypeVar, Union

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class BaseEntity(BaseModel, Generic[T]):
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
            return json.loads(self.model_dump_json())

        return {
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            **json.loads(self.props.model_dump_json()),
        }
