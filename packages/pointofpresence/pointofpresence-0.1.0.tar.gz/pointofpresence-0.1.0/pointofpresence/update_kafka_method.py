from .client_base import APIClientBase
from requests.exceptions import HTTPError


class APIClientKafkaUpdate(APIClientBase):
    """Extension of APIClientBase with Kafka topic update method."""

    def update_kafka_topic(self, dataset_id, data):
        """
        Update an existing Kafka topic by making a PUT request.

        :param dataset_id: ID of the dataset to update.
        :param data: Data for updating the Kafka topic.
        :return: Response JSON data indicating success.
        :raises ValueError: If the update fails.
        """
        url = f"{self.base_url}/kafka/{dataset_id}"
        try:
            response = self.session.put(url, json=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            error_detail = response.json().get("detail", str(e))
            if "Kafka dataset not found" in error_detail:
                raise ValueError("Error updating Kafka dataset: Not found")
            else:
                raise ValueError(
                    f"Error updating Kafka dataset: {error_detail}"
                )
