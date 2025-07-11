import jwt
import os
from datetime import datetime

from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.hiring_process_repository import HiringProcessRepository
from src.repositories.document_db.business_repository import BusinessRepository
from src.domain.position import PositionEntity
from src.domain.business import BusinessEntity
from src.domain.hiring_process import HiringProcessEntity
from typing import Dict, Any


class TokenExpiredException(Exception):
    """Exception raised when token has expired."""
    pass

class InvalidTokenException(Exception):
    """Exception raised when token is invalid."""
    pass


def get_position_by_token_use_case(params: dict) -> list[dict]:
    """get position by token use case."""
    
    business_repository = BusinessRepository()
    position_repository = PositionRepository()
    hiring_repository = HiringProcessRepository()

    token_data = decode_vacancy_token(params["token"])
    business = business_repository.getById(token_data["business_id"])
    position = position_repository.getById(token_data["id"])
    hiring_params = {
        "business_id": token_data["business_id"],
        "position_id": token_data["id"],
        "profile.linkedin_num_id": token_data["linkedin_num_id"]
    }
    hiring = hiring_repository.getByLinkedinNumId(hiring_params)

    validate_data(business, position, hiring)

    response = build_response(business, position, hiring)

    return response


def decode_vacancy_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate the vacancy form token.
    
    Args:
        token: The JWT token to decode
        
    Returns:
        Dictionary containing the decoded token payload
        
    Raises:
        TokenExpiredException: If the token has expired
        InvalidTokenException: If the token is invalid or cannot be decoded
    """
    try:
        payload = jwt.decode(
            token,
            os.getenv("PROFILE_FILTER_PROCESS_ARN"),
            algorithms=["HS256"]
        )

        exp_time = payload.get("exp")

        if isinstance(exp_time, str):
            exp_time = datetime.fromisoformat(exp_time)
        else:
            exp_time = datetime.fromtimestamp(exp_time)

        if exp_time and datetime.now() > exp_time:
            raise TokenExpiredException("Token has expired")
            
        return payload
        
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException("Token has expired")
    except (jwt.InvalidTokenError, jwt.DecodeError) as e:
        raise InvalidTokenException(f"Invalid token: {str(e)}")
    except Exception as e:
        raise InvalidTokenException(f"Error decoding token: {str(e)}")


def validate_data(business: BusinessEntity, position: PositionEntity, hiring: HiringProcessEntity) -> None:
    """Validate the data fetched from the repositories."""
    if not business:
        raise ValueError("Business not found")
    if not position:
        raise ValueError("Position not found")
    if not hiring:
        raise ValueError("Hiring process not found")


def build_response(business: BusinessEntity, position: PositionEntity, hiring: HiringProcessEntity) -> Dict[str, Any]:
    """Build the response data for the position."""   
    
    return {
        "business_name": business.props.name,
        "business_id": business.id,
        "business_logo": business.props.logo,
        "business_description": business.props.description,
        "hiring_id": hiring.id,
        "hiring_profile_name": hiring.props.profile.name,
        "hiring_card_id": hiring.props.card_id,
        "position_entity": position.to_dto(flat=True),
    }
