import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.list_organization_method import APIClientOrganizationList
from requests.exceptions import HTTPError


@pytest.fixture
def client():
    """
    Fixture for APIClientOrganizationList without triggering network calls.
    """
    with patch.object(APIClientOrganizationList, "_check_api_availability"):
        return APIClientOrganizationList(base_url="https://api.example.com")


@patch("pointofpresence.client_base.requests.Session.get")
@patch.object(APIClientOrganizationList, "_check_api_availability")
def test_list_organizations_success(mock_check_api, mock_get, client):
    """Test the list_organizations method with successful retrieval."""
    mock_check_api.return_value = None

    # Mock the GET response for a successful request
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = ["org1", "org2", "org3"]
    mock_get.return_value = mock_response

    # Call the list_organizations method
    response = client.list_organizations()

    # Assertions to verify correct behavior
    assert response == ["org1", "org2", "org3"]
    mock_get.assert_called_once_with(
        "https://api.example.com/organization", params=None
    )


@patch("pointofpresence.client_base.requests.Session.get")
@patch.object(APIClientOrganizationList, "_check_api_availability")
def test_list_organizations_with_filter(mock_check_api, mock_get, client):
    """Test the list_organizations method with name filtering."""
    mock_check_api.return_value = None

    # Mock the GET response for a filtered request
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = ["filtered_org"]
    mock_get.return_value = mock_response

    # Call the list_organizations method with a filter
    response = client.list_organizations(name="filtered")

    # Assertions to verify correct behavior
    assert response == ["filtered_org"]
    mock_get.assert_called_once_with(
        "https://api.example.com/organization", params={"name": "filtered"}
    )


@patch("pointofpresence.client_base.requests.Session.get")
@patch.object(APIClientOrganizationList, "_check_api_availability")
def test_list_organizations_http_error(mock_check_api, mock_get, client):
    """Test the list_organizations method with an HTTP error."""
    mock_check_api.return_value = None

    # Mock the GET response to raise an HTTPError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError("Server error")
    mock_response.json.return_value = {"detail": "Server error"}
    mock_get.return_value = mock_response

    # Call the list_organizations method and expect a ValueError
    with pytest.raises(ValueError) as exc_info:
        client.list_organizations()

    # Verify error message
    assert "Error listing organizations: Server error" in str(exc_info.value)
    mock_get.assert_called_once_with(
        "https://api.example.com/organization", params=None
    )
