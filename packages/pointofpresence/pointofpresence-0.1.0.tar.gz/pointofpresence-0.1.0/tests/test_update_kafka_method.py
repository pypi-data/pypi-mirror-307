import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.update_kafka_method import APIClientKafkaUpdate
from requests.exceptions import HTTPError


@pytest.fixture
def client():
    """Fixture for APIClientKafkaUpdate without triggering network calls."""
    with patch.object(APIClientKafkaUpdate, "_check_api_availability"):
        return APIClientKafkaUpdate(base_url="https://api.example.com")


@patch("pointofpresence.client_base.requests.Session.put")
@patch.object(APIClientKafkaUpdate, "_check_api_availability")
def test_update_kafka_topic_not_found(mock_check_api, mock_put, client):
    """Test the update_kafka_topic method with dataset not found."""
    mock_check_api.return_value = None

    # Mock the PUT response to simulate 404 Not Found
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Kafka dataset not found"
    )
    mock_response.json.return_value = {"detail": "Kafka dataset not found"}
    mock_put.return_value = mock_response

    # Define payload data
    data = {
        "dataset_name": "kafka_topic_example_updated",
        "kafka_topic": "example_topic_updated",
    }

    # Call the update_kafka_topic method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.update_kafka_topic("nonexistent-id", data)

    # Verify error message
    assert "Error updating Kafka dataset: Not found" in str(exc_info.value)
    mock_put.assert_called_once_with(
        "https://api.example.com/kafka/nonexistent-id", json=data
    )


@patch("pointofpresence.client_base.requests.Session.put")
@patch.object(APIClientKafkaUpdate, "_check_api_availability")
def test_update_kafka_topic_failure(mock_check_api, mock_put, client):
    """Test the update_kafka_topic method with general failure."""
    mock_check_api.return_value = None

    # Mock the PUT response to raise an HTTPError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Error updating Kafka dataset"
    )
    mock_response.json.return_value = {
        "detail": "Error updating Kafka dataset"
    }
    mock_put.return_value = mock_response

    # Define payload data
    data = {
        "dataset_name": "kafka_topic_example_updated",
        "kafka_topic": "example_topic_updated",
    }

    # Call the update_kafka_topic method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.update_kafka_topic("12345678-abcd-efgh-ijkl-1234567890ab", data)

    # Verify error message
    assert "Error updating Kafka dataset: Error updating Kafka dataset" in str(
        exc_info.value
    )
    mock_put.assert_called_once_with(
        "https://api.example.com/kafka/12345678-abcd-efgh-ijkl-1234567890ab",
        json=data,
    )
