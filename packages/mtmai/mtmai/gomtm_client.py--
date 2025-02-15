from .mtmaisdk.clients.rest.configuration import Configuration
from .mtmaisdk.clients.rest.api_client import ApiClient
from .context import get_backend_url


def get_gomtm_client():
    backend_url = get_backend_url()
    if not backend_url:
        raise ValueError("backend_url is required")
    return ApiClient(
        configuration=Configuration(
            host=backend_url,
        )
    )
