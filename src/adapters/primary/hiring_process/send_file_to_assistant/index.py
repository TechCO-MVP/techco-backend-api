
from datetime import datetime
from typing import Dict, Any
import base64
import urllib.parse

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from src.constants.index import ENV, REGION_NAME

from src.use_cases.hiring_process.put_hiring_process_custom_fields_by_id import put_hiring_process_custom_fields_by_id_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/hiring_process/send_file_to_assistant")
def send_file_to_assistant():
    """send file to assistant"""
    try:

        # Obtener el hiring_process_id
        
        body = base64.b64decode(app.current_event.body)
        content_type = app.current_event.headers.get('Content-Type', '')
        boundary = content_type.split('boundary=')[-1]
        

        # Extraer el boundary del Content-Type
        
        # Procesar el body multipart
        # El body contendrá algo como:
        # ------WebKitFormBoundary7MA4YWxkTrZu0gW
        # Content-Disposition: form-data; name="file"; filename="example.pdf"
        # Content-Type: application/pdf
        #
        # [contenido binario del archivo]
        # ------WebKitFormBoundary7MA4YWxkTrZu0gW--
        
        # Extraer el contenido del archivo
        # Primero, dividimos por el boundary
        parts = body.split(f'--{boundary}'.encode())
        
        # Buscamos la parte que contiene el archivo
        file_content = None
        file_type = 'pdf'  # default
        hiring_process_id = None
        original_filename = None
        
        for part in parts:
            if b'Content-Disposition: form-data; name="hiring_process_id"' in part:
                hiring_process_id = part.split(b'\r\n\r\n')[1].decode().strip()
            
            # Buscar el archivo
            if b'Content-Disposition: form-data; name="file"' in part:
                # Extraer el nombre original del archivo
                if b'filename=' in part:
                    filename_part = part.split(b'filename=')[1].split(b'\r\n')[0]
                    # Decodificar el nombre del archivo si está en formato URL
                    original_filename = urllib.parse.unquote(filename_part.decode().strip('"'))
                
                if b'Content-Type:' in part:
                    file_type = part.split(b'Content-Type: ')[1].split(b'\r\n')[0].decode()
                
                file_content = part.split(b'\r\n\r\n')[1].rstrip(b'\r\n')
        
        if not file_content:
            return Response(
                status_code=400,
                body={"message": "No file found in request"},
                content_type=content_types.APPLICATION_JSON,
            )

        # Crear nombre único para el archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = original_filename if original_filename else f"file_{timestamp}"
        safe_filename = "".join(c for c in safe_filename if c.isalnum() or c in ('-', '_', '.'))
        file_key = f"{hiring_process_id}/{timestamp}_{safe_filename}"
        
        # Subir el archivo a S3
        s3_client = boto3.client('s3')
        bucket_name = f"{ENV}-techco-assessments-files-{REGION_NAME}"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=file_content,
            ContentType=file_type
        )

        # Generar la URL del archivo
        file_url = f"https://{bucket_name}.s3.{REGION_NAME}.amazonaws.com/{file_key}"

        return Response(
            status_code=200,
            body={
                "message": "File uploaded successfully",
                "file_url": file_url,
                "file_key": file_key
            },
            content_type=content_types.APPLICATION_JSON,
        )

    # except ValidationError as e:
    #     logger.error(str(e))
    #     return Response(
    #         status_code=422, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
    #     )

    except ValueError as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )

    except Exception as e:
        logger.exception("An error occurred: %s", e)
        return Response(
            status_code=500,
            body={"message": "An error occurred: %s" % e},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    """
    Handler function for send file to assistant
    request: The request object, described like:
    {
        "body": {
            "UpdateHiringProcessCustomFieldsDTO"
        }
    }
    """

    return app.resolve(event, context)
