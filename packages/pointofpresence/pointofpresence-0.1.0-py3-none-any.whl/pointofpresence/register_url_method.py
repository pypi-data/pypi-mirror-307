# pointofpresence/register_url_method.py

from .client_base import APIClientBase
from requests.exceptions import HTTPError


class APIClientURLRegister(APIClientBase):
    """Extension of APIClientBase with URL resource registration method."""

    def register_url(self, data):
        """
        Register a new URL resource by making a POST request.

        :param data: Data for the URL resource.
        :return: Response JSON data with the resource ID.
        :raises ValueError: If the registration fails.
        """
        url = f"{self.base_url}/url"
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            # Extract error details if available
            error_detail = response.json().get("detail", str(e))
            # Custom handling for common errors
            if "Organization does not exist" in error_detail:
                raise ValueError(
                    "Error creating URL resource: Organization "
                    "(owner_org) does not exist."
                )
            elif "Group name already exists in database" in error_detail:
                raise ValueError(
                    "Error creating URL resource: Name already exists."
                )
            else:
                raise ValueError(
                    f"Error creating URL resource: {error_detail}"
                )
