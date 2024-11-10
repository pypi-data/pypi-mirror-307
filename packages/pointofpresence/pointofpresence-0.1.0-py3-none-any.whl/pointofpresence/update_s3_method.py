from .client_base import APIClientBase
from requests.exceptions import HTTPError


class APIClientS3Update(APIClientBase):
    """Extension of APIClientBase with S3 resource update method."""

    def update_s3_resource(self, resource_id, data):
        """
        Update an existing S3 resource by making a PUT request.

        :param resource_id: ID of the resource to update.
        :param data: Data for updating the S3 resource.
        :return: Response JSON data indicating success.
        :raises ValueError: If the update fails.
        """
        url = f"{self.base_url}/s3/{resource_id}"
        try:
            response = self.session.put(url, json=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            error_detail = response.json().get("detail", str(e))
            if "S3 resource not found" in error_detail:
                raise ValueError("Error updating S3 resource: Not found")
            else:
                raise ValueError(f"Error updating S3 resource: {error_detail}")
