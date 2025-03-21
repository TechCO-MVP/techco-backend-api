from pydantic import ValidationError


def format_validation_error(error: ValidationError) -> list[str]:
    """
    Format the validation error into a more readable format.
    """
    errors = []
    for err in error.errors():
        field = err["loc"][0]
        message = err["msg"]
        context = err.get("ctx", {})

        readable_error = f"Field '{field}' failed validation: {message}"
        if context:
            readable_error += f" (Additional info: {context})"

        errors.append(readable_error)

    return errors
