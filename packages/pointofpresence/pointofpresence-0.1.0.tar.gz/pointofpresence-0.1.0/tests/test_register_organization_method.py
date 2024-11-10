# tests/test_register_organization_method.py

import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.register_organization_method import (
    APIClientOrganizationRegister,
)
from requests.exceptions import HTTPError


@pytest.fixture
def client():
    """Fixture for APIClientOrganization without triggering network calls."""
    with patch.object(
        APIClientOrganizationRegister, "_check_api_availability"
    ):
        return APIClientOrganizationRegister(
            base_url="https://api.example.com"
        )


@patch("pointofpresence.client_base.requests.Session.post")
@patch.object(APIClientOrganizationRegister, "_check_api_availability")
def test_register_organization_success(mock_check_api, mock_post, client):
    """Test successful registration of an organization."""
    mock_check_api.return_value = None

    # Mock the POST response for a successful creation
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": "305284e6-6338-4e13-b39b-e6efe9f1c45a",
        "message": "Organization created successfully",
    }
    mock_post.return_value = mock_response

    # Define payload data
    data = {
        "name": "new_organization",
        "title": "New Organization",
        "description": "An organization for testing purposes",
    }

    # Call the register_organization method
    response = client.register_organization(data)

    # Assertions to verify correct behavior
    assert response["id"] == "305284e6-6338-4e13-b39b-e6efe9f1c45a"
    assert response["message"] == "Organization created successfully"
    mock_post.assert_called_once_with(
        "https://api.example.com/organization", json=data
    )


@patch("pointofpresence.client_base.requests.Session.post")
@patch.object(APIClientOrganizationRegister, "_check_api_availability")
def test_register_organization_name_exists(mock_check_api, mock_post, client):
    """Test registration failure due to an existing organization name."""
    mock_check_api.return_value = None

    # Mock the POST response to return a 400 error for duplicate organization
    # name
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "400 Client Error: Bad Request"
    )
    mock_response.json.return_value = {
        "detail": "Organization name already exists"
    }
    mock_post.return_value = mock_response

    # Define payload data
    data = {
        "name": "existing_organization",
        "title": "Existing Organization",
        "description": "An organization that already exists",
    }

    # Attempt to register the organization and verify the ValueError is raised
    with pytest.raises(ValueError) as exc_info:
        client.register_organization(data)

    # Verify the error message
    assert (
        str(exc_info.value)
        == "Error creating organization: Organization name already exists"
    )
    mock_post.assert_called_once_with(
        "https://api.example.com/organization", json=data
    )


@patch("pointofpresence.client_base.requests.Session.post")
@patch.object(APIClientOrganizationRegister, "_check_api_availability")
def test_register_organization_general_failure(
    mock_check_api, mock_post, client
):
    """Test registration failure with a generic error."""
    mock_check_api.return_value = None

    # Mock the POST response to raise a general 400 HTTPError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "400 Client Error: Bad Request"
    )
    mock_response.json.return_value = {"detail": "Invalid data provided"}
    mock_post.return_value = mock_response

    # Define payload data
    data = {
        "name": "invalid_organization",
        "title": "Invalid Organization",
        "description": "An invalid organization",
    }

    # Attempt to register the organization and verify the ValueError is raised
    with pytest.raises(ValueError) as exc_info:
        client.register_organization(data)

    # Verify the error message
    assert "Error creating organization: Invalid data provided" in str(
        exc_info.value
    )
    mock_post.assert_called_once_with(
        "https://api.example.com/organization", json=data
    )
