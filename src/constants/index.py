from os import environ

ENV = environ.get("ENV", "dev")

REGION_NAME = environ.get("REGION_NAME", "us-east-1")
EMAIL_OTP = "tech@techco.pe"
UI_URI = environ.get("UI_URI", "https://develop.dzkuw34ypddf5.amplifyapp.com/es/signin")

CLIENT_ID = environ.get("COGNITO_USER_POOL_CLIENT_ID", "")

# S3 Profile filter process
S3_RAW_PROFILE_DATA_IA_BUCKET_NAME = environ.get("S3_RAW_PROFILE_DATA_IA_BUCKET_NAME", "")
S3_DEPURATED_PROFILE_DATA_IA_BUCKET_NAME = environ.get(
    "S3_DEPURATED_PROFILE_DATA_IA_BUCKET_NAME", ""
)
S3_REFINED_PROFILE_DATA_IA_BUCKET_NAME = environ.get("S3_REFINED_PROFILE_DATA_IA_BUCKET_NAME", "")
S3_ASSESSMENTS_FILES_BUCKET_NAME = environ.get("S3_ASSESSMENTS_FILES_BUCKET_NAME", "")

DEFAULT_PIPE_TEMPLATE_ID = environ.get("PIPE_TEMPLATE_ID", "305713420")
MEDIUM_PROFILE_PIPE_TEMPLATE_ID = environ.get("MEDIUM_PROFILE_PIPE_TEMPLATE_ID", "306379995")
LOW_PROFILE_PIPE_TEMPLATE_ID = environ.get("LOW_PROFILE_PIPE_TEMPLATE_ID", "306376951")

API_URL = environ.get("API_URL", "https://zcich4tlm3.execute-api.us-east-1.amazonaws.com/dev")

TOKEN_SERVICE_BRIGHTDATA_SECRET_NAME = environ.get("TOKEN_SERVICE_BRIGHTDATA", "")
TABLE_WEBSOCKET_CONNECTIONS = f"{ENV}-websocket-connections"
TABLE_WEBSOCKET_CONNECTIONS_PUBLIC = f"{ENV}-websocket-connections-public"
API_ID = environ.get("API_ID", "y7fav1lech")
