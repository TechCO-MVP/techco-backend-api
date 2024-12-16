import json

from src.adapters.primary.create_organization.index import handler


def test_create_organization_handler():
    event: dict = {}
    context: dict = {}
    response = handler(event, context)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Go Serverless v1.0! Your function executed successfully!!"
    assert body["input"] == event
