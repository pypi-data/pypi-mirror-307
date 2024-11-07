# -*- coding: utf-8 -*-
"""
report scenario state to remote
"""
import json
import time

import requests


# http://127.0.0.1:7617/v2/editor/report/UploadTestResult

class ReportClient:
    def __init__(self, ip="127.0.0.1", port=7617):
        self.ip = ip
        self.port = port
        self.url = "http://%s:%s" % (ip, port)

    def upload_scenario_result(self, test_id, device_id, script_id, exec_id, scenario):
        data = {
            "test_id": test_id,
            "device_id": int(device_id),
            "script_id": int(script_id),
            "status": str(scenario.step_status),
            "last_index": int(scenario.step_index),
            "process": str(json.dumps(scenario.step_process, default=lambda o: o.__dict__, indent=4)),
            "scenario": str(scenario.current_scenario),
            "ts": int(round(time.time() * 1000)),
            "exec_id": exec_id,
        }
        return requests.post(self.url + "/v2/editor/report/UploadTestResult", json=data, timeout=30)
