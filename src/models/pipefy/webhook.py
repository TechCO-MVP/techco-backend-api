from pydantic import BaseModel
from typing import Any


class FromToModel(BaseModel):
    id: int
    name: str


class UserModel(BaseModel):
    id: int
    name: str
    username: str
    email: str
    avatar_url: str


class CardModel(BaseModel):
    id: int
    title: str
    pipe_id: str


class FieldModel(BaseModel):
    id: str
    label: str
    internal_id: int


class CardMoveEvent(BaseModel):
    action: str
    from_: FromToModel  # 'from' is a reserved keyword in Python, so using 'from_'
    to: FromToModel
    moved_by: UserModel
    card: CardModel


class CardFieldUpdateEvent(BaseModel):
    action: str
    field: FieldModel
    new_value: Any
    updated_by: UserModel
    card: CardModel
