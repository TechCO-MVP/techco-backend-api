from typing import List
from src.services.graphql.graphql_service import GraphQLClient

from src.repositories.pipefy.queries.card import CREATE_CARD


class CardRepository:
    def __init__(self, graphql_client: GraphQLClient):
        self.graphql_client = graphql_client

    def create_card(self, pipe_id: str, title: str, fields_attributes: List[dict]):
        variables = {
            "input": {
                "pipe_id": pipe_id,
                "title": title,
                "fields_attributes": fields_attributes,
            }
        }
        return self.graphql_client.execute_query(CREATE_CARD, variables)
