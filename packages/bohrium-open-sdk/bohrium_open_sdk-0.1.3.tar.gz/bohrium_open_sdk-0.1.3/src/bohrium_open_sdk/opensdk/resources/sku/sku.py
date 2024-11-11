import logging

from bohrium_open_sdk.opensdk._resource import SyncAPIResource
from bohrium_open_sdk.opensdk._response import APIResponse
from bohrium_open_sdk.opensdk._base_client import APIResponseManager


logger = logging.getLogger(__name__)


class Sku(SyncAPIResource):

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        scene: str = "job",
        product_line: str = "bohrium",
        choose_type: str = "cpu",
    ):
        with APIResponseManager(self._client.get) as api:
            uri = f"/{self._client.api_prefix}/v1/open/sku/list"
            params = {
                "page": page,
                "pageSize": page_size,
            }
            scene and params.update({"scene": scene})
            product_line and params.update({"productLine": product_line})
            choose_type and params.update({"chooseType": choose_type})

            response = api.get_response(uri, params=params)
            return APIResponse(response).json
        
  