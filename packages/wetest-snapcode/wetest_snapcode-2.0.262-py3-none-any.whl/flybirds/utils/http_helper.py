# -*- coding: utf-8 -*-
"""
http help
"""
import json
import time
import requests
import os
from urllib.parse import urlparse


def http_get(url, param=None, header=None):
    if url is not None and url != "":
        result = requests.get(
            url,
            params=param,
            headers=header,
        )
        j_obj = result.json()
        result.close()
        return j_obj
    else:
        return None


class HttpUdt:
    __id = os.environ.get("TEST_ID")
    __key = os.environ.get("TEST_SECRET")
    __auth = (__id, __key)
    __prefix = os.environ.get("REPORT_URL", "")
    __host = urlparse(__prefix).hostname
    __timeout = 5
    __headers = {"Host": __host}
    __payload = {
        "auth": __auth,
        "headers": __headers,
        "timeout": __timeout,
    }
    if os.environ.get("UDT_CAR_NO_TEST"):
        __api_version = "/v1/device-report"
    else:
        __api_version = "/v1/test-report"
    __request_url = __prefix + __api_version

    def _parse_response(resp):
        return resp.json()["data"]

    @classmethod
    def ai_popup(cls, img_path):
        part_url = "/ai/api/popCheck"
        files = {
            "file": (
                os.path.basename(img_path),
                open(img_path, "rb"),
                "image/jpeg",
            ),
        }
        params = {"project": cls.__id}
        response = requests.post(
            cls.__request_url + part_url, params=params, files=files, **cls.__payload
        )
        response.raise_for_status()
        return cls._parse_response(response)

    @classmethod
    def popup_text(cls):
        part_url = "/ai/api/popButtonText"
        params = {"project": cls.__id}
        response = requests.get(
            cls.__request_url + part_url, params=params, **cls.__payload
        )
        response.raise_for_status()
        return cls._parse_response(response)

    @classmethod
    def download_file(cls, file_path):
        part_url = "/editor/common/GetFilePath"
        params = {"project": cls.__id, "name": file_path}
        response = requests.get(
            cls.__request_url + part_url, params=params, **cls.__payload
        )
        response.raise_for_status()
        download_url = cls._parse_response(response)["data"]

        file = requests.get(download_url)
        file_path = file_path.strip("/")
        download_path = os.path.join(os.getcwd(), "download", file_path)
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        with open((download_path), "wb") as f:
            f.write(file.content)
        return download_path

    @classmethod
    def upload_file(cls, file_path):
        part_url = "/editor/common/UploadFilesToCloud"
        file_name = "/report/" + os.path.basename(file_path)
        params = {"project": cls.__id, "name": file_name}
        files = {"file": (file_name, open(file_path, "rb"), "image/jpeg")}
        response = requests.post(
            cls.__request_url + part_url, params=params, files=files, **cls.__payload
        )
        response.raise_for_status()
        return cls._parse_response(response)["data"]

    @classmethod
    def upload_scenario_result(cls, test_id, device_id, script_id, exec_id, scenario):
        # only used in test mode
        part_url = "/v1/test-report/editor/report/UploadTestResult"
        params = {"project": cls.__id}
        data = {
            "test_id": test_id,
            "device_id": int(device_id),
            "script_id": int(script_id),
            "status": str(scenario.step_status),
            "last_index": int(scenario.step_index),
            "process": str(
                json.dumps(
                    scenario.step_process, default=lambda o: o.__dict__, indent=4
                )
            ),
            "scenario": str(scenario.current_scenario),
            "ts": int(round(time.time() * 1000)),
            "exec_id": exec_id,
        }
        return requests.post(
            cls.__prefix + part_url, params=params, json=data, **cls.__payload
        )

    @classmethod
    def icon_detect(cls, img_path, icon_name):
        part_url = "/ai/api/icon_detect"
        files = {
            "file": (
                os.path.basename(img_path),
                open(img_path, "rb"),
                "image/jpeg",
            ),
        }
        params = {"name": icon_name}
        response = requests.post(
            cls.__request_url + part_url, params=params, files=files, **cls.__payload
        )
        response.raise_for_status()
        return response.json()
