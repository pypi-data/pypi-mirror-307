# -*- coding: utf-8 -*-
"""
report scenario state to remote
"""
import json
import os
import time

import requests


class TestClient:
    def __init__(self, ip="127.0.0.1", port=5001):
        self.ip = ip
        self.port = port
        self.url = "http://%s:%s" % (ip, port)

    def wait_ready(self, retry=10):
        i = 0
        while i < retry:
            try:
                if requests.get(self.url + "/ping", timeout=3).ok:
                    return True
            except:
                pass
            i = i + 1
            time.sleep(1)

        return False

    def init_device(self, device_id):
        data = {
            "device_id": device_id,
        }
        return requests.post(self.url + "/v1/feature/device/init", json=data, timeout=60)

    def uninit_device(self, device_id):
        data = {
            "device_id": device_id,
        }
        return requests.post(self.url + "/v1/feature/device/stop", json=data, timeout=60)

    def start_test(self, f, test_id, device_id, script_debug_id):
        data = {
            "env_test_id": str(test_id),
            "env_device_id": str(device_id),
            "env_script_id": str(script_debug_id),
            "script": f,
            "type": "file",
        }
        return requests.post(self.url + "/v1/feature/start", json=data)

    def dump(self):
        return requests.get(self.url + "/v1/feature/scenario/current", timeout=30)


class AssistdClient:
    def __init__(self, host):
        self.url = host

    def wait_ready(self, retry=10):
        i = 0
        while i < retry:
            try:
                if requests.get(self.url + "/v1/heartbeat", timeout=3).ok:
                    return True
            except:
                pass
            i = i + 1
            time.sleep(1)

        return False

    def get_port(self, device_id):
        params = {
            "serial": device_id
        }
        resp = requests.get(self.url + "/v1/car/port", params=params, timeout=10)
        data = resp.json()
        if resp.status_code == 200 and data["ret"] == 0:
            port = data["data"]["port"]
            return port
        return 5001
