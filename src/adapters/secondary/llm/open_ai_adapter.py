import json
import os
from time import sleep
from typing import List

import boto3
from aws_lambda_powertools import Logger
from openai import OpenAI

from src.models.openai.index import OpenAIMessage
from src.services.llm.llm_service import LLMService

logger = Logger()


class OpenAIAdapter(LLMService):

    def __init__(self):
        api_key = self.get_secret_api_key()
        self.client = OpenAI(api_key=api_key)
        self.assistant_id = os.getenv("OPEN_AI_ASSISTANT_ID", "")

    def generate_response(
        self,
        messages: List[OpenAIMessage],
        file_path: str = None,
    ) -> str:
        file_id = self.upload_file(file_path)
        thread_run = self.create_and_run_thread(messages, file_id)
        self.wait_for_completion(thread_run)
        return self.get_thread_response(thread_run)

    def upload_file(self, file_path: str) -> str:
        with open(file_path, "rb") as file:
            uploaded_file = self.client.files.create(file=file, purpose="assistants")
        return uploaded_file.id

    def create_and_run_thread(self, messages: List[OpenAIMessage], file_id: str):
        return self.client.beta.threads.create_and_run(
            assistant_id=self.assistant_id,
            thread={
                "messages": messages,
                "tool_resources": {
                    "file_search": {
                        "vector_stores": [
                            {
                                "file_ids": [file_id],
                            }
                        ]
                    }
                },
            },
        )

    def wait_for_completion(self, thread_run):
        while True:
            run = self.client.beta.threads.runs.retrieve(
                run_id=thread_run.id,
                thread_id=thread_run.thread_id,
            )

            if run.status == "completed":
                break

            if run.status in ["failed", "incomplete", "requires_action", "expired"]:
                raise Exception(f"Run failed: {run}")

            sleep(5)

    def get_thread_response(self, thread_run) -> str:
        messages_thread = self.client.beta.threads.messages.list(thread_id=thread_run.thread_id)
        return messages_thread.data[0].content[0].text.value

    def get_secret_api_key(self) -> str:
        try:
            client = boto3.client("secretsmanager", region_name=os.getenv("REGION_NAME"))
            response = client.get_secret_value(SecretId=os.getenv("OPEN_AI_API_KEY_SECRET_NAME"))
            secret_string = json.loads(response["SecretString"])

            return secret_string["api_key"]
        except Exception as e:
            logger.error(f"Failed to get secret for OpenAI Adapter: {e}")
            raise e
