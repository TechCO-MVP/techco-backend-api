import cgi
import io
import uuid

from src.repositories.s3.filter_profile import S3StorageRepository
from src.constants.index import S3_PROFILE_FILTER_CV_FILES_BUCKET_NAME
from src.repositories.document_db.position_repository import PositionRepository
from src.repositories.document_db.user_repository import UserRepository
from src.errors.entity_not_found import EntityNotFound
from src.domain.profile import ProfileFilterProcessQueryDTO, PROCESS_TYPE
from src.use_cases.profile.start_filter_profile_use_case import start_filter_profile_use_case


def save_cv_profile_filter_use_case(body: dict, content_type: str, headers: dict) -> tuple:
    """Use case to save CV profile filter data."""
    data = extract_body_data(body, content_type, headers)
    position_id = data.get("position_id")
    business_id = data.get("business_id")
    if not position_id or not business_id or not data.get("file"):
        raise ValueError("position_id, business_id and file are required")

    file_id = str(uuid.uuid4())
    file_type = data.get("file_type", "application/pdf").split("/")[-1]
    s3_repository = S3StorageRepository(bucket_name=S3_PROFILE_FILTER_CV_FILES_BUCKET_NAME)
    file_key = f"{business_id}/{position_id}/cv/{file_id}.{file_type}"
    s3_repository.put_raw(file_key, data.get("file"), data.get("file_type"))
    return file_key, position_id, business_id


def extract_body_data(body: dict, content_type: str, headers: dict) -> dict:
    """Extract data from the multipart/form-data body."""
    if "boundary=" not in content_type:
        raise ValueError("No boundary found in Content-Type")

    body_bytes = io.BytesIO(body)
    environ = {
        "REQUEST_METHOD": "POST",
        "CONTENT_TYPE": content_type,
        "CONTENT_LENGTH": str(len(body)),
    }

    form = cgi.FieldStorage(fp=body_bytes, environ=environ, headers=headers, keep_blank_values=True)

    data = {}
    for key in form.keys():
        if key == "file":
            file_item = form[key]
            if file_item.file:
                data["file"] = file_item.file.read()
                data["file_type"] = file_item.type or "application/pdf"
        else:
            data[key] = form[key].value

    return data


def start_filter_profile_cv_use_case(position_id: str, business_id: str, file_key: str):
    """Start filter profile CSV use case."""
    position_repository = PositionRepository()
    position = position_repository.getById(position_id)
    if not position:
        raise EntityNotFound("Position", position_id)

    user_repository = UserRepository()
    user_entity = user_repository.getById(position.props.owner_position_user_id)
    user_email = user_entity.props.email

    profile_filter_process_query_dto = ProfileFilterProcessQueryDTO(
        role=position.props.role,
        seniority=position.props.seniority,
        country_code=position.props.country_code,
        city=position.props.city,
        description=position.props.description,
        responsabilities=position.props.responsabilities,
        skills=position.props.skills,
        business_id=business_id,
        position_id=position_id,
        cv_file_key=file_key,
    )

    return start_filter_profile_use_case(
        profile_filter_process_query_dto, user_email, PROCESS_TYPE.PROFILES_CV_SEARCH
    )
