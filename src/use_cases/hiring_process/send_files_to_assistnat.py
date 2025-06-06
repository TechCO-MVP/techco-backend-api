import cgi
import io
import boto3

from datetime import datetime
from aws_lambda_powertools import Logger

from src.constants.index import ENV, REGION_NAME


logger = Logger()

def send_file_to_assistant_use_case(body: dict, content_type: str, headers: dict) -> tuple:
    """put hiring process custom fileds by id use case."""

    url_s3 = save_file_to_s3(body, content_type, headers)

    return url_s3



def save_file_to_s3(body: dict, content_type: str, headers: dict) -> tuple:
    """save file to s3"""
    if 'boundary=' not in content_type:
        raise ValueError("No boundary found in Content-Type")
        
    body_io = io.BytesIO(body)
    environ = {
        'REQUEST_METHOD': 'POST',
        'CONTENT_TYPE': content_type,
        'CONTENT_LENGTH': str(len(body))
    }
    
    form = cgi.FieldStorage(
        fp=body_io,
        environ=environ,
        headers=headers,
        keep_blank_values=True
    )
    
    file_content = None
    file_type = 'pdf'
    hiring_process_id = None
    
    for key in form.keys():
        
        if key == 'hiring_process_id':
            hiring_process_id = form[key].value
        elif key == 'file':
            file_item = form[key]
            
            if file_item.file:
                file_content:str = file_item.file.read()
                file_type = file_item.type or 'application/pdf'

                if file_content.startswith(b'%PDF'):
                    logger.info("Content is a valid PDF file")
                else:
                    logger.warning("Content does not start with %PDF")
                    raise ValueError("Content does not start with %PDF")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_key = f"{hiring_process_id}/{timestamp}.{file_type.split('/')[-1]}"
    s3_client = boto3.client('s3')
    bucket_name = f"{ENV}-techco-assessments-files-{REGION_NAME}"
    
    try:
        logger.info("Uploading file to S3. Content length: %d", len(file_content))
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=file_content,
            ContentType=file_type
        )
        logger.info("File uploaded successfully to S3")
    except Exception as e:
        logger.error("Error uploading to S3: %s", str(e))
        raise ValueError(f"Error uploading to S3: {str(e)}")

    return f"https://{bucket_name}.s3.{REGION_NAME}.amazonaws.com/{file_key}"