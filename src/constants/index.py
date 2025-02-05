from os import environ

ENV = environ.get("ENV", "dev")

REGION_NAME = environ.get("REGION_NAME", "us-east-1")
EMAIL_OTP = "juliancastroruge@gmail.com"
UI_URI = environ.get("UI_URI", "https://develop.dzkuw34ypddf5.amplifyapp.com")

CLIENT_ID = environ.get("COGNITO_USER_POOL_CLIENT_ID", "")

# S3 Profile filter process
S3_RAW_PROFILE_DATA_IA_BUCKET_NAME = environ.get("S3_RAW_PROFILE_DATA_IA_BUCKET_NAME", "")
S3_DEPURATED_PROFILE_DATA_IA_BUCKET_NAME = environ.get(
    "S3_DEPURATED_PROFILE_DATA_IA_BUCKET_NAME", ""
)
S3_REFINED_PROFILE_DATA_IA_BUCKET_NAME = environ.get("S3_REFINED_PROFILE_DATA_IA_BUCKET_NAME", "")
