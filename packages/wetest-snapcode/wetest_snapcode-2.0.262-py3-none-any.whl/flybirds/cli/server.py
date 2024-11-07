# -*- coding: utf-8 -*-
"""
process args
"""
import json
import os
import signal
import sys
import time
from copy import copy
from collections import namedtuple, defaultdict
import shutil

from behave.model_core import Status
from flask import Flask, request
import cantools
from flybirds_poco.drivers.android.uiautomation import AndroidUiautomationPoco

from flybirds.core.server import config
from flybirds.core.server.dump import ScenarioState

from flybirds.cli.parse_args import parse_args, default_report_path
from flybirds.core.server.handler import (
    get_script_path,
    do_start_script,
    do_screen_ocr,
    save_current_scenario_to_json,
)
from flybirds.core.server.handler import (
    get_current_app,
    list_apps,
    start_app,
    stop_app,
    clear_app,
)
from flybirds_airtest.core.android.adb import ADB
from flybirds.core.server.client import TestClient, AssistdClient
from flybirds.utils import flybirds_log as log
from flybirds.core.launch_cycle.run_manage import run_script, RunManage
import flybirds.core.global_resource as gr
from flybirds.core.global_context import GlobalContext
from flybirds.utils.feature_helper import SCRIPT_TYPE_OF_FILE, SCRIPT_TYPE_OF_CODE
from flybirds.utils.file_helper import save_to_file_path
from flybirds.utils.http_helper import HttpUdt

app = Flask(__name__)
r_context = {"run_args": None}
r_test_stage = None


@app.route("/ping", methods=["GET"])
def ping():
    return json.dumps({"ret": "pong"}), 200, {"ContentType": "application/json"}


@app.route("/v1/feature/device/init", methods=["POST"])
def init_device():
    data = request.get_json()
    device_id = data.get("device_id")
    poco_device_instance = f"pocoInstance{device_id}"
    poco = gr.get_value(poco_device_instance)
    if poco is not None:
        stop_device()

    if device_id is None:
        matching_elements = [
            item for item in app.config["fb_define"] if "deviceId=" in item
        ]
        for did in matching_elements:
            device_id = did.split("=")[1]
            break
    if device_id is None:
        return (
            json.dumps(
                {
                    "res": "not found device id",
                }
            ),
            200,
            {"ContentType": "application/json"},
        )

    script = data.get(
        "script", f" #language:zh-CN\n功能:flybirds初始化\n场景:初始化\n当 设备初始化[{device_id}]\n"
    )
    init_script_path = get_script_path(SCRIPT_TYPE_OF_CODE, script, device_id)
    r_context = init_context(device_id, init_script_path, None)
    err = do_start_script(r_context)
    log.info(f"end init script with: {err}")
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


def release_poco(device_id):
    log.info("stop driver of device " + str(device_id))
    try:
        GlobalContext.ui_driver.uninit_driver(device_id)
    except:
        pass
    try:
        GlobalContext.device.device_disconnect(device_id)
    except:
        pass


@app.route("/v1/feature/device/stop", methods=["POST"])
def stop_device():
    global r_test_stage
    if r_test_stage == "running":
        gr.set_value("aborted", 1)

    gr.set_value("pause_step", 0)
    while r_test_stage != "stopped":
        time.sleep(1)

    gr.set_value("aborted", 0)
    data = request.get_json()
    device_id = data.get("device_id")
    if device_id is None:
        device_id = gr.get_device_id()

    release_poco(device_id)

    while app.config["fb_report_path"]:
        # report/*
        report_path = app.config["fb_report_path"].pop()
        report_dir_path = report_path[0 : report_path.rfind(os.sep)]
        report_fullpath = os.path.join(os.getcwd(), report_dir_path)
        shutil.rmtree(report_fullpath, ignore_errors=True)

        # *report.json created by behave
        json_path = report_path.replace(os.sep, "")
        json_fullpath = os.path.join(os.getcwd(), json_path)
        if os.path.exists(json_fullpath):
            os.remove(json_fullpath)
    return json.dumps({"ret": "ok"}), 200, {"ContentType": "application/json"}


def reset_test_status():
    resume_step()
    gr.set_test_env({})


