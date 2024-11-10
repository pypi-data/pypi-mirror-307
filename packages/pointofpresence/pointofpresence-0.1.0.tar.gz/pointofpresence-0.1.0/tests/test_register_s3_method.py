import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.register_s3_method import APIClientS3Register
from requests.exceptions import HTTPError


@pytest.fixture
def client():
    """Fixture for APIClientS3Register without triggering network calls."""
    with patch.object(APIClientS3Register, "_check_api_availability"):
        return APIClientS3Register(base_url="https://api.example.com")


@patch("pointofpresence.client_base.requests.Session.post")
@patch.object(APIClientS3Register, "_check_api_availability")
def test_register_s3_link_success(mock_check_api, mock_post, client):
    """Test the register_s3_link method with successful registration."""
    mock_check_api.return_value = None

    # Mock the POST response
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": "12345678-abcd-efgh-ijkl-1234567890ab"
    }
    mock_post.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "s3_resource_example",
        "resource_title": "S3 Resource Example",
        "owner_org": "organization_id",
        "resource_s3": "s3://bucket-name/object-key",
        "notes": "This is a sample S3 resource.",
        "extras": {"key1": "value1", "key2": "value2"},
    }

    # Call the register_s3_link method
    response = client.register_s3_link(data)

    # Assertions to verify correct behavior
    assert response == {"id": "12345678-abcd-efgh-ijkl-1234567890ab"}
    mock_post.assert_called_once_with("https://api.example.com/s3", json=data)


@patch("pointofpresence.client_base.requests.Session.post")
@patch.object(APIClientS3Register, "_check_api_availability")
def test_register_s3_link_key_error(mock_check_api, mock_post, client):
    """Test the register_s3_link method with reserved key conflict error."""
    mock_check_api.return_value = None

    # Mock the POST response to simulate a reserved key conflict
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Reserved key conflict"
    )
    mock_response.json.return_value = {"detail": "Reserved key conflict"}
    mock_post.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "s3_resource_example",
        "resource_title": "S3 Resource Example",
        "owner_org": "organization_id",
        "resource_s3": "s3://bucket-name/object-key",
        "notes": "This is a sample S3 resource.",
        "extras": {"key1": "value1", "key2": "value2"},
    }

    # Call the register_s3_link method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.register_s3_link(data)

    # Verify error message
    assert "Reserved key conflict" in str(exc_info.value)
    mock_post.assert_called_once_with("https://api.example.com/s3", json=data)


@patch("pointofpresence.client_base.requests.Session.post")
@patch.object(APIClientS3Register, "_check_api_availability")
def test_register_s3_link_value_error(mock_check_api, mock_post, client):
    """Test the register_s3_link method with invalid input error."""
    mock_check_api.return_value = None

    # Mock the POST response to simulate a ValueError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError("Invalid input")
    mock_response.json.return_value = {"detail": "Invalid input"}
    mock_post.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "s3_resource_example",
        "resource_title": "S3 Resource Example",
        "owner_org": "organization_id",
        "resource_s3": "invalid_s3_url",
        "notes": "This is a sample S3 resource.",
        "extras": {"key1": "value1", "key2": "value2"},
    }

    # Call the register_s3_link method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.register_s3_link(data)

    # Verify error message
    assert "Invalid input" in str(exc_info.value)
    mock_post.assert_called_once_with("https://api.example.com/s3", json=data)
