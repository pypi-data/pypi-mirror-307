# -*- coding: utf-8 -*-
"""
process args
"""
import json
import os

from flybirds.core.launch_cycle.run_manage import RunManage
import flybirds.core.global_resource as gr
from flybirds.utils import flybirds_log as log, file_helper
from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.utils import feature_helper
from flybirds.utils.feature_helper import SCRIPT_TYPE_OF_FILE


def get_script_path(script_type, script, debug_id):
    if script_type != SCRIPT_TYPE_OF_FILE:
        init_script_path = "features/test/"
        file_helper.create_dirs(init_script_path)
        script_path = feature_helper.store_feature_to_file_path(
            script,
            script_type,
            debug_id,
            init_script_path)
    else:
        script_path = script
    return script_path


def do_start_script(r_context):
    RunManage.load_pkg()
    RunManage.process("before_run_processor", r_context)
    err = RunManage.exe(r_context)
    RunManage.process("after_run_processor", r_context)
    return err


def do_screen_ocr():
    screen_path = os.path.join(gr.get_screen_save_dir(), "ocr.png")
    g_Context.screen.screen_shot(screen_path)

    if os.path.exists(screen_path):
        log.info(f"screenshot an save in : {screen_path}")
        ocr_result = g_Context.ocr_driver_instance.ocr(screen_path, det=True)
        return None, ocr_result
    else:
        return "screenshot failed", None


def do_ui_driver():
    screen_path = os.path.join(gr.get_screen_save_dir(), "ocr.png")
    g_Context.screen.screen_shot(screen_path)
    if os.path.exists(screen_path):
        log.info(f"screenshot an save in : {screen_path}")
        ocr_result = g_Context.ocr_driver_instance.ocr(screen_path, det=True)
        return None, ocr_result
    else:
        return "screenshot failed", None


def get_current_app():
    app = g_Context.app.current_app()
    if "/" in app:
        package = app.split("/")[0]
    else:
        package = app
    return package


def save_current_scenario_to_json():
    current_scenario = gr.get_value("current_scenario")
    if current_scenario is None:
        return json.dumps({
            'scenario': "",
        }, ensure_ascii=False)
    return current_scenario.to_json()


def list_apps():
    return g_Context.app.list_apps()


def start_app(package):
    g_Context.app.wake_app(package, 6)


def stop_app(package):
    g_Context.app.shut_app(package)


def clear_app(package):
    g_Context.app.clear_app(package)
