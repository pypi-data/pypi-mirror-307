import logging

from bohrium_open_sdk.opensdk._resource import SyncAPIResource
from bohrium_open_sdk.opensdk._response import APIResponse
from bohrium_open_sdk.opensdk._base_client import APIResponseManager

logger = logging.getLogger(__name__)


class Stock(SyncAPIResource):

    def get_stock(self, *, sku_id: int = None):
        with APIResponseManager(self._client.get) as api:
            if not sku_id:
                raise ValueError("sku_id is required")
            uri = f"/{self._client.api_prefix}/v1/open/stock"
            params = {
                "sku_id": sku_id,
            }
            response = api.get_response(uri, params=params)
            return APIResponse(response).json
        
    def purchase(
        self,
        *,
        sku_id: int,
        sku_num: int,
        app_key: str = None,
        agreement_price: int = None, # 协议价，单位：分
        pricing_element_num: int = None, # 计价因子数量
        buy_used_amount: int = None, # 购买使用量，单位：月
    ):
        if not app_key:
            app_key = self._client.app_key
        with APIResponseManager(self._client.post) as api:
            if not app_key:
                raise ValueError("app_key is required")
            if not sku_id:
                raise ValueError("sku_id is required")
            if not sku_num or sku_num <= 0:
                raise ValueError("sku_num is not valid")
            if agreement_price != None and agreement_price <= 0:
                raise ValueError("agreement_price is not valid")
            purchase_item = {
                "marketing_type": 3,
                "sku_id": sku_id,
                "sku_num": sku_num,
            }
            agreement_price and purchase_item.update({"agreement_price": agreement_price})
            pricing_element_num and purchase_item.update({"pricing_element_num": pricing_element_num})
            buy_used_amount and purchase_item.update({"buy_used_amount": buy_used_amount})
            data = {
                "items": [purchase_item],
                "product_line": "Bohrium",
                "source_id": 1,
                "scene": "appName",
                "scene_type": 2,
                "app_name": app_key,
            }
            uri = f"/{self._client.api_prefix}/v1/open/stock/purchase"
            response = api.get_response(uri, json=data)
            return APIResponse(response).json
        
    def expend(self, *, job_id: str, sku_id: int, sku_num: int):
        with APIResponseManager(self._client.post) as api:
            if not job_id:
                raise ValueError("job_id is required")
            if not sku_id:
                raise ValueError("sku_id is required")
            if not sku_num or sku_num <= 0:
                raise ValueError("sku_num is not valid")
            data = {
                "job_id": job_id,
                "sku_id": sku_id,
                "sku_num": sku_num,
            }
            uri = f"/{self._client.api_prefix}/v1/open/stock/expend"
            response = api.get_response(uri, json=data)
            return APIResponse(response).json
        