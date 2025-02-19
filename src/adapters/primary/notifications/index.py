from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = Logger()

@logger.inject_lambda_context
def lambda_handler(event, context:LambdaContext) -> None:
    logger.info("notification lambda_handler")
    logger.info(event)
    logger.info(context)

    for record in event['Records']:
        message_body = record['body']
        print(f"Processing message: {message_body}")
        # Procesar el mensaje aquí

    return
