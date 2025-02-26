from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CardExpiration(BaseModel):
    expiredAt: Optional[datetime]
    shouldExpireAt: Optional[datetime]


class CardField(BaseModel):
    name: Optional[str]
    value: Optional[str]
    updated_at: Optional[datetime]


class CardAssignee(BaseModel):
    id: str
    assignedAt: datetime


class CardRelation(BaseModel):
    childId: str
    parentId: str
    sourceId: str
    sourceType: Optional[str]


class CardRelationship(BaseModel):
    id: str
    name: Optional[str]
    source_type: Optional[str]
    cards: Optional[List["Card"]]


class CardEdge(BaseModel):
    cursor: str
    node: Optional["Card"]


class CardConnection(BaseModel):
    edges: Optional[List[CardEdge]]
    nodes: Optional[List["Card"]]
    totalCount: int


class Pipe(BaseModel):
    id: str
    name: Optional[str]


class Phase(BaseModel):
    id: str
    name: Optional[str]


class User(BaseModel):
    id: str
    email: Optional[str]
    name: Optional[str]


class CardLateness(BaseModel):
    id: str
    reason: Optional[str]


class Card(BaseModel):
    id: str
    title: str
    age: Optional[int]
    assignees: Optional[List[CardAssignee]]
    attachments: Optional[List[str]]
    attachments_count: int
    cardAssignees: Optional[List[CardAssignee]]
    checklist_items_checked_count: int
    checklist_items_count: int
    child_relations: Optional[List[CardRelation]]
    comments: Optional[List[str]]
    comments_count: int
    created_at: Optional[datetime]
    created_by: Optional[User]
    creator_email: Optional[str]
    current_lateness: Optional[CardLateness]
    current_phase: Optional[Phase]
    current_phase_age: Optional[int]
    done: Optional[bool]
    due_date: Optional[datetime]
    emailMessagingAddress: Optional[str]
    expiration: Optional[CardExpiration]
    expired: bool
    fields: Optional[List[CardField]]
    finished_at: Optional[datetime]
    inboxEmailsRead: bool
    inbox_emails: Optional[List[str]]
    labels: Optional[List[str]]
    late: bool
    overdue: bool
    parent_relations: Optional[List[CardRelation]]
    path: Optional[str]
    phases_history: Optional[List[str]]
    pipe: Optional[Pipe]
    public_form_submitter_email: Optional[str]
    started_current_phase_at: Optional[datetime]
    subtitles: Optional[List[str]]
    suid: Optional[str]
    summary: Optional[List[str]]
    summary_attributes: Optional[List[str]]
    summary_fields: Optional[List[str]]
    updated_at: Optional[datetime]
    url: Optional[str]
    uuid: Optional[str]
