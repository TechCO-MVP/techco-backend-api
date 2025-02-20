from typing import List

from src.constants.index import (
    S3_RAW_PROFILE_DATA_IA_BUCKET_NAME,
    S3_DEPURATED_PROFILE_DATA_IA_BUCKET_NAME,
)
from src.repositories.s3.filter_profile import S3StorageRepository
from src.domain.profile_brightdata import ProfileBrightDataDTO

keys_remover = [
    "posts",
    "people_also_viewed",
    "volunteer_experience",
    "publications",
    "input_url",
    "linkedin_id",
    "activity",
    "honors_and_awards",
    "similar_profiles",
    "default_avatar",
    "memorialized_account",
]


def remove_keys(profiles: List[ProfileBrightDataDTO]) -> List[ProfileBrightDataDTO]:
    """Remove keys from profiles."""
    for profile in profiles:
        for key in keys_remover:
            profile.pop(key, None)

    return profiles


def transform_and_refine_use_case(process_id: str):
    """Transform and refine bright data use case."""
    s3_storage_repository = S3StorageRepository(S3_RAW_PROFILE_DATA_IA_BUCKET_NAME)
    profiles: List[ProfileBrightDataDTO] = s3_storage_repository.get(process_id, "json")

    profiles = remove_keys(profiles)

    s3_storage_repository = S3StorageRepository(S3_DEPURATED_PROFILE_DATA_IA_BUCKET_NAME)
    s3_storage_repository.put(process_id, profiles)
