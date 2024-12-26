import os
from pymongo import MongoClient
from pymongo.database import Database


def create_documentdb_client() -> Database:
    username = os.getenv("DOCUMENTDB_USERNAME")
    password = os.getenv("DOCUMENTDB_PASSWORD")
    cluster_endpoint = os.getenv("DOCUMENTDB_ENDPOINT")
    cluster_port = os.getenv("DOCUMENTDB_PORT")
    database_name = os.getenv("DOCUMENTDB_DATABASE")

    uri = (
        f"mongodb://{username}:{password}@{cluster_endpoint}:{cluster_port}/{database_name}"
        "?ssl=true&retryWrites=false"
    )
    client = MongoClient(uri)

    return client.get_database(database_name)
