import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.update_url_method import APIClientURLUpdate
from requests.exceptions import HTTPError


@pytest.fixture
def client():
    """Fixture for APIClientURLUpdate without triggering network calls."""
    with patch.object(APIClientURLUpdate, "_check_api_availability"):
        return APIClientURLUpdate(base_url="https://api.example.com")


@patch("pointofpresence.client_base.requests.Session.put")
@patch.object(APIClientURLUpdate, "_check_api_availability")
def test_update_url_resource_success(mock_check_api, mock_put, client):
    """Test the update_url_resource method with successful update."""
    mock_check_api.return_value = None

    # Mock the PUT response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Resource updated successfully"
    }
    mock_put.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "example_resource_name",
        "resource_title": "Example Resource Title",
        "owner_org": "example_org_id",
        "resource_url": "http://example.com/resource",
        "file_type": "CSV",
        "notes": "Additional notes about the resource.",
        "extras": {"key1": "value1", "key2": "value2"},
        "mapping": {"field1": "mapping1", "field2": "mapping2"},
        "processing": {
            "delimiter": ",",
            "header_line": 1,
            "start_line": 2,
            "comment_char": "#",
        },
    }

    # Call the update_url_resource method
    response = client.update_url_resource(
        "12345678-abcd-efgh-ijkl-1234567890ab", data
    )

    # Assertions to verify correct behavior
    assert response == {"message": "Resource updated successfully"}
    mock_put.assert_called_once_with(
        "https://api.example.com/url/12345678-abcd-efgh-ijkl-1234567890ab",
        json=data,
    )


@patch("pointofpresence.client_base.requests.Session.put")
@patch.object(APIClientURLUpdate, "_check_api_availability")
def test_update_url_resource_not_found(mock_check_api, mock_put, client):
    """Test the update_url_resource method with resource not found."""
    mock_check_api.return_value = None

    # Mock the PUT response to simulate 404 Not Found
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Resource not found"
    )
    mock_response.json.return_value = {"detail": "Resource not found"}
    mock_put.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "example_resource_name",
        "resource_url": "http://example.com/resource",
    }

    # Call the update_url_resource method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.update_url_resource("nonexistent-id", data)

    # Verify error message
    assert "Error updating URL resource: Not found" in str(exc_info.value)
    mock_put.assert_called_once_with(
        "https://api.example.com/url/nonexistent-id", json=data
    )


@patch("pointofpresence.client_base.requests.Session.put")
@patch.object(APIClientURLUpdate, "_check_api_availability")
def test_update_url_resource_failure(mock_check_api, mock_put, client):
    """Test the update_url_resource method with general failure."""
    mock_check_api.return_value = None

    # Mock the PUT response to raise an HTTPError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Error updating URL resource"
    )
    mock_response.json.return_value = {"detail": "Error updating URL resource"}
    mock_put.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "example_resource_name",
        "resource_url": "http://example.com/resource",
    }

    # Call the update_url_resource method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.update_url_resource(
            "12345678-abcd-efgh-ijkl-1234567890ab", data
        )

    # Verify error message
    assert "Error updating URL resource: Error updating URL resource" in str(
        exc_info.value
    )
    mock_put.assert_called_once_with(
        "https://api.example.com/url/12345678-abcd-efgh-ijkl-1234567890ab",
        json=data,
    )
