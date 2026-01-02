"""E2E test fixtures - Cognito user management."""

import base64
import json
import time
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any

import boto3
import pytest


@dataclass
class E2EUser:
    """E2E test user data."""

    username: str
    email: str
    password: str
    id_token: str
    user_id: str


@pytest.fixture(scope="module")
def cognito_client(aws_region: str, aws_profile: str) -> Any:
    """Create Cognito client with the correct profile."""
    session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
    return session.client("cognito-idp")


@pytest.fixture(scope="module")
def test_user(
    cognito_client: Any,
    cognito_user_pool_id: str,
    cognito_client_id: str,
) -> Generator[E2EUser, None, None]:
    """Create a test user in Cognito, yield it, then clean up."""
    # Generate unique username/email
    timestamp = int(time.time())
    username = f"testuser_{timestamp}"
    email = f"testuser-{timestamp}@example.com"
    password = "TestPassword123!"

    # Create user
    cognito_client.admin_create_user(
        UserPoolId=cognito_user_pool_id,
        Username=username,
        UserAttributes=[
            {"Name": "email", "Value": email},
            {"Name": "email_verified", "Value": "true"},
            {"Name": "phone_number", "Value": "+33630633814"},
            {"Name": "phone_number_verified", "Value": "true"},
        ],
        MessageAction="SUPPRESS",
    )

    # Set password
    cognito_client.admin_set_user_password(
        UserPoolId=cognito_user_pool_id,
        Username=username,
        Password=password,
        Permanent=True,
    )

    # Authenticate and get tokens
    auth_response = cognito_client.admin_initiate_auth(
        UserPoolId=cognito_user_pool_id,
        ClientId=cognito_client_id,
        AuthFlow="ADMIN_USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": email,
            "PASSWORD": password,
        },
    )

    id_token = auth_response["AuthenticationResult"]["IdToken"]

    # Decode token to get user ID (sub claim)
    payload = id_token.split(".")[1]
    # Add padding if needed
    payload += "=" * (4 - len(payload) % 4)
    decoded = json.loads(base64.urlsafe_b64decode(payload))
    user_id = decoded["sub"]

    user = E2EUser(
        username=username,
        email=email,
        password=password,
        id_token=id_token,
        user_id=user_id,
    )

    yield user

    # Cleanup: delete user
    try:
        cognito_client.admin_delete_user(
            UserPoolId=cognito_user_pool_id,
            Username=username,
        )
    except Exception:
        pass  # Ignore cleanup errors


@pytest.fixture(scope="class")
def auth_headers(test_user: E2EUser) -> dict:
    """Get authorization headers for authenticated requests."""
    return {"Authorization": f"Bearer {test_user.id_token}"}
