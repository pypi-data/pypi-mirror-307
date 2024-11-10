import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.update_s3_method import APIClientS3Update
from requests.exceptions import HTTPError


@pytest.fixture
def client():
    """Fixture for APIClientS3Update without triggering network calls."""
    with patch.object(APIClientS3Update, "_check_api_availability"):
        return APIClientS3Update(base_url="https://api.example.com")


@patch("pointofpresence.client_base.requests.Session.put")
@patch.object(APIClientS3Update, "_check_api_availability")
def test_update_s3_resource_success(mock_check_api, mock_put, client):
    """Test the update_s3_resource method with successful update."""
    mock_check_api.return_value = None

    # Mock the PUT response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "S3 resource updated successfully"
    }
    mock_put.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "updated_resource_name",
        "resource_s3": "http://new-s3-url.com/resource",
    }

    # Call the update_s3_resource method
    response = client.update_s3_resource(
        "12345678-abcd-efgh-ijkl-1234567890ab", data
    )

    # Assertions to verify correct behavior
    assert response == {"message": "S3 resource updated successfully"}
    mock_put.assert_called_once_with(
        "https://api.example.com/s3/12345678-abcd-efgh-ijkl-1234567890ab",
        json=data,
    )


@patch("pointofpresence.client_base.requests.Session.put")
@patch.object(APIClientS3Update, "_check_api_availability")
def test_update_s3_resource_not_found(mock_check_api, mock_put, client):
    """Test the update_s3_resource method with resource not found."""
    mock_check_api.return_value = None

    # Mock the PUT response to simulate 404 Not Found
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "S3 resource not found"
    )
    mock_response.json.return_value = {"detail": "S3 resource not found"}
    mock_put.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "updated_resource_name",
        "resource_s3": "http://new-s3-url.com/resource",
    }

    # Call the update_s3_resource method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.update_s3_resource("nonexistent-id", data)

    # Verify error message
    assert "Error updating S3 resource: Not found" in str(exc_info.value)
    mock_put.assert_called_once_with(
        "https://api.example.com/s3/nonexistent-id", json=data
    )


@patch("pointofpresence.client_base.requests.Session.put")
@patch.object(APIClientS3Update, "_check_api_availability")
def test_update_s3_resource_failure(mock_check_api, mock_put, client):
    """Test the update_s3_resource method with general failure."""
    mock_check_api.return_value = None

    # Mock the PUT response to raise an HTTPError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Error updating S3 resource"
    )
    mock_response.json.return_value = {"detail": "Error updating S3 resource"}
    mock_put.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "updated_resource_name",
        "resource_s3": "http://new-s3-url.com/resource",
    }

    # Call the update_s3_resource method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.update_s3_resource("12345678-abcd-efgh-ijkl-1234567890ab", data)

    # Verify error message
    assert "Error updating S3 resource: Error updating S3 resource" in str(
        exc_info.value
    )
    mock_put.assert_called_once_with(
        "https://api.example.com/s3/12345678-abcd-efgh-ijkl-1234567890ab",
        json=data,
    )
