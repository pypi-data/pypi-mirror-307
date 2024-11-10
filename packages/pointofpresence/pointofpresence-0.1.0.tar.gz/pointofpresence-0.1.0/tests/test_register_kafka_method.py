import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.register_kafka_method import APIClientKafkaRegister
from requests.exceptions import HTTPError


@pytest.fixture
def client():
    """Fixture for APIClientKafka without triggering network calls."""
    with patch.object(APIClientKafkaRegister, "_check_api_availability"):
        return APIClientKafkaRegister(base_url="https://api.example.com")


@patch("pointofpresence.client_base.requests.Session.post")
@patch.object(APIClientKafkaRegister, "_check_api_availability")
def test_register_kafka_topic_success(mock_check_api, mock_post, client):
    """Test the register_kafka_topic method with successful registration."""
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
        "dataset_name": "kafka_topic_example",
        "dataset_title": "Kafka Topic Example",
        "owner_org": "organization_id",
        "kafka_topic": "example_topic",
        "kafka_host": "kafka_host",
        "kafka_port": "9092",
        "dataset_description": "Example Kafka topic for testing.",
        "extras": {"key1": "value1", "key2": "value2"},
        "mapping": {"field1": "mapping1", "field2": "mapping2"},
        "processing": {"data_key": "data", "info_key": "info"},
    }

    # Call the register_kafka_topic method
    response = client.register_kafka_topic(data)

    # Assertions to verify correct behavior
    assert response == {"id": "12345678-abcd-efgh-ijkl-1234567890ab"}
    mock_post.assert_called_once_with(
        "https://api.example.com/kafka", json=data
    )


@patch("pointofpresence.client_base.requests.Session.post")
@patch.object(APIClientKafkaRegister, "_check_api_availability")
def test_register_kafka_topic_failure(mock_check_api, mock_post, client):
    """Test the register_kafka_topic method with failed registration."""
    mock_check_api.return_value = None

    # Mock the POST response to raise an HTTPError
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError(
        "Error creating Kafka dataset"
    )
    mock_post.return_value = mock_response

    # Define payload data
    data = {
        "dataset_name": "kafka_topic_example",
        "dataset_title": "Kafka Topic Example",
        "owner_org": "organization_id",
        "kafka_topic": "example_topic",
        "kafka_host": "kafka_host",
        "kafka_port": "9092",
        "dataset_description": "Example Kafka topic for testing.",
        "extras": {"key1": "value1", "key2": "value2"},
        "mapping": {"field1": "mapping1", "field2": "mapping2"},
        "processing": {"data_key": "data", "info_key": "info"},
    }

    # Call the register_kafka_topic method and verify it raises ValueError
    with pytest.raises(ValueError) as exc_info:
        client.register_kafka_topic(data)

    # Verify error message
    assert "Error creating Kafka dataset" in str(exc_info.value)
    mock_post.assert_called_once_with(
        "https://api.example.com/kafka", json=data
    )
