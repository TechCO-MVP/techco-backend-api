from typing import List
from src.services.graphql.graphql_service import GraphQLClient

from src.repositories.pipefy.queries.card import CREATE_CARD, GET_CARD, UPDATE_CARD_FIELD


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

    def get_card(self, card_id: str):
        variables = {"id": card_id}
        return self.graphql_client.execute_query(GET_CARD, variables)

    def update_card_field(self, card_id: str, field_id: str, new_value: any):
        variables = {
            "input": {
                "card_id": card_id,
                "field_id": field_id,
                "new_value": new_value,
            }
        }
        return self.graphql_client.execute_query(UPDATE_CARD_FIELD, variables)
