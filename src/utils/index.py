from typing import Optional

from src.domain.user import UserEntity
from src.domain.role import BusinessRole


def get_role_business(user_entity: UserEntity, business_id: str) -> Optional[BusinessRole]:
    """Get the role for a user in a specific business."""
    return next((r for r in user_entity.props.roles if r.business_id == business_id), None)
