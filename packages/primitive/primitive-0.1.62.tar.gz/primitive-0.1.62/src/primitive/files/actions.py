import hashlib
import sys
import threading
from pathlib import Path
from typing import Dict, Optional

import requests
from gql import gql
from loguru import logger

from primitive.graphql.sdk import create_requests_session
from primitive.utils.actions import BaseAction

from ..utils.auth import guard
from .graphql.mutations import (
    file_update_mutation,
    pending_file_create_mutation,
)


# this class can be used in multithreaded S3 client uploader
# this requires getting an S3 access token to this machine however
# we are using presigned urls instead at this time Oct 29th, 2024
class ProgressPercentage(object):
    def __init__(self, filepath: Path) -> None:
        self._filename = filepath.name
        self._size = float(filepath.stat().st_size)
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)"
                % (self._filename, self._seen_so_far, self._size, percentage)
            )
            sys.stdout.flush()


class Files(BaseAction):
    def _pending_file_create(
        self,
        file_name: str,
        file_size: int,
        file_checksum: str,
        file_path: str,
        key_prefix: str,
        is_public: bool = False,
    ):
        mutation = gql(pending_file_create_mutation)
        input = {
            "filePath": file_path,
            "fileName": file_name,
            "fileSize": file_size,
            "fileChecksum": file_checksum,
            "keyPrefix": key_prefix,
            "isPublic": is_public,
        }
        variables = {"input": input}
        result = self.primitive.session.execute(
            mutation, variable_values=variables, get_execution_result=True
        )
        return result.data.get("pendingFileCreate")

    def _update_file_status(
        self,
        file_id: str,
        is_uploading: Optional[bool] = None,
        is_complete: Optional[bool] = None,
    ):
        mutation = gql(file_update_mutation)
        input: Dict[str, str | bool] = {
            "id": file_id,
        }
        if is_uploading is not None:
            input["isUploading"] = is_uploading
        if is_complete is not None:
            input["isComplete"] = is_complete

        variables = {"input": input}
        result = self.primitive.session.execute(
            mutation, variable_values=variables, get_execution_result=True
        )
        return result

    @guard
    def upload_file_direct(
        self,
        path: Path,
        is_public: False,
        key_prefix: str = "",
        file_id: Optional[str] = None,
    ):
        logger.enable("primitive")
        if path.exists() is False:
            raise Exception(f"File {path} does not exist.")

        file_size = path.stat().st_size
        if file_size == 0:
            raise Exception(f"{path} is empty.")

        file_checksum = hashlib.md5(path.read_bytes()).hexdigest()

        if not file_id:
            pending_file_create = self._pending_file_create(
                file_name=path.name,
                file_size=path.stat().st_size,
                file_checksum=file_checksum,
                file_path=str(path),
                key_prefix=key_prefix,
                is_public=is_public,
            )
        file_id = pending_file_create.get("id")
        presigned_url = pending_file_create.get("presignedUrlForUpload")

        if not file_id:
            raise Exception("No file_id found or provided.")
        if not presigned_url:
            raise Exception("No presigned_url returned.")

        self._update_file_status(file_id, is_uploading=True)
        with open(path, "rb") as object_file:
            object_text = object_file.read()
            response = requests.put(presigned_url, data=object_text)
            if response.ok:
                logger.info(f"File {path} uploaded successfully.")
                update_file_status_result = self._update_file_status(
                    file_id, is_uploading=False, is_complete=True
                )
            else:
                message = f"Failed to upload file {path}. {response.status_code}: {response.text}"
                logger.error(message)
                raise Exception(message)
        file_pk = update_file_status_result.data.get("fileUpdate").get("pk")
        file_access_url = f"{self.primitive.host_config.get("transport")}://{self.primitive.host}/files/{file_pk}/presigned-url/"
        logger.info(f"Available at: {file_access_url}")
        return update_file_status_result

    @guard
    def upload_file_via_api(
        self,
        path: Path,
        is_public: bool = False,
        key_prefix: str = "",
        job_run_id: str = "",
    ):
        """
        This method uploads a file via the Primitive API.
        This does NOT upload the file straight to S3
        """
        file_path = str(path.resolve())
        if path.exists() is False:
            raise FileNotFoundError(f"File not found at {file_path}")

        if is_public:
            operations = (
                """{ "query": "mutation fileUpload($input: FileUploadInput!) { fileUpload(input: $input) { ... on File { id } } }", "variables": { "input": { "fileObject": null, "isPublic": true, "filePath": \""""
                + file_path
                + """\", "keyPrefix": \""""
                + key_prefix
                + """\", "jobRunId": \""""
                + job_run_id
                + """\" } } }"""
            )  # noqa

        else:
            operations = (
                """{ "query": "mutation fileUpload($input: FileUploadInput!) { fileUpload(input: $input) { ... on File { id } } }", "variables": { "input": { "fileObject": null, "isPublic": false, "filePath": \""""
                + file_path
                + """\", "keyPrefix": \""""
                + key_prefix
                + """\", "jobRunId": \""""
                + job_run_id
                + """\" } } }"""
            )  # noqa
        body = {
            "operations": ("", operations),
            "map": ("", '{"fileObject": ["variables.input.fileObject"]}'),
            "fileObject": (path.name, open(path, "rb")),
        }

        session = create_requests_session(self.primitive.host_config)
        transport = self.primitive.host_config.get("transport")
        url = f"{transport}://{self.primitive.host}/"
        response = session.post(url, files=body)
        return response
