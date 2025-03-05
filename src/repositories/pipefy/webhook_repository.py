from src.services.graphql.graphql_service import GraphQLClient

from src.repositories.pipefy.queries.webhook import CREATE_WEBHOOK, DELETE_WEBHOOK


class WebhookRepository:
    def __init__(self, graphql_client: GraphQLClient):
        self.graphql_client = graphql_client

    def create_webhook(self, pipe_id: str, url: str, name: str, actions: list[str]):
        variables = {
            "input": {
                "pipe_id": pipe_id,
                "url": url,
                "name": name,
                "actions": actions,
            }
        }
        return self.graphql_client.execute_query(CREATE_WEBHOOK, variables)

    def delete_webhook(self, webhook_id: str):
        variables = {"input": {"id": webhook_id}}
        return self.graphql_client.execute_query(DELETE_WEBHOOK, variables)
