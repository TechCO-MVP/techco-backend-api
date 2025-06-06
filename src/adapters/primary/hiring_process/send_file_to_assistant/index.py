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
        # Log del evento completo para debug
        logger.info("Event received: %s", app.current_event.raw_event)
        
        # Log de los headers
        logger.info("Headers: %s", app.current_event.headers)
        
        # Obtener el body
        body = app.current_event.body
        logger.info("Body type: %s", type(body))
        logger.info("Body first 100 chars: %s", body[:100] if body else "No body")
        
        content_type = app.current_event.headers.get('Content-Type', '')
        logger.info("Content-Type: %s", content_type)
        
        # Extraer el boundary
        if 'boundary=' not in content_type:
            return Response(
                status_code=400,
                body={"message": "No boundary found in Content-Type"},
                content_type=content_types.APPLICATION_JSON,
            )
            
        boundary = content_type.split('boundary=')[-1]
        logger.info("Boundary: %s", boundary)
        
        # Procesar el body multipart
        try:
            parts = body.split(f'--{boundary}')
            logger.info("Number of parts: %d", len(parts))
            for i, part in enumerate(parts):
                logger.info("Part %d first 100 chars: %s", i, part[:100] if part else "Empty part")
        except Exception as e:
            logger.error("Error splitting parts: %s", str(e))
            return Response(
                status_code=400,
                body={"message": "Error processing multipart form data"},
                content_type=content_types.APPLICATION_JSON,
            )
        
        file_content = None
        file_type = 'pdf'
        hiring_process_id = None
        
        for i, part in enumerate(parts):
            try:
                logger.info("Processing part %d", i)
                
                # Buscar el hiring_process_id
                if 'Content-Disposition: form-data; name="hiring_process_id"' in part:
                    try:
                        hiring_process_id = part.split('\r\n\r\n')[1].strip()
                        logger.info("Found hiring_process_id: %s", hiring_process_id)
                    except Exception as e:
                        logger.error("Error decoding hiring_process_id: %s", str(e))
                        continue
                
                # Buscar el archivo
                if 'Content-Disposition: form-data; name="file"' in part:
                    logger.info("Found file part")
                    try:
                        if 'Content-Type:' in part:
                            file_type = part.split('Content-Type: ')[1].split('\r\n')[0]
                            logger.info("File type: %s", file_type)
                        
                        # Obtener el contenido del archivo
                        file_parts = part.split('\r\n\r\n')
                        logger.info("Number of file parts after split: %d", len(file_parts))
                        for i, fp in enumerate(file_parts):
                            logger.info("File part %d length: %d", i, len(fp) if fp else 0)
                            logger.info("File part %d first 100 chars: %s", i, fp[:100] if fp else "Empty")
                        
                        if len(file_parts) > 1:
                            file_content = file_parts[1]
                            logger.info("File content type: %s", type(file_content))
                            logger.info("File content length: %d", len(file_content))
                            
                            # Manejar el contenido como base64
                            if isinstance(file_content, str):
                                logger.info("Content is string, attempting base64 decode")
                                try:
                                    # Intentar decodificar base64
                                    file_content = base64.b64decode(file_content)
                                    logger.info("Successfully decoded base64 content. New length: %d", len(file_content))
                                except Exception as e:
                                    logger.error("Base64 decode failed: %s", str(e))
                                    # Si falla base64, intentar con bytes directos
                                    try:
                                        file_content = file_content.encode('utf-8')
                                        logger.info("Using UTF-8 encoding. New length: %d", len(file_content))
                                    except Exception as e:
                                        logger.error("UTF-8 encoding failed: %s", str(e))
                                        raise
                            else:
                                logger.info("Content is already bytes, length: %d", len(file_content))
                            
                            logger.info("Final file content length: %d", len(file_content))
                            logger.info("First 100 bytes as hex: %s", file_content[:100].hex() if file_content else "No content")
                            
                            # Verificar que el contenido comienza con %PDF
                            if file_content.startswith(b'%PDF'):
                                logger.info("Content is a valid PDF file")
                            else:
                                logger.warning("Content does not start with %PDF")
                                logger.info("First 10 bytes: %s", file_content[:10].hex())
                        else:
                            logger.error("No file content found in part")
                    except Exception as e:
                        logger.error("Error processing file part: %s", str(e))
                        continue
            except Exception as e:
                logger.error("Error processing part %d: %s", i, str(e))
                continue

        if not hiring_process_id:
            return Response(
                status_code=400,
                body={"message": "hiring_process_id is required in form-data"},
                content_type=content_types.APPLICATION_JSON,
            )

        if not file_content:
            return Response(
                status_code=400,
                body={"message": "No file found in request"},
                content_type=content_types.APPLICATION_JSON,
            )

        # Crear nombre único para el archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_key = f"{hiring_process_id}/{timestamp}.{file_type.split('/')[-1]}"
        
        # Subir el archivo a S3
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
            return Response(
                status_code=500,
                body={"message": f"Error uploading to S3: {str(e)}"},
                content_type=content_types.APPLICATION_JSON,
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
