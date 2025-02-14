import os
from typing import List

import boto3
from openai import OpenAI

from aws_lambda_powertools import Logger

from src.services.llm.llm_service import LLMService
from src.models.openai.index import OpenAIMessage, OpenAITool

logger = Logger()


class OpenAIAdapter(LLMService):

    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.8):
        api_key = self.get_secret_api_key()
        self.client = OpenAI(model_name=model_name, temperature=temperature, api_key=api_key)

    def generate_response(
        self,
        messages: List[OpenAIMessage],
        tools: List[OpenAITool] = None,
        tool_choice: str = None,
        file_path: str = None,
    ) -> str:
        file = self.client.files.create(file=open(file_path, "rb", purpose="fine-tune"))
        response = self.client.completions.create(file=file, messages=messages, tools=tools)
        self.client.files.delete(file.id)

        return response["choices"][0]["message"]

    def get_secret_api_key(self):
        try:
            client = boto3.client("secretsmanager", region_name=os.getenv("REGION_NAME"))
            response = client.get_secret_value(SecretId=os.getenv("OPEN_AI_API_KEY_SECRET_NAME"))
            secret_string = response["SecretString"]

            return secret_string["api_key"]
        except Exception as e:
            logger.error(f"Failed to get secret for OpenAI Adapter: {e}")
            raise e