@app.route("/v1/feature/start", methods=["POST"])
def start_script():
    data = request.get_json()

    log.info("start feature by data =" + json.dumps(data))

    script_type = data.get("type", SCRIPT_TYPE_OF_FILE)
    debug_id = data.get("script_debug_id")
    script = data.get("script")
    cos_dir = data.get("cos_dir", "car/test/")

    if data.get("env_test_id") is not None:
        config.set_test_id(data.get("env_test_id"))
    if data.get("env_device_id") is not None:
        config.set_device_id(data.get("env_device_id"))
    if data.get("env_script_id") is not None:
        config.set_script_id(data.get("env_script_id"))

    script_path = get_script_path(script_type, script, debug_id)
    device_id = data.get("device_id")

    reset_test_status()

    r_context = init_context(device_id, script_path, cos_dir)
    global r_test_stage
    r_test_stage = "running"
    err = do_start_script(r_context)
    log.info(f"end script with: {err}")
    r_test_stage = "stopped"
    gr.set_value("abort", 0)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/v1/feature/stop", methods=["GET"])
def stop():
    global r_test_stage
    if r_test_stage == "running":
        gr.set_value("aborted", 1)
    gr.set_value("pause_step", 0)

    while r_test_stage != "stopped":
        time.sleep(1)

    gr.set_value("aborted", 0)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


def init_context(device_id, script_path, cos_dir):
    defines = copy(app.config["fb_define"])
    if device_id is not None:
        defines = [item for item in defines if "deviceId=" not in item]
        defines.append("deviceId=" + device_id)

    if cos_dir is not None:
        defines.append("cos_dir=" + cos_dir)

    report_path = default_report_path()
    app.config["fb_report_path"].append(report_path)
    run_args = parse_args(
        script_path,
        app.config["fb_tag"],
        app.config["fb_report_format"],
        report_path,
        defines,
        app.config["fb_rerun"],
        app.config["fb_es"],
        app.config["fb_to_html"],
        app.config["fb_run_at"],
        app.config["fb_processes"],
    )
    r_context["run_args"] = run_args
    return r_context


@app.route("/v1/feature/scenario/current", methods=["GET"])
def get_current_scenario():
    return save_current_scenario_to_json(), 200, {"ContentType": "application/json"}


@app.route("/v1/feature/scenario/reset", methods=["GET"])
def reset_scenario():
    gr.set_value("current_scenario", ScenarioState())
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/v1/feature/step/current", methods=["GET"])
def get_current_step():
    current_scenario = gr.get_value("current_scenario")
    if current_scenario is None:
        return (
            json.dumps(
                {
                    "scenario": "",
                }
            ),
            200,
            {"ContentType": "application/json"},
        )
    return (
        json.dumps(
            {
                "current_scenario": current_scenario.name,
                "current_step": current_scenario.step,
            }
        ),
        200,
        {"ContentType": "application/json"},
    )


@app.route("/v1/feature/step/pause", methods=["GET"])
def pause_step():
    gr.set_value("pause_step", 1)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/v1/feature/step/resume", methods=["GET"])
def resume_step():
    gr.set_value("pause_step", 0)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/v1/feature/screen/ocr", methods=["GET"])
def screen_ocr():
    err, ocr_result = do_screen_ocr()
    if err is None:
        return (
            json.dumps({"ocr_result": ocr_result}),
            200,
            {"ContentType": "application/json"},
        )
    else:
        return (
            json.dumps({f"ocr_failed": f"{err}"}),
            500,
            {"ContentType": "application/json"},
        )


@app.route("/v1/feature/app/current", methods=["GET"])
def current_app():
    return (
        json.dumps(json.dumps({"current_app": get_current_app()})),
        200,
        {"ContentType": "application/json"},
    )


@app.route("/v1/feature/app/list", methods=["GET"])
def list_device_apps():
    return (
        json.dumps(json.dumps({"apps": list_apps()})),
        200,
        {"ContentType": "application/json"},
    )


@app.route("/v1/feature/app/start", methods=["POST"])
def app_start():
    data = request.get_json()
    device_id = data.get("device_id")
    package = data.get("package")
    start_app(package)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/v1/feature/app/stop", methods=["POST"])
def app_stop():
    data = request.get_json()
    device_id = data.get("device_id")
    package = data.get("package")
    stop_app(package)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/v1/feature/app/clear", methods=["POST"])
def app_clear():
    data = request.get_json()
    device_id = data.get("device_id")
    package = data.get("package")
    clear_app(package)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/v1/feature/screen/dump", methods=["GET"])
