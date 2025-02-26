from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Organization(BaseModel):
    id: str
    name: Optional[str]


class RepoPermissionsInternalGQL(BaseModel):
    configure_repo: bool
    create_item: bool
    delete_item: bool
    delete_repo: bool
    manage_field: bool
    manage_label: bool
    show_repo: bool


class RepoPreference(BaseModel):
    only_assignees_can_edit_cards: Optional[bool]
    public: Optional[bool]
    public_form: Optional[bool]


class PublicFormInternal(BaseModel):
    title: Optional[str]
    description: Optional[str]
    submitButtonText: Optional[str]


class PhaseFieldConnection(BaseModel):
    fields: Optional[List[str]]


class PhaseField(BaseModel):
    id: str
    label: Optional[str]
    type: Optional[str]


class PipeMember(BaseModel):
    id: str
    roleName: Optional[str]
    joinedAt: Optional[datetime]


class PipeWebhook(BaseModel):
    id: str
    name: Optional[str]
    url: Optional[str]


class Pipe(BaseModel):
    id: str
    name: str
    noun: str
    anyone_can_create_card: Optional[bool]
    canBeTagged: Optional[bool]
    cards_count: Optional[int]
    childrenRelations: Optional[List[str]]
    clone_from_id: Optional[int]
    color: Optional[str]
    conditionExpressionsFieldIds: Optional[List[str]]
    countOnlyWeekDays: Optional[bool]
    create_card_label: Optional[str]
    created_at: Optional[datetime]
    description: Optional[str]
    emailAddress: Optional[str]
    expiration_time_by_unit: Optional[int]
    expiration_unit: Optional[int]
    fieldConditions: Optional[List[str]]
    icon: Optional[str]
    improvementSetting: Optional[str]
    labels: Optional[List[str]]
    last_updated_by_card: Optional[datetime]
    members: Optional[List[PipeMember]]
    only_admin_can_remove_cards: Optional[bool]
    only_assignees_can_edit_cards: Optional[bool]
    opened_cards_count: Optional[int]
    organization: Optional[Organization]
    organizationId: str
    parentsRelations: Optional[List[str]]
    permissions: Optional[RepoPermissionsInternalGQL]
    phases: Optional[List[str]]
    preferences: Optional[RepoPreference]
    public: Optional[bool]
    publicForm: Optional[PublicFormInternal]
    reachedConcurrentBulkActionsLimit: bool
    reports: Optional[List[str]]
    role: Optional[str]
    startFormFieldConditions: Optional[List[str]]
    startFormPhaseId: Optional[str]
    start_form_fields: Optional[List[str]]
    subtitleFields: Optional[PhaseFieldConnection]
    suid: Optional[str]
    summary_attributes: Optional[List[str]]
    summary_options: Optional[List[str]]
    title_field: Optional[PhaseField]
    type: str
    users: Optional[List[str]]
    users_count: Optional[int]
    uuid: Optional[str]
    webhooks: Optional[List[PipeWebhook]]
