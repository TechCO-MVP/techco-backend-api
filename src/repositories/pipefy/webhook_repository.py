import os
import json

from src.services.graphql.graphql_service import GraphQLClient

from src.repositories.pipefy.queries.webhook import CREATE_WEBHOOK, DELETE_WEBHOOK
from src.utils.secrets import get_secret_by_name


class WebhookRepository:
    def __init__(self, graphql_client: GraphQLClient):
        self.graphql_client = graphql_client
        self.headers = self.get_headers()

    def create_webhook(self, pipe_id: str, url: str, name: str, actions: list[str]):
        variables = {
            "input": {
                "pipe_id": pipe_id,
                "url": url,
                "name": name,
                "actions": actions,
                "headers": json.dumps(self.headers),
            }
        }
        return self.graphql_client.execute_query(CREATE_WEBHOOK, variables)

    def delete_webhook(self, webhook_id: str):
        variables = {"input": {"id": webhook_id}}
        return self.graphql_client.execute_query(DELETE_WEBHOOK, variables)

    def get_apiwateway_api_key(self):
        secret = get_secret_by_name(os.getenv("API_GATEWAY_API_KEY_SECRET_NAME"), "json")
        return secret["api_key"]

    def get_headers(self):
        return {"x-api-key": self.get_apiwateway_api_key()}
