from src.domain.position import UpdatePositionDTO, PositionDTO


def update_position_use_case(update_position_dto: UpdatePositionDTO) -> PositionDTO:
    """Update position use case."""
    # Here you would implement the logic to update the position
    # For demonstration, we'll just return the DTO as a response
    return update_position_dto.model_json_schema()
