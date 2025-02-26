import os

from src.services.graphql.graphql_service import GraphQLClient
from src.repositories.pipefy.queries.pipe import GET_PIPE, CLONE_PIPES


class PipeRepository:
    def __init__(self, graphql_client: GraphQLClient):
        self.graphql_client = graphql_client

    def get_pipe_by_id(self, pipe_id: str):
        variables = {"id": pipe_id}
        return self.graphql_client.execute_query(GET_PIPE, variables)

    def clone_pipe(self, pipe_id: str):
        variables = {
            "input": {
                "pipe_template_ids": [pipe_id],
                "organization_id": os.getenv("PIPEFY_ORGANIZATION_ID"),
            }
        }
        return self.graphql_client.execute_query(CLONE_PIPES, variables)
