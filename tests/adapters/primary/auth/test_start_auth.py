"""Tests for the start_auth module."""

import json
import unittest
from unittest.mock import patch

from botocore.exceptions import ClientError

from src.adapters.primary.auth.start_auth import lambda_handler

PATH = "src.adapters.primary.auth.start_auth."


class TestStartAuth(unittest.TestCase):
    """Test the start_auth module."""

    def setUp(self):
        """Set up the test."""
        self.event = {
            "httpMethod": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"email": "email@test.co"}),
        }

    @patch(f"{PATH}os.environ")
    @patch(f"{PATH}cognito_client")
    def test_start_auth_success(self, mock_cognito_client, mock_env):
        """Test start_auth success."""
        mock_env.__getitem__.return_value = "fake-client-id"

        mock_cognito_client.initiate_auth.return_value = {"Session": "fake-session-token"}

        response = lambda_handler(self.event, {})

        mock_cognito_client.initiate_auth.assert_called_once_with(
            AuthFlow="CUSTOM_AUTH",
            AuthParameters={"USERNAME": "email@test.co"},
            ClientId="fake-client-id",
        )
        self.assertEqual(response["statusCode"], 200)

    @patch(f"{PATH}os.environ")
    @patch(f"{PATH}cognito_client")
    def test_lambda_handler_client_error(self, mock_cognito_client, mock_env):
        """Test start_auth client error."""
        mock_env.__getitem__.return_value = "fake-client-id"

        error_response = {
            "Error": {"Code": "UserNotFoundException", "Message": "User does not exist"},
            "ResponseMetadata": {
                "RequestId": "string",
                "HostId": "string",
                "HTTPStatusCode": 400,
                "HTTPHeaders": {"header-name": "header-value"},
                "RetryAttempts": 0,
            },
        }
        mock_cognito_client.initiate_auth.side_effect = ClientError(error_response, "InitiateAuth")

        response = lambda_handler(self.event, {})

        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertIn("Failed to start authentication:", body["error"])

    @patch(f"{PATH}cognito_client")
    @patch(f"{PATH}os.environ")
    def test_lambda_handler_unexpected_error(self, mock_environ, mock_cognito_client):
        """Test start_auth unexpected error."""
        mock_environ.__getitem__.return_value = "fake-client-id"
        mock_cognito_client.initiate_auth.side_effect = Exception("Unexpected error")

        response = lambda_handler(self.event, {})

        self.assertEqual(response["statusCode"], 500)
        body = json.loads(response["body"])
        self.assertIn("Unexpected error", body["error"])
