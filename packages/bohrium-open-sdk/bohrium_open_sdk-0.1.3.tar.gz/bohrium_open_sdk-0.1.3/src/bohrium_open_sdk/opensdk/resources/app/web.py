import logging

from bohrium_open_sdk.opensdk._resource import SyncAPIResource
from bohrium_open_sdk.opensdk.resources.app.web_sub_model import WebSubModel

logger = logging.getLogger(__name__)


class Web(SyncAPIResource):
    sub_model: "WebSubModel"

    def __init__(self, _client) -> None:
        self.sub_model = WebSubModel(_client)
        super().__init__(_client)
