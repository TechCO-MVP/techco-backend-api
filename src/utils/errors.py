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

def normalize_exception(e: Exception) -> Exception:
    """Normalize an exception to always have a dictionary as the first argument"""
    if e.args and isinstance(e.args[0], str):
        e.args = ({"message": e.args[0]},)
    elif e.args and isinstance(e.args[0], dict):
        pass
    else:
        e.args = ({"message": str(e)},)
    return e
