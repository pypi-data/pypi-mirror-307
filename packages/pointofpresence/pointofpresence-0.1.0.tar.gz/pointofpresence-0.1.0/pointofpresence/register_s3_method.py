from .client_base import APIClientBase
from requests.exceptions import HTTPError


class APIClientS3Register(APIClientBase):
    """Extension of APIClientBase with S3 link registration method."""

    def register_s3_link(self, data):
        """
        Register a new S3 link by making a POST request.

        :param data: Data for the S3 link.
        :return: Response JSON data with the link ID.
        :raises ValueError: If the registration fails or organization
                            does not exist.
        """
        url = f"{self.base_url}/s3"
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            # Extract error details from response JSON
            error_detail = response.json().get("detail", str(e))
            # Specific error for organization existence
            if "Organization does not exist" in error_detail:
                raise ValueError(
                    "Error creating S3 resource: Organization "
                    "(owner_org) does not exist"
                )
            # Reserved key conflict
            elif "Reserved key error" in error_detail:
                raise ValueError(
                    "Error creating S3 resource: Reserved key conflict."
                )
            # Invalid input handling
            elif "Invalid input" in error_detail:
                raise ValueError(f"Error creating S3 resource: {error_detail}")
            else:
                raise ValueError(f"Error creating S3 resource: {error_detail}")
