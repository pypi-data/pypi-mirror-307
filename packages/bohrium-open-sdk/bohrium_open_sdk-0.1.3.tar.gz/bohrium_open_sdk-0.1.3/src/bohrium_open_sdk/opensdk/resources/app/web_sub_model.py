import logging
import os.path
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Union
from urllib.parse import urlparse

from bohrium_open_sdk.opensdk._base_client import APIResponseManager
from bohrium_open_sdk.opensdk._resource import SyncAPIResource
from bohrium_open_sdk.opensdk._response import APIErrorResponse, APIResponse
from bohrium_open_sdk.opensdk._tiefblue_client import Tiefblue
from bohrium_open_sdk.opensdk._types import JobInputType, UploadInputItem
from bohrium_open_sdk.opensdk.resources.user.user import User

logger = logging.getLogger(__name__)


class WebSubModel(SyncAPIResource):

    user: User

    def __init__(self, _client) -> None:
        self._client = _client
        self.user = User(_client)
        self._tiefblue_client = Tiefblue(base_url=_client.tiefblue_base_url)

    def detail(self, job_id: int):
        with APIResponseManager(self._client.get) as api:
            uri = f"{self._client.api_prefix}/v1/app/job/app/detail/{job_id}"
            response = api.get_response(uri)
            return APIResponse(response).json

    def kill(self, job_id: int):
        with APIResponseManager(self._client.post) as api:
            uri = f"{self._client.api_prefix}/v1/app/job/app/kill/{job_id}"
            response = api.get_response(uri)
            return APIResponse(response).json

    def delete(self, job_id: int):
        with APIResponseManager(self._client.post) as api:
            uri = f"{self._client.api_prefix}/v1/app/job/app/del/{job_id}"
            response = api.get_response(uri)
            return APIResponse(response).json

    def list(
        self, *, page: int = 1, query_type: str = "all", page_size: int = 20, **kwargs
    ):
        # get user info
        user_info = self.user.get_info()

        if user_info["code"] != 0:
            return APIErrorResponse("get user info failed", int(user_info["code"]))
        with APIResponseManager(self._client.get) as api:
            uri = f"{self._client.api_prefix}/v1/app/job/app/list"
            params = {
                "page": page,
                "queryType": query_type,
                "pageSize": page_size,
                "submitUserId": user_info["data"]["user_id"],
            }
            params.update(kwargs or {})

            response = api.get_response(uri, params=params)
            return APIResponse(response).json

    def log(self, job_id: int):
        with APIResponseManager(self._client.get) as api:
            uri = f"{self._client.api_prefix}/v1/app/job/app/{job_id}/log?logFile=./STDOUTERR"
            logger.debug(f"request_uri:{uri}")
            response = api.get_response(uri)
            return APIResponse(response).json

    def submit(
        self,
        *,
        app_key: str,
        sub_model_name: str,
        cmd: str,
        project_id: Optional[int] = 0,
        machine_type: Optional[str] = None,
        sku_id: Optional[int] = 0,
        upload_files: Optional[List[UploadInputItem]] = None,
        source_app_key: Optional[str] = None,
    ):
        app_schema = self.get_app_schema(app_key)

        sub_model_list_data = self._get_sub_model_by_app_key(app_key)

        if sub_model_list_data["code"] != 0:
            return APIErrorResponse(
                "get sub model list failed", int(sub_model_list_data["code"])
            )

        sub_model_list = sub_model_list_data["data"]

        found = False
        for item in sub_model_list:
            if item["submodelName"] == sub_model_name:
                sub_model_info = item
                found = True
                break

        if not found:
            logger.error(f"sub_model_name:{sub_model_name} not found")
            return APIErrorResponse(f"sub_model_name:{sub_model_name} not found", 404)

        inputs = {}
        ext_config = {}
        if machine_type:
            inputs["__SYSTEM_SUBMIT_BOHRIUM_MACHINE_TYPE__"] = machine_type

        ext_config["inputs"] = inputs

        if sku_id is None or sku_id == 0:
            # machine_type not define
            if machine_type is None or machine_type == "":
                sku_id = sub_model_info["skuId"]

        if project_id == 0:
            project_id = self._client.project_id

        return self._submit_task(
            app_key,
            sub_model_name,
            app_schema,
            cmd=cmd,
            project_id=project_id,
            deployment_id=sub_model_info["deploymentId"],
            sku_id=sku_id,
            upload_files=upload_files,
            ext_config=ext_config,
            source_app_key=source_app_key,
        )

    def _submit_task(
        self,
        app_key,
        sub_model_name,
        app_schema,
        cmd: str,
        project_id: int,
        deployment_id: str,
        sku_id: int,
        upload_files: Optional[List[UploadInputItem]] = None,
        ext_config: Optional[Dict[str, JobInputType]] = None,
        source_app_key: Optional[str] = None,
    ):
        create_resp = self._create(app_key, deployment_id, source_app_key)
        logger.debug(
            f"create_resp:app_key{app_schema.appKey}, "
            f"sub_model_name:{sub_model_name}, "
            f"deployment_id:{deployment_id}, "
            f"job_id:{create_resp.jobId}, "
            f"upload_path:{create_resp.uploadPath}"
            f"project_id:{project_id}, "
            f"source_app_key: {source_app_key}"
        )

        job_id, upload_path = (
            create_resp.jobId,
            create_resp.uploadPath,
        )

        if upload_files is not None:
            # method _upload will patch upload_files with input_path
            upload_files = self._upload(upload_files, job_id, upload_path)
            logging.debug(
                f"upload_files success:app_key:{app_schema.appKey}, upload_file:{upload_files},upload_path:{upload_path}"
            )

        return self._commit(
            app_key,
            job_id,
            cmd,
            sub_model_name,
            project_id,
            sku_id=sku_id,
            ext_config=ext_config,
        )

    def _commit(
        self,
        app_key: str,
        job_id: str,
        cmd: str,
        sub_model_name: str,
        project_id: int,
        sku_id: Optional[int] = None,
        ext_config: Dict[str, JobInputType] = None,
    ):

        with APIResponseManager(self._client.post) as api:
            uri = f"{self._client.api_prefix}/v1/app/job/app/commit"
            # sub_model_name is not necessary
            if sub_model_name is not None and sub_model_name != "":
                ext_config["subModelName"] = sub_model_name

            uuid_str = uuid.uuid4().hex
            suffix = uuid_str[-12:]

            ext_config["name"] = f"job-{app_key}-{sub_model_name}-{suffix}"
            ext_config["projectId"] = project_id
            ext_config["skuId"] = sku_id
            ext_config["jobId"] = job_id
            ext_config["submodelParam"] = {"cmd": cmd}

            logging.debug(f"request_uri:{uri}, body:{ext_config}")
            response = api.get_response(uri, json=ext_config)
            return APIResponse(response).json

    def _upload(
        self, upload_files: List[UploadInputItem], job_id: int, upload_path: str
    ):
        for index, item in enumerate(upload_files):
            upload_files[index] = self.__upload(item, job_id, upload_path)
        return upload_files

    def __upload(self, file_item: UploadInputItem, job_id: int, upload_path: str):
        filename = os.path.basename(file_item.src)
        token_resp = self._gen_upload_token(
            job_id=job_id,
            upload_path=upload_path,
            filename=filename,
        )

        token = token_resp["Authorization"]
        work_path = Path(token_resp["workPath"])
        input_path = self._gen_upload_path(upload_path, filename)

        # patch input_path to upload_files
        file_item.input_path = input_path
        # object_key = f"{work_path}/{input_path}"
        object_key = work_path / input_path

        custom_headers = {"Authorization": token}

        self._tiefblue_client.upload_from_file_multi_part(
            object_key=object_key,
            file_path=str(file_item.src),
            progress_bar=True,
            custom_headers=custom_headers,
        )
        return file_item

    def _gen_upload_token(self, job_id: str, upload_path: str, filename: str):
        url = f"/{self._client.api_prefix}/v1/app/job/app/upload/token"
        params = {}
        params["jobId"] = job_id
        params["path"] = self._gen_upload_path(upload_path, filename)

        response = self._client.get(url, params=params)
        return APIResponse(response).data

    def _gen_upload_path(self, upload_path: str, filename: str):
        return f"{upload_path}/{filename}"

    def _create(self, app_key: str, deployment_id: str, source_app_key: Optional[str] = None):
        uri = f"/{self._client.api_prefix}/v1/app/job/app/create"
        data = {
            "appKey": app_key,
            "deploymentId": deployment_id,
        }
        if source_app_key:
            data["sourceAppKey"] = source_app_key
        response = self._client.post(uri, json=data)
        return APIResponse(response).data

    def download(
        self,
        job_id: int,
        remote_target: str,
        save_path: Union[str, Path],
    ):
        remote_target = Path(remote_target)
        save_path = Path(save_path)
        return self._download(job_id, remote_target, save_path)

    def _download(self, job_id: int, remote_target: Path, save_path: Path):
        import json

        detail = self._detail(job_id)

        if not detail:
            logger.error(
                f"cannot download files, get job detail failed, job_id: {job_id}"
            )
            return False

        logger.debug(json.dumps(detail, indent=4))

        # "prefix": "launching/app/uni-dock/deployment/303/record/16673/job/",
        if not hasattr(detail, "workPath") or not hasattr(detail, "id"):
            logger.error(
                f"cannot download files, job detail not a valid object, job_id: {job_id}"
            )
            return False
        prefix = str(Path(detail.workPath) / remote_target)
        data = {
            "prefix": prefix,
            "maxObjects": 1000,
            "pathKey": detail.id,
            "pathType": "appJob",
        }
        resp = self.iterate(data)

        if not resp:
            logger.error(
                f"cannot download files, iterate files failed, job_id: {job_id}"
            )
            return False

        logger.debug(json.dumps(resp, indent=4))
        prefix_placeholder = resp.get("prefix") or prefix
        path_list, extract_err = self.extract_paths(job_id, resp)
        if len(path_list) == 0:
            logger.error(f"no file found, job_id: {job_id}")
            return False
        if extract_err:
            logger.error(str(extract_err))
            return False

        logger.debug(path_list)

        # {"fileName":".record","uploadPathList":["launching/app/humanb/deployment/659/record/9777/job/outputs/.record"],"pathKey":9762,"pathType":"appJob","uploadPathType":2}
        for path in path_list:
            data = self._multi_download(job_id, path)
            if not data:
                logger.error(f"Failed to download file, path: {path}")
                return False
            download_url = data.get("directUrl")
            if not download_url:
                logger.error(
                    f"Failed to download file, directUrl not found, path: {path}"
                )
                return False
            path_from_prefix = path.replace(prefix_placeholder, "")
            parsed_url = urlparse(download_url)
            parsed_path: str = parsed_url.path
            download_url_without_query = (
                f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_path}"
            )
            local_filename = save_path / (
                path_from_prefix or parsed_path.split("/")[-1]
            ).lstrip("/")

            if not local_filename.parent.exists():
                local_filename.parent.mkdir(parents=True)

            logger.debug(
                f"Downloading {download_url_without_query} to {local_filename}"
            )
            if not self.download_file(download_url, local_filename):
                logger.error(
                    f"Failed to download file, path: {path}, url: {download_url_without_query}"
                )
                return False

        return True

    def extract_paths(self, job_id: int, data: dict):
        paths = []
        if not data:
            return (paths, Exception("Failed to extract paths, data is empty"))
        for obj in data.get("objects", []):
            current_path = obj.get("path")
            if not obj.get("isDir"):
                paths.append(current_path)
            else:
                # Assuming call_api is a function that calls the API with the next directory path
                # and returns the JSON response.
                data = {
                    "prefix": current_path,
                    "maxObjects": 1000,
                    "pathKey": job_id,
                    "pathType": "appJob",
                }

                response = self.iterate(data)
                if response:
                    tmp_list, err = self.extract_paths(job_id, response)
                    if err:
                        return ([], err)
                    paths.extend(tmp_list)
                else:
                    err = f"Failed to extract paths, iterate files failed, path: {obj.get('path')}"
                    logger.error(err)
                    return ([], Exception(err))
        return (paths, None)

    def iterate(self, data):
        with APIResponseManager(self._client.post) as api:
            uri = f"/{self._client.api_prefix}/v2/file/iterate"
            response = api.get_response(uri, json=data)
            return APIResponse(response).data

    def download_file(self, url: str, local_filename: Path) -> bool:
        import requests

        response = requests.get(url, stream=True)

        if response.status_code == 200:
            total_length = response.headers.get("Content-Length")
            if total_length:
                total_length = int(total_length)
            if not total_length:
                local_filename.touch(exist_ok=True)
            else:
                with local_filename.open("ab") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        chunk and f.write(chunk)
            logger.debug(f"Downloaded {local_filename} successfully")
            return True
        else:
            logger.error(
                f"Failed to download file, error message({response.status_code}): {response.text}"
            )
            return False

    def _multi_download(self, job_id, path):
        with APIResponseManager(self._client.post) as api:
            data = {
                "fileName": path,
                "uploadPathList": [path],
                "pathKey": job_id,
                "pathType": "appJob",
                "uploadPathType": 2,
            }
            uri = f"/{self._client.api_prefix}/v1/file/job/app/multi_download"
            response = api.get_response(uri, json=data)
            return APIResponse(response).data

    def _get_sub_model_by_app_key(self, app_key: str):
        with APIResponseManager(self._client.get) as api:
            uri = f"{self._client.api_prefix}/v1/square/app/submodel/list?appKey={app_key}"
            response = api.get_response(uri)
            return APIResponse(response).json

    def get_app_schema(self, app_key: str):
        uri = f"/{self._client.api_prefix}/v1/square/app/exist"
        response = self._client.get(uri, params={"appKey": app_key})
        return APIResponse(response).data

    def _detail(self, job_id: int):
        with APIResponseManager(self._client.get) as api:
            uri = f"{self._client.api_prefix}/v1/app/job/app/detail/{job_id}"
            response = api.get_response(uri)
            return APIResponse(response).data
