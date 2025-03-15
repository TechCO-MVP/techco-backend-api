import os
import requests
from src.utils.secrets import get_secret_by_name


class GraphQLClient:

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def execute_query(self, query: str, variables: dict = None):
        """Execures a GraphQL query with error handling."""
        try:
            payload = {"query": query, "variables": variables or {}}

            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                raise Exception(f"GraphQL Error: {data["errors"]}")

            return data.get("data", {})

        except requests.RequestException as e:
            raise Exception(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")


def get_client() -> GraphQLClient:
    """Get the GraphQL client."""
    secrets = get_secret_by_name(os.getenv("PIPEFY_API_KEY_SECRET_NAME"), "json")
    return GraphQLClient(secrets["PIPEFY_API_URL"], secrets["PIPEFY_API_TOKEN"])
