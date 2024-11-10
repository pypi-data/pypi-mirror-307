from .client_base import APIClientBase
from requests.exceptions import HTTPError


class APIClientOrganizationDelete(APIClientBase):
    """Extension of APIClientBase with organization deletion method."""

    def delete_organization(self, organization_name):
        """
        Delete an organization by making a DELETE request.

        :param organization_name: Name of the organization to delete.
        :return: Response JSON data indicating success.
        :raises ValueError: If the deletion fails.
        """
        url = f"{self.base_url}/organization/{organization_name}"
        try:
            response = self.session.delete(url)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            error_detail = response.json().get("detail", str(e))
            if "Organization not found" in error_detail:
                raise ValueError("Error deleting organization: Not found")
            else:
                raise ValueError(
                    f"Error deleting organization: {error_detail}"
                )
