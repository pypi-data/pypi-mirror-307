import logging

from bohrium_open_sdk.opensdk._resource import SyncAPIResource
from bohrium_open_sdk.opensdk._response import APIResponse
from bohrium_open_sdk.opensdk._base_client import APIResponseManager


log = logging.getLogger(__name__)


class User(SyncAPIResource):

    def get_info(self):
        response = self._client.get("openapi/v1/ak/user")
        return APIResponse(response).json

    def list_project(self):
        with APIResponseManager(self._client.get) as api:
            uri = f"/{self._client.api_prefix}/v1/open/user/project/list"

            response = api.get_response(uri)
            return APIResponse(response).json
        
    