from .client_base import APIClientBase
from requests.exceptions import HTTPError


class APIClientOrganizationRegister(APIClientBase):
    """Extension of APIClientBase with organization registration method."""

    def register_organization(self, data):
        """
        Register a new organization by making a POST request.

        :param data: Data for the organization.
        :return: Response JSON data with the organization ID and message.
        :raises ValueError: If the registration fails or name already exists.
        """
        url = f"{self.base_url}/organization"
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            # Retrieve the error detail if available, otherwise use the
            # error message
            error_detail = response.json().get("detail", str(e))

            # Specific error for organization name existence
            if "Group name already exists in database" in error_detail:
                raise ValueError(
                    "Error creating organization: Organization name "
                    "already exists"
                )
            else:
                raise ValueError(
                    f"Error creating organization: {error_detail}"
                )
