from .client_base import APIClientBase
from requests.exceptions import HTTPError


class APIClientURLUpdate(APIClientBase):
    """Extension of APIClientBase with URL resource update method."""

    def update_url_resource(self, resource_id, data):
        """
        Update an existing URL resource by making a PUT request.

        :param resource_id: ID of the resource to update.
        :param data: Data for updating the URL resource.
        :return: Response JSON data indicating success.
        :raises ValueError: If the update fails.
        """
        url = f"{self.base_url}/url/{resource_id}"
        try:
            response = self.session.put(url, json=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            error_detail = response.json().get("detail", str(e))
            if "Resource not found" in error_detail:
                raise ValueError("Error updating URL resource: Not found")
            elif "Reserved key error" in error_detail:
                raise ValueError(
                    f"Error updating URL resource: {error_detail}"
                )
            elif "Invalid input" in error_detail:
                raise ValueError(
                    f"Error updating URL resource: {error_detail}"
                )
            else:
                raise ValueError(
                    f"Error updating URL resource: {error_detail}"
                )
