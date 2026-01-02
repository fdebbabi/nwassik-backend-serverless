"""Shared pytest configuration and fixtures."""

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


@pytest.fixture(scope="session")
def stage() -> str:
    """Get the deployment stage (dev, staging, prod)."""
    env = os.getenv("STAGE")
    if not env:
        pytest.fail("STAGE not set in .env")
    return env.lower()


@pytest.fixture(scope="session")
def api_endpoint() -> str:
    """Get the API endpoint from API_DOMAIN in .env."""
    domain = os.getenv("API_DOMAIN")
    if not domain:
        pytest.fail("API_DOMAIN not set in .env")
    return domain


@pytest.fixture(scope="session")
def aws_region() -> str:
    """Get AWS region from environment."""
    region = os.getenv("AWS_REGION")
    if not region:
        pytest.fail("AWS_REGION not set in .env")
    return region


@pytest.fixture(scope="session")
def aws_profile() -> str:
    """Get AWS profile from environment."""
    profile = os.getenv("AWS_PROFILE")
    if not profile:
        pytest.fail("AWS_PROFILE not set in .env")
    return profile


@pytest.fixture(scope="session")
def cognito_user_pool_id() -> str:
    """Get Cognito User Pool ID from environment."""
    pool_id = os.getenv("COGNITO_USER_POOL_ID")
    if not pool_id:
        pytest.fail("COGNITO_USER_POOL_ID not set in .env")
    return pool_id


@pytest.fixture(scope="session")
def cognito_client_id() -> str:
    """Get Cognito App Client ID from environment."""
    client_id = os.getenv("COGNITO_APP_CLIENT_ID")
    if not client_id:
        pytest.fail("COGNITO_APP_CLIENT_ID not set in .env")
    return client_id
