import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.delete_organization_method import (
    APIClientOrganizationDelete,
)
from requests.exceptions import HTTPError


@pytest.fixture
def client():
    """
    Fixture for APIClientOrganizationDelete without triggering network calls.
    """
    with patch.object(APIClientOrganizationDelete, "_check_api_availability"):
        return APIClientOrganizationDelete(base_url="https://api.example.com")


@patch("pointofpresence.client_base.requests.Session.delete")
@patch.object(APIClientOrganizationDelete, "_check_api_availability")
def test_delete_organization_success(mock_check_api, mock_delete, client):
    """Test the delete_organization method with successful deletion."""
    mock_check_api.return_value = None

    # Mock the DELETE response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Organization deleted successfully"
    }
    mock_delete.return_value = mock_response

    # Call the delete_organization method
    response = client.delete_organization("example_org")

    # Assertions to verify correct behavior
    assert response == {"message": "Organization deleted successfully"}
    mock_delete.assert_called_once_with(
        "https://api.example.com/organization/example_org"
    )


@patch("pointofpresence.client_base.requests.Session.delete")
@patch.object(APIClientOrganizationDelete, "_check_api_availability")
def test_delete_organization_not_found(mock_check_api, mock_delete, client):
    """Test the delete_organization method with organization not found."""
    mock_check_api.return_value = None

    # Mock the DELETE response to simulate 404 Not Found
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Organization not found"
    )
    mock_response.json.return_value = {"detail": "Organization not found"}
    mock_delete.return_value = mock_response

    # Call the delete_organization method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.delete_organization("nonexistent_org")

    # Verify error message
    assert "Error deleting organization: Not found" in str(exc_info.value)
    mock_delete.assert_called_once_with(
        "https://api.example.com/organization/nonexistent_org"
    )


@patch("pointofpresence.client_base.requests.Session.delete")
@patch.object(APIClientOrganizationDelete, "_check_api_availability")
def test_delete_organization_failure(mock_check_api, mock_delete, client):
    """Test the delete_organization method with general failure."""
    mock_check_api.return_value = None

    # Mock the DELETE response to raise an HTTPError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Error deleting organization"
    )
    mock_response.json.return_value = {"detail": "Error deleting organization"}
    mock_delete.return_value = mock_response

    # Call the delete_organization method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.delete_organization("example_org")

    # Verify error message
    assert "Error deleting organization: Error deleting organization" in str(
        exc_info.value
    )
    mock_delete.assert_called_once_with(
        "https://api.example.com/organization/example_org"
    )
