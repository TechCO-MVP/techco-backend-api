import json
import os
import requests
from time import sleep
from typing import Any, Dict, List

import boto3
from aws_lambda_powertools import Logger
from openai import OpenAI
from openai.types.beta.assistant import Assistant
from openai.types.beta.threads.run import Run
from openai.types.beta.thread import Thread

from src.adapters.secondary.llm.assistants.index import get_config_by_type
from src.adapters.secondary.llm.open_ai_tools import OpenAITools
from src.domain.assistant import ASSISTANT_TYPE
from src.models.openai.index import OpenAIMessage
from src.services.llm.llm_service import LLMService

logger = Logger("OpenAIAdapter")


class OpenAIAdapter(LLMService):

    def __init__(self, context: Dict[str, Any] = None):
        api_key = self.get_secret_api_key()
        self.client = OpenAI(api_key=api_key)
        self.assistant_id = os.getenv("OPEN_AI_ASSISTANT_ID", "")
        self.tools = OpenAITools()
        self.context = context or {}

    def generate_response(
        self,
        messages: List[OpenAIMessage],
        file_path: str = None,
        return_thread_id: bool = False,
    ) -> str:
        file_id = self.upload_file(file_path)
        sleep(60)  # Wait for the file to be indexed
        thread_run = self.create_and_run_thread(messages, file_id)
        self.wait_for_completion(thread_run)
        self.delete_file(file_id)
        return self.get_thread_response(thread_run) if not return_thread_id else thread_run.id

    def initialize_assistant_thread(self, assistant_id: str, initial_message: str = "Hola!") -> Run:
        """
        Initialize the assistant with the given ID.
        the thread is initialized with a greeting message.
        """
        logger.info("Initializing assistant thread")

        thread_run = self.client.beta.threads.create_and_run(
            assistant_id=assistant_id,
            thread={
                "messages": [
                    {
                        "role": "user",
                        "content": initial_message,
                    }
                ]
            },
        )

        return thread_run

    def create_message_thread(self, thread_id: str, message: str, role: str = "user") -> Run:
        """
        Create a message thread with the given message and role.
        """
        logger.info("Creating message thread message")

        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=message,
        )

        thread_run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
        )

        return thread_run

    def upload_file(self, file_path: str) -> str:
        with open(file_path, "rb") as file:
            uploaded_file = self.client.files.create(file=file, purpose="assistants")
        return uploaded_file.id

    def delete_file(self, file_id: str) -> bool:
        self.client.files.delete(file_id)
        return True

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

    def wait_for_completion(self, thread_run: Run) -> Run:
        while True:
            run = self.client.beta.threads.runs.retrieve(
                run_id=thread_run.id,
                thread_id=thread_run.thread_id,
            )

            if run.status in ["completed", "requires_action"]:
                return run

            if run.status in ["failed", "incomplete", "expired"]:
                raise Exception(f"Run failed: {run}")

            sleep(5)

    def run_and_process_thread(self, thread_run: Run) -> Any:
        logger.info("Running and processing thread")
        logger.info(thread_run.status)

        thread_run = self.wait_for_completion(thread_run)
        return self.handle_run_state(thread_run)

    def handle_run_state(self, thread_run: Run) -> Any:
        logger.info("Handling run state")
        logger.info(thread_run.status)

        state_handlers = {
            "completed": self.get_thread_response,
            "requires_action": self.handle_requires_action,
        }

        handler = state_handlers.get(thread_run.status)
        if not handler:
            raise Exception(f"Unsupported run state: {thread_run.status}")

        return handler(thread_run)

    def handle_requires_action(self, thread_run: Run) -> Any:
        self.complete_required_action(thread_run)
        return self.run_and_process_thread(thread_run)

    def get_thread_response(self, thread_run: Run) -> str:
        messages_thread = self.client.beta.threads.messages.list(thread_id=thread_run.thread_id)
        return messages_thread.data[0].content[0].text.value

    def complete_required_action(self, thread_run: Run):
        if thread_run.status != "requires_action":
            raise Exception("Thread run does not require action")

        tool_outputs = []
        tool_calls = thread_run.required_action.submit_tool_outputs.tool_calls

        for tool_call in tool_calls:
            tool_type = tool_call.type
            if tool_type != "function":
                raise Exception(f"Unsupported tool type: {tool_type}")

            f_name = tool_call.function.name
            f_args = tool_call.function.arguments

            output = self.tools.execute(f_name, self.context, **json.loads(f_args))
            tool_outputs.append(
                {
                    "tool_call_id": tool_call.id,
                    "output": json.dumps(output),
                }
            )

        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_run.thread_id,
            run_id=thread_run.id,
            tool_outputs=tool_outputs,
        )

    def create_assistant(self, identifier: str, type: ASSISTANT_TYPE) -> Assistant:
        """
        Create a new assistant with the given identifier,
        the identifier will be appended to the assistant name.
        """
        logger.info(f"Creating assistant with identifier: {identifier}, type: {type}")
        config = get_config_by_type(type)
        assistant = self.client.beta.assistants.create(
            name=f"{config['name']} - {identifier}",
            model=config["model"],
            instructions=config["instructions"],
            response_format=config["response_format"],
            tools=config["tools"],
        )

        logger.info(f"Assistant created with ID: {assistant.id}")
        return assistant

    def get_thread(self, thread_id: str) -> Thread:
        """
        Get the thread with the given ID.
        """
        logger.info(f"Getting thread with ID: {thread_id}")
        thread = self.client.beta.threads.retrieve(thread_id=thread_id)

        return thread

    def get_secret_api_key(self) -> str:
        try:
            client = boto3.client("secretsmanager", region_name=os.getenv("REGION_NAME"))
            response = client.get_secret_value(SecretId=os.getenv("OPEN_AI_API_KEY_SECRET_NAME"))
            secret_string = json.loads(response["SecretString"])

            return secret_string["api_key"]
        except Exception as e:
            logger.error(f"Failed to get secret for OpenAI Adapter: {e}")
            raise e

    def get_message_history(self, thread_id: str, limit: str = 20, message_id: str = None) -> dict:
        """
        Get the message history for the given thread ID and message ID.
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.get_secret_api_key()}",
            "OpenAI-Beta": "assistants=v2",
        }
        url = f"https://api.openai.com/v1/threads/{thread_id}/messages?order=desc&limit={limit}"

        if message_id:
            url += f"&after={message_id}"

        get_messages = requests.get(url, headers=headers, timeout=5)
        logger.info(f"Response from OpenAI API: {get_messages.status_code} - {get_messages.text}")

        if get_messages.status_code == 200:
            messages = get_messages.json()
            
            if not messages.get("has_more"):
                messages["data"].pop()

            return messages
        else:
            error = (
                f"Failed to get message history: {get_messages.status_code} - {get_messages.text}"
            )
            logger.error(error)
            raise Exception(error)