def screen_dump():
    poco = gr.get_value("pocoInstance")
    if poco is not None:
        return (
            json.dumps({"uitree": poco.agent.hierarchy.dump()}),
            200,
            {"ContentType": "application/json"},
        )
    else:
        return (
            json.dumps({f"uidump": "poco not ready"}),
            500,
            {"ContentType": "application/json"},
        )


@app.route("/v1/feature/dbc/<dbc_name>", methods=["GET"])
def parse_dbc(dbc_name):
    prefix = "/car/candbc/"
    dbc_name = prefix + dbc_name
    dbc_path = HttpUdt.download_file(dbc_name)
    log.info(f"download file to {dbc_path}")
    db = cantools.database.load_file(dbc_path)

    Message = namedtuple(
        "Message", ["name", "frame_id", "frame_id_hex", "type", "signals"]
    )
    Signal = namedtuple(
        "Signal",
        [
            "name",
            "initial",
            "minimum",
            "maximum",
            "scale",
            "offset",
            "start",
            "length",
            "comment",
        ],
    )
    result = {"messages": []}

    for m in db.messages:
        sigs = defaultdict(list)
        for s in m.signals:
            sig = Signal(
                s.name,
                s.initial if s.initial else s.minimum,
                s.minimum,
                s.maximum,
                s.scale,
                s.offset,
                s.start,
                s.length,
                s.comment,
            )
            if s.is_multiplexer:
                continue
            elif s.multiplexer_signal:
                sub_id = s.multiplexer_signal + " = " + str(hex(s.multiplexer_ids[0]))
                sigs[sub_id].append(sig._asdict())
            else:
                sigs[""].append(sig._asdict())

        sigs_format = []
        for k, v in sigs.items():
            sigs_format.append({"id": k, "data": v})
        msg = Message(
            m.name,
            m.frame_id,
            hex(m.frame_id),
            "multi" if m.is_multiplexed() else "noMulti",
            sigs_format,
        )._asdict()
        result["messages"].append(msg)
    return json.dumps(result), 200, {"ContentType": "application/json"}


@app.route("/v1/feature/panel", methods=["GET"])
def screenshot_panel():
    device_id = gr.get_device_id()
    dev = ADB(device_id)

    name = round(time.time())
    remote_path = f"/sdcard/pictures/{name}.png"
    cur_path = os.path.join(os.getcwd(), "download", f"{name}.png")
    os.makedirs(os.path.dirname(cur_path), exist_ok=True)

    screen_cmd = f"shell fission_screencap -d 0 {remote_path}"
    try:
        dev.cmd(screen_cmd)
    except Exception as e:
        return (
            json.dumps({"code": -2, "ret": e}),
            500,
            {"ContentType": "application/json"},
        )
    pull_cmd = f"pull {remote_path} {cur_path}"
    dev.cmd(pull_cmd)
    if not os.access(cur_path, os.R_OK):
        return (
            json.dumps({"code": -2, "ret": f"file not exist: {cur_path}"}),
            500,
            {"ContentType": "application/json"},
        )
    url = HttpUdt.upload_file(cur_path)
    return (
        json.dumps({"code": 0, "ret": url}),
        200,
        {"ContentType": "application/json"},
    )


@app.route("/v1/feature/shutdown", methods=["GET"])
def shutdown_server():
    data = request.get_json()
    device_id = data.get("device_id")
    if device_id is None:
        device_id = gr.get_device_id()
    release_poco(device_id)
    os.kill(os.getpid(), signal.SIGINT)
    return "Server shutting down..."


def run_server(
    server_port,
    feature_path,
    tag,
    report_format,
    report_path,
    define,
    rerun,
    es,
    to_html,
    run_at,
    processes,
):
    log.info(f"run server with run_args: {server_port}")
    app.config["fb_feature_path"] = feature_path
    app.config["fb_tag"] = tag
    app.config["fb_report_format"] = report_format
    app.config["fb_report_path"] = [report_path]
    app.config["fb_define"] = define
    app.config["fb_rerun"] = rerun
    app.config["fb_es"] = es
    app.config["fb_to_html"] = to_html
    app.config["fb_run_at"] = run_at
    app.config["fb_processes"] = processes

    app.run(port=server_port)


