import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.delete_resource_method import APIClientResourceDelete
from requests.exceptions import HTTPError


@pytest.fixture
def client():
    """Fixture for APIClientResourceDelete without triggering network calls."""
    with patch.object(APIClientResourceDelete, "_check_api_availability"):
        return APIClientResourceDelete(base_url="https://api.example.com")


@patch("pointofpresence.client_base.requests.Session.delete")
@patch.object(APIClientResourceDelete, "_check_api_availability")
def test_delete_resource_by_id_success(mock_check_api, mock_delete, client):
    """Test the delete_resource_by_id method with successful deletion."""
    mock_check_api.return_value = None

    # Mock the DELETE response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Resource deleted successfully"
    }
    mock_delete.return_value = mock_response

    # Call the delete_resource_by_id method
    response = client.delete_resource_by_id("example_id")

    # Assertions to verify correct behavior
    assert response == {"message": "Resource deleted successfully"}
    mock_delete.assert_called_once_with(
        "https://api.example.com/resource",
        params={"resource_id": "example_id"},
    )


@patch("pointofpresence.client_base.requests.Session.delete")
@patch.object(APIClientResourceDelete, "_check_api_availability")
def test_delete_resource_by_id_not_found(mock_check_api, mock_delete, client):
    """Test the delete_resource_by_id method with resource not found."""
    mock_check_api.return_value = None

    # Mock the DELETE response to simulate 404 Not Found
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Resource not found"
    )
    mock_response.json.return_value = {"detail": "Resource not found"}
    mock_delete.return_value = mock_response

    # Call the delete_resource_by_id method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.delete_resource_by_id("nonexistent_id")

    # Verify error message
    assert "Error deleting resource: Not found" in str(exc_info.value)
    mock_delete.assert_called_once_with(
        "https://api.example.com/resource",
        params={"resource_id": "nonexistent_id"},
    )


@patch("pointofpresence.client_base.requests.Session.delete")
@patch.object(APIClientResourceDelete, "_check_api_availability")
def test_delete_resource_by_name_success(mock_check_api, mock_delete, client):
    """Test the delete_resource_by_name method with successful deletion."""
    mock_check_api.return_value = None

    # Mock the DELETE response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Resource deleted successfully"
    }
    mock_delete.return_value = mock_response

    # Call the delete_resource_by_name method
    response = client.delete_resource_by_name("example_resource")

    # Assertions to verify correct behavior
    assert response == {"message": "Resource deleted successfully"}
    mock_delete.assert_called_once_with(
        "https://api.example.com/resource/example_resource"
    )


@patch("pointofpresence.client_base.requests.Session.delete")
@patch.object(APIClientResourceDelete, "_check_api_availability")
def test_delete_resource_by_name_not_found(
    mock_check_api, mock_delete, client
):
    """Test the delete_resource_by_name method with resource not found."""
    mock_check_api.return_value = None

    # Mock the DELETE response to simulate 404 Not Found
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Resource not found"
    )
    mock_response.json.return_value = {"detail": "Resource not found"}
    mock_delete.return_value = mock_response

    # Call the delete_resource_by_name method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.delete_resource_by_name("nonexistent_resource")

    # Verify error message
    assert "Error deleting resource: Not found" in str(exc_info.value)
    mock_delete.assert_called_once_with(
        "https://api.example.com/resource/nonexistent_resource"
    )
