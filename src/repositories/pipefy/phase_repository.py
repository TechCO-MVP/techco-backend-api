import os

from src.services.graphql.graphql_service import GraphQLClient
from src.repositories.pipefy.queries.phase import GET_PHASE_NAME


class PhaseRepository:
    def __init__(self, graphql_client: GraphQLClient):
        self.graphql_client = graphql_client

    def get_phase_name_by_id(self, phase_id: str):
        variables = {"id": phase_id}
        return self.graphql_client.execute_query(GET_PHASE_NAME, variables)