def parse_udt_args(udt_args):
    udt_features = ""
    udt_exec_id = ""
    for a in udt_args.split(" "):
        if "files=" in a:
            udt_features = a.split("=")[1]
            continue

        if "exec_id=" in a:
            udt_exec_id = a.split("=")[1]
            continue

    return udt_features, udt_exec_id


def run_test(
    udt_args,
    tag,
    report_format,
    report_path,
    define,
    rerun,
    es,
    to_html,
    run_at,
    processes,
):
    config.dump_config()

    udt_features, udt_exec_id = parse_udt_args(udt_args)

    feature_paths = udt_features.strip().split(",")
    i = 0
    size_of_feature = len(feature_paths)
    test_client = None
    if config.get_local_server_ip():
        test_client = TestClient(
            ip=config.get_local_server_ip(), port=config.get_local_server_port()
        )

    if config.is_desktop_mode():
        host = config.get_assistd_host()
        if host is not None:
            raw_serial = config.get_raw_serial()
            print("get port from assistd", raw_serial, host)
            assist_client = AssistdClient(host)
            assist_client.wait_ready()
            flybirds_port = assist_client.get_port(config.get_raw_serial())
            print("get port from assistd", flybirds_port)
            if flybirds_port > 0:
                test_client = TestClient(port=flybirds_port)

    while i < size_of_feature:
        if config.get_script_dir() is not None:
            f = f"{config.get_script_dir()}/{feature_paths[i]}"
        else:
            f = feature_paths[i]
        (path, filename) = os.path.split(f)
        log.info("============ run for : {}".format(str(f)))
        script_id = filename.split(".")[0]
        config.set_script_id(script_id)

        if sys.platform.startswith("win"):
            f = f.replace("\\", "/")

        scenario_result = ScenarioState()
        if test_client is None:
            run_args = parse_args(
                f,
                tag,
                report_format,
                report_path,
                define,
                rerun,
                es,
                to_html,
                run_at,
                processes,
            )
            log.info("============last run_args: index {}, {}".format(i, str(run_args)))
            r_context = {"run_args": run_args}
            RunManage.load_pkg()
            RunManage.process("before_run_processor", r_context)
            RunManage.exe(r_context)
            RunManage.process("after_run_processor", r_context)
            scenario_result = gr.get_value("current_scenario")
        else:
            if test_client is not None:
                ret = test_client.start_test(
                    f,
                    config.get_test_id(),
                    config.get_device_id(),
                    config.get_script_id(),
                )
                log.info("start_test: res {} {}".format(ret.text, ret.ok))
                ret = test_client.dump()
                log.info("test result dump: res {} {}".format(ret.text, ret.ok))
                if ret.ok:
                    scenario_res = json.loads(test_client.dump().text)
                    scenario_result.current_scenario = scenario_res.get(
                        "current_scenario"
                    )
                    scenario_result.current_step = scenario_res.get("current_step")
                    scenario_result.step_index = scenario_res.get("step_index")
                    scenario_result.step_status = scenario_res.get("step_status")
                    scenario_result.step_process = scenario_res.get("step_process")

        log.info(
            "============dump last result to result_json.xml run_args: {}".format(
                str(scenario_result.to_json())
            )
        )
        save_dir = "udt_result"
        if config.get_result_dir():
            save_dir = config.get_result_dir()
        save_to_file_path(
            str(scenario_result.to_json()),
            f"{save_dir}/scenarios_result/",
            f"{filename}_{i}_result_json.xml",
        )

        # upload to server
        try:
            res = HttpUdt.upload_scenario_result(
                config.get_test_id(),
                config.get_device_id(),
                config.get_script_id(),
                udt_exec_id,
                scenario_result,
            )
            log.info(
                "upload_scenario_result: res {} {} {}".format(
                    parse_udt_args, res.text, res.url
                )
            )
        except Exception as e:
            log.info("upload_scenario_result: failed {}".format(e))

        result_file = f"{save_dir}/scenarios_result/{filename}_{i}_result_json.xml"

        if scenario_result is None or scenario_result.step_status in (
            Status.failed,
            Status.undefined,
        ):
            if os.environ.get("UDT_IGNORE_ERROR") or i < size_of_feature - 1:
                pass
            else:
                raise Exception(
                    f"run script failed by error step_status, details to see: {result_file}"
                )

        i = i + 1


if __name__ == "__main__":
    app.run(port=5000)
