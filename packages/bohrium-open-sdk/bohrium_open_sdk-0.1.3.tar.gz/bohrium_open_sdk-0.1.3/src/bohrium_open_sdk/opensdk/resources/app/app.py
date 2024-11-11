from enum import Enum
from bohrium_open_sdk.opensdk.resources.app.app_job import AppJob
from bohrium_open_sdk.opensdk._resource import SyncAPIResource
from bohrium_open_sdk.opensdk._response import APIResponse
from bohrium_open_sdk.opensdk._base_client import APIResponseManager
from dp.launching.typing import BaseModel


class NoticeTypeEnum(str, Enum):
    MAIL = "mail" # 邮件通知
    # SMS = "sms" # 短信通知, 暂不支持
    BOHRIUM_NOTICE = "notice" # 站内信通知
    
class SceneTypeEnum(str, Enum):
    WEB_APP = "webApp" # 自定义 web 场景

class SendNoticePayloadMail(BaseModel):
    subject: str
    body: str

class BohriumNoticeKindIdEnum(int, Enum):
    NOTICE_APP_NEW_MESSAGE = 34 # 新的 App 消息


class SendNoticePayloadBohriumNotice(BaseModel):
    kindId: BohriumNoticeKindIdEnum
    link: str = ""
    content: str = ""
    contentEN: str = ""


class SendNoticePayload(BaseModel):
    mail: SendNoticePayloadMail = None
    notice: SendNoticePayloadBohriumNotice = None
    

class App(SyncAPIResource):
    job: AppJob

    def __init__(self, _client) -> None:
        self.job = AppJob(_client)
        super().__init__(_client)

    def get_app_info(self, app_key: str):
        response = self._client.get(
            "/openapi/v1/square/app/schema", params={"appKey": app_key}
        )
        return APIResponse(response).json
    
    def send_notice(
        self,
        notice_type: NoticeTypeEnum,
        to_user_id: int,
        payload: SendNoticePayload,
        scene_type: SceneTypeEnum = SceneTypeEnum.WEB_APP,
    ):
        with APIResponseManager(self._client.post) as api:
            if not notice_type:
                raise ValueError("notice_type is required")
            if not scene_type:
                raise ValueError("scene_type is required")
            if not to_user_id:
                raise ValueError("to_user_id is required")
            if not payload or (not payload.mail and not payload.notice):
                raise ValueError("payload is required")
            if not self._client.app_key:
                raise ValueError("app_key is required")
            
            uri = f"{self._client.api_prefix}/v1/square/app/admin/send_notice"
            data = {
                "appKey": self._client.app_key,
                "noticeType": notice_type.value,
                "sceneType": scene_type.value,
                "toUserId": to_user_id,
                "payload": payload.model_dump() if hasattr(payload, "model_dump") else payload.dict(),
            }
            headers = {
                "x-userno-place": "body",
                "x-userno-key": "toUserId",
            }
            response = api.get_response(uri, json=data, headers=headers)
            return APIResponse(response).json
