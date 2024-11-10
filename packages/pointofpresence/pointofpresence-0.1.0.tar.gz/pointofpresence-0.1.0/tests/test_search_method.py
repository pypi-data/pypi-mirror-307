# tests/test_search_method.py

import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.search_method import APIClientSearch
from requests.exceptions import HTTPError  # Importar HTTPError


@pytest.fixture
def client():
    """Fixture for APIClientSearch without triggering network calls."""
    with patch.object(APIClientSearch, "_check_api_availability"):
        return APIClientSearch(base_url="https://api.example.com")


def test_search_datasets_success(client):
    """Test the search_datasets method with successful results."""
    with patch("pointofpresence.client_base.requests.Session.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": "12345678-abcd-efgh-ijkl-1234567890ab",
                "name": "example_dataset_name",
                "title": "Example Dataset Title",
                "owner_org": "example_org_name",
                "description": "This is an example dataset.",
                "resources": [
                    {
                        "id": "abcd1234-efgh5678-ijkl9012",
                        "url": "http://example.com/resource",
                        "name": "Example Resource Name",
                        "description": "This is an example.",
                        "format": "CSV",
                    }
                ],
                "extras": {"key1": "value1", "key2": "value2"},
            }
        ]
        mock_get.return_value = mock_response

        # Call the search_datasets method on the client
        response = client.search_datasets(terms=["example", "dataset"])

        # Assertions
        assert response == mock_response.json()
        mock_get.assert_called_once_with(
            "https://api.example.com/search",
            params={"terms": ["example", "dataset"], "server": "local"},
        )


def test_search_datasets_no_results(client):
    """Test the search_datasets method with no matching datasets."""
    with patch("pointofpresence.client_base.requests.Session.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # Call the search_datasets method with no expected results
        response = client.search_datasets(terms=["nonexistent"])

        # Assertions
        assert response == []
        mock_get.assert_called_once_with(
            "https://api.example.com/search",
            params={"terms": ["nonexistent"], "server": "local"},
        )


def test_search_datasets_http_error(client):
    """Test the search_datasets method with an HTTP error."""
    with patch("pointofpresence.client_base.requests.Session.get") as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("HTTP Error")
        mock_response.json.return_value = {"detail": "Error occurred"}
        mock_get.return_value = mock_response

        # Call the search_datasets method and expect ValueError
        with pytest.raises(ValueError) as exc_info:
            client.search_datasets(terms=["error_term"])

        # Verify error message
        assert "Error searching for datasets: Error occurred" in str(
            exc_info.value
        )
        mock_get.assert_called_once_with(
            "https://api.example.com/search",
            params={"terms": ["error_term"], "server": "local"},
        )


def test_search_datasets_global_server(client):
    """Test the search_datasets method with the global server option."""
    with patch("pointofpresence.client_base.requests.Session.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": "23456789-abcd-efgh-ijkl-234567890abc",
                "name": "global_dataset_name",
                "title": "Global Dataset Title",
                "owner_org": "global_org_name",
                "description": "This is a global example dataset.",
            }
        ]
        mock_get.return_value = mock_response

        # Call the search_datasets method with the global server option
        response = client.search_datasets(
            terms=["global", "dataset"], server="global"
        )

        # Assertions
        assert response == mock_response.json()
        mock_get.assert_called_once_with(
            "https://api.example.com/search",
            params={"terms": ["global", "dataset"], "server": "global"},
        )
