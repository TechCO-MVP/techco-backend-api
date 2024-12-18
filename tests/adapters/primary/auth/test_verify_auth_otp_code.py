# """Tests for the verify_auth_otp_code module."""

# import json
# import unittest
# from unittest.mock import patch

# from botocore.exceptions import ClientError

# from src.adapters.primary.auth.verify_auth_otp_code import lambda_handler

# PATH = "src.adapters.primary.auth.verify_auth_otp_code."


# class TestStartAuth(unittest.TestCase):
#     """Test the verify_auth_otp_code module."""

#     def setUp(self):
#         """Set up the test."""
#         self.event = {
#             "httpMethod": "POST",
#             "headers": {"Content-Type": "application/json"},
#             "body": json.dumps(
#                 {"email": "email@test.co", "otp": "123456", "session": "fake-session"}
#             ),
#         }

#     @patch(f"{PATH}REGION_NAME", "fake-region")
#     @patch(f"{PATH}CLIENT_ID", "fake-client-id")
#     @patch(f"{PATH}cognito_client")
#     def test_verify_auth_otp_code_success(self, mock_cognito_client):
#         """Test verify_auth_otp_code success."""
#         mock_cognito_client.respond_to_auth_challenge.return_value = {
#             "AuthenticationResult": {
#                 "IdToken": "fake-id-token",
#                 "AccessToken": "fake_access_token",
#                 "RefreshToken": "fake_refresh_token",
#             }
#         }

#         response = lambda_handler(self.event, {})

#         mock_cognito_client.respond_to_auth_challenge.assert_called_once_with(
#             ClientId="fake-client-id",
#             ChallengeName="CUSTOM_CHALLENGE",
#             ChallengeResponses={"USERNAME": "email@test.co", "ANSWER": "123456"},
#             Session="fake-session",
#         )
#         self.assertEqual(response["statusCode"], 200)
#         self.assertEqual(
#             response["body"],
#             json.dumps(
#                 {
#                     "message": "Successfully authenticated.",
#                     "idToken": "fake-id-token",
#                     "accessToken": "fake_access_token",
#                     "refreshToken": "fake_refresh_token",
#                 }
#             ),
#         )

#     @patch(f"{PATH}REGION_NAME", "fake-region")
#     @patch(f"{PATH}CLIENT_ID", "fake-client-id")
#     @patch(f"{PATH}cognito_client")
#     def test_verify_auth_otp_code_sfailed(self, mock_cognito_client):
#         """Test verify_auth_otp_code success."""
#         mock_cognito_client.respond_to_auth_challenge.return_value = {"Error": "error response"}

#         response = lambda_handler(self.event, {})

#         mock_cognito_client.respond_to_auth_challenge.assert_called_once_with(
#             ClientId="fake-client-id",
#             ChallengeName="CUSTOM_CHALLENGE",
#             ChallengeResponses={"USERNAME": "email@test.co", "ANSWER": "123456"},
#             Session="fake-session",
#         )
#         self.assertEqual(response["statusCode"], 400)
#         self.assertEqual(response["body"], json.dumps({"message": "Invalid OTP code."}))

#     @patch(f"{PATH}REGION_NAME", "fake-region")
#     @patch(f"{PATH}CLIENT_ID", "fake-client-id")
#     @patch(f"{PATH}cognito_client")
#     def test_lambda_handler_client_error(self, mock_cognito_client):
#         """Test verify_auth_otp_code client error."""
#         error_response = {"Error": {"Message": "User does not exist"}}
#         mock_cognito_client.respond_to_auth_challenge.side_effect = ClientError(
#             error_response, "InitiateAuth"
#         )

#         response = lambda_handler(self.event, {})

#         self.assertEqual(response["statusCode"], 400)
#         body = json.loads(response["body"])
#         self.assertIn("Error validating OTP code:", body["error"])

#     @patch(f"{PATH}REGION_NAME", "fake-region")
#     @patch(f"{PATH}CLIENT_ID", "fake-client-id")
#     @patch(f"{PATH}cognito_client")
#     def test_lambda_handler_unexpected_error(self, mock_cognito_client):
#         """Test verify_auth_otp_code unexpected error."""
#         mock_cognito_client.respond_to_auth_challenge.side_effect = Exception("Unexpected error")

#         response = lambda_handler(self.event, {})

#         self.assertEqual(response["statusCode"], 500)
#         body = json.loads(response["body"])
#         self.assertIn("Unexpected error", body["error"])
