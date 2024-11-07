"""
CAN/PW/DAQ message
"""
import json
import random
import string
import socket

import flybirds.core.global_resource as gr
import flybirds.utils.flybirds_log as log
import flybirds.utils.dsl_helper as dsl_helper
from flybirds.core.exceptions import FlybirdsException


class CarProtocol:
    # CAN Message
    __can_set = {
        "op": "CAN.dbc.set",
        "reqid": str(random.randint(1, 10**9)),
        "data": {
            "sn": "".join(random.sample(string.ascii_letters + string.digits, 8)),
            "speed": 1,
            "mode": 1,
            "period": 100,
            "times": 1,
            "message": {
                "name": "".join(random.sample(string.ascii_letters, 4)),
                "id": random.randint(1, 10**3),
                "signals": [
                    {
                        "name": "".join(random.sample(string.ascii_letters, 4)),
                        "value": random.randint(1, 10**2),
                        "send": True,
                    }
                ],
            },
        },
    }

    __can_get = {
        "op": "CAN.dbc.get",
        "reqid": str(random.randint(1, 10**9)),
        "data": {
            "sn": "".join(random.sample(string.ascii_letters + string.digits, 8)),
            "message": {
                "name": "".join(random.sample(string.ascii_letters, 4)),
                "id": random.randint(1, 10**3),
                "signals": [
                    {
                        "name": "".join(random.sample(string.ascii_letters, 4)),
                        "get": True,
                    }
                ],
            },
        },
    }

    __can_stop = {
        "op": "CAN.dbc.stop",
        "reqid": str(random.randint(1, 10**9)),
        "data": {
            "sn": "".join(random.sample(string.ascii_letters + string.digits, 8)),
            "message": {
                "name": "".join(random.sample(string.ascii_letters, 4)),
                "id": random.randint(1, 10**3),
                "sub_id": [],
            },
        },
    }

    __can = {"set": __can_set, "get": __can_get, "stop": __can_stop}

    # PW Message
    __pw_write = {
        "op": "PW.cmd.write",
        "reqid": str(random.randint(1, 10**9)),
        "data": {
            "sn": "".join(random.sample(string.ascii_letters + string.digits, 8)),
            "cmd": "CURR",
            "value": "1",
        },
    }

    __pw_read = {
        "op": "PW.cmd.read",
        "reqid": str(random.randint(1, 10**9)),
        "data": {
            "sn": "".join(random.sample(string.ascii_letters + string.digits, 8)),
            "cmd": "CURR",
        },
    }

    __pw = {"write": __pw_write, "read": __pw_read}

    # DAQ Message
    __daq = {
        "op": "DAQ.cmd.get",
        "reqid": str(random.randint(1, 10**9)),
        "data": {
            "sn ": "".join(random.sample(string.ascii_letters + string.digits, 8)),
            "chsname": "左喇叭检测",
            "channel": "AI0",
        },
    }

    @classmethod
    def __parse_key(cls, key):
        param_dict = dsl_helper.params_to_dic(key)
        sel = param_dict["selector"]
        if "=" in sel:
            k, v = sel.split("=")
            param_dict[k] = v
        cls.__mock = eval(param_dict.get("mock", "False"))
        return param_dict

    @classmethod
    def control_can(cls, key, tag):
        param_dict = cls.__parse_key(key)

        if not cls.__mock:
            frame = cls.__can[tag]["data"]
            frame["sn"] = gr.get_device_id()
            if mode := param_dict.get("mode"):
                mode = int(mode)
                frame["mode"] = mode
                if mode == 1:
                    frame.update(
                        zip(
                            ["speed", "period", "times"],
                            [
                                int(param_dict["speed"]),
                                int(param_dict["period"]),
                                int(param_dict["times"]),
                            ],
                        )
                    )

            message = frame["message"]
            message.update(
                zip(["name", "id"], [param_dict["msg_name"], int(param_dict["id"])])
            )
            if sub_id := param_dict.get("sub_id"):
                message.update({"sub_id": sub_id})

            if signals := message.get("signals"):
                signals.clear()
                sig_names = param_dict.get("sig_name")
                sig_names = [sig.strip("[ ]") for sig in sig_names.split(",")]
                if values := param_dict.get("value"):
                    values = [val.strip("[ ]") for val in values.split(",")]
                    for name, value in zip(sig_names, values):
                        signals.append(
                            dict(
                                zip(["name", "value", "send"], [name, int(value), True])
                            )
                        )
                else:
                    for name in sig_names:
                        signals.append(dict(zip(["name", "get"], [name, True])))

        req = cls.__can[tag]
        cls.__response(req)

    @classmethod
    def control_pw(cls, key, tag):
        param_dict = cls.__parse_key(key)

        if not cls.__mock:
            frame = cls.__pw[tag]["data"]
            frame["sn"] = gr.get_device_id()
            cmd = param_dict["cmd"]
            if cmd not in ("CURR", "VOLT", "POWer", "OUTPut"):
                raise FlybirdsException(
                    f"{cmd} is illegal, please input CURR, VOLT, POWer or OUTPut!"
                )
            frame["cmd"] = param_dict["cmd"]
            frame["value"] = param_dict.get("value")

        req = cls.__pw[tag]
        cls.__response(req)

    @classmethod
    def control_daq(cls, key):
        param_dict = cls.__parse_key(key)

        if not cls.__mock:
            frame = cls.__daq["data"]
            frame["sn"] = gr.get_device_id()
            frame["chsname"] = param_dict["chsname"]
            frame["channel"] = param_dict.get("channel")

        req = cls.__daq
        cls.__response(req)

    @classmethod
    def __response(cls, req):
        log.info(f"request: {req}")
        req_json = json.dumps(req)
        rsp_json = (
            cls.__mock_server(req_json) if cls.__mock else cls.__car_server(req_json)
        )
        rsp = json.loads(rsp_json)
        log.info(f"response: {rsp}")

        if rsp["code"] == 0:
            gr.set_value("log_capture", rsp["data"])
        else:
            gr.set_value("log_capture", rsp["msg"])
            raise FlybirdsException(rsp["msg"])

    def __car_server(req_json):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip_port = ("127.0.0.1", 9001)
        client.connect(ip_port)
        log.info(f"{client} connected!")
        log.info(req_json)
        client.sendall(req_json.encode())
        client.settimeout(5)
        rsp_json = client.recv(1024).decode()
        return rsp_json

    def __mock_server(req_json):
        req = json.loads(req_json)
        rsp = {}
        rsp["op"] = req["op"]
        rsp["reqid"] = req["reqid"]
        rsp["data"] = req["data"]
        rsp["code"] = 0
        rsp["msg"] = "ok"
        rsp_json = json.dumps(rsp)
        return rsp_json
