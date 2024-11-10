# tests/test_register_url_method.py

import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.register_url_method import APIClientURLRegister
from requests.exceptions import HTTPError


@pytest.fixture
def client():
    """Fixture for APIClientURLRegister without triggering network calls."""
    with patch.object(APIClientURLRegister, "_check_api_availability"):
        return APIClientURLRegister(base_url="https://api.example.com")


@patch("pointofpresence.client_base.requests.Session.post")
@patch.object(APIClientURLRegister, "_check_api_availability")
def test_register_url_success(mock_check_api, mock_post, client):
    """Test the register_url method with successful registration."""
    mock_check_api.return_value = None

    # Mock the POST response for a successful registration
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": "12345678-abcd-efgh-ijkl-1234567890ab"
    }
    mock_post.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "example_url_resource",
        "resource_title": "Example URL Resource",
        "owner_org": "organization_id",
        "resource_url": "https://example.com/resource",
        "file_type": "CSV",
        "notes": "This is a sample URL resource.",
        "extras": {"key1": "value1", "key2": "value2"},
        "mapping": {"field1": "mapped_field1"},
        "processing": {"delimiter": ",", "header_line": 1},
    }

    # Call the register_url method
    response = client.register_url(data)

    # Assertions to verify correct behavior
    assert response == {"id": "12345678-abcd-efgh-ijkl-1234567890ab"}
    mock_post.assert_called_once_with("https://api.example.com/url", json=data)


@patch("pointofpresence.client_base.requests.Session.post")
@patch.object(APIClientURLRegister, "_check_api_availability")
def test_register_url_key_error(mock_check_api, mock_post, client):
    """Test the register_url method with a reserved key error."""
    mock_check_api.return_value = None

    # Mock the POST response to simulate a KeyError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Reserved key error"
    )
    mock_response.json.return_value = {"detail": "Reserved key conflict"}
    mock_post.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "example_url_resource",
        "resource_title": "Example URL Resource",
        "owner_org": "organization_id",
        "resource_url": "https://example.com/resource",
        "file_type": "CSV",
        "notes": "This is a sample URL resource.",
        "extras": {"key1": "value1", "key2": "value2"},
        "mapping": {"field1": "mapped_field1"},
        "processing": {"delimiter": ",", "header_line": 1},
    }

    # Call the register_url method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.register_url(data)

    # Verify error message
    assert "Reserved key conflict" in str(exc_info.value)
    mock_post.assert_called_once_with("https://api.example.com/url", json=data)


@patch("pointofpresence.client_base.requests.Session.post")
@patch.object(APIClientURLRegister, "_check_api_availability")
def test_register_url_value_error(mock_check_api, mock_post, client):
    """Test the register_url method with invalid input."""
    mock_check_api.return_value = None

    # Mock the POST response to simulate a ValueError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Invalid input error"
    )
    mock_response.json.return_value = {"detail": "Invalid input data"}
    mock_post.return_value = mock_response

    # Define payload data
    data = {
        "resource_name": "example_url_resource",
        "resource_title": "Example URL Resource",
        "owner_org": "organization_id",
        "resource_url": "invalid_url",
        "file_type": "CSV",
        "notes": "This is a sample URL resource.",
        "extras": {"key1": "value1", "key2": "value2"},
        "mapping": {"field1": "mapped_field1"},
        "processing": {"delimiter": ",", "header_line": 1},
    }

    # Call the register_url method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.register_url(data)

    # Verify error message
    assert "Invalid input data" in str(exc_info.value)
    mock_post.assert_called_once_with("https://api.example.com/url", json=data)
