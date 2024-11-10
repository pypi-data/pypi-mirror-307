from .register_kafka_method import APIClientKafkaRegister
from .register_organization_method import APIClientOrganizationRegister
from .register_s3_method import APIClientS3Register
from .register_url_method import APIClientURLRegister
from .list_organization_method import APIClientOrganizationList
from .search_method import APIClientSearch
from .update_kafka_method import APIClientKafkaUpdate
from .update_s3_method import APIClientS3Update
from .update_url_method import APIClientURLUpdate
from .delete_organization_method import APIClientOrganizationDelete
from .delete_resource_method import APIClientResourceDelete


class APIClient(
    APIClientKafkaRegister,
    APIClientOrganizationRegister,
    APIClientS3Register,
    APIClientURLRegister,
    APIClientOrganizationList,
    APIClientSearch,
    APIClientKafkaUpdate,
    APIClientS3Update,
    APIClientURLUpdate,
    APIClientOrganizationDelete,
    APIClientResourceDelete,
):
    """Unified API Client with GET, POST, and DELETE methods."""

    pass
