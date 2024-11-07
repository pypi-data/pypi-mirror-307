# -*- coding: utf-8 -*-
"""
app step implement
"""
import os

import flybirds.core.global_resource as gr
import flybirds.core.plugin.plugins.default.ui_driver.poco.poco_ele as poco_ele
import flybirds.utils.flybirds_log as log
from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.utils import file_helper, download_helper


def init_device(context, param=None):
    device_id = param
    gr.set_value("deviceid", device_id)

    connect_device(context, device_id)
    set_cur_device(context, device_id)
    log.info("poco initial complete")


def connect_device(context, param):
    dev = g_Context.device.device_connect(param)
    poco = gr.get_value(f"pocoInstance{param}")
    if poco is None:
        poco = g_Context.element.ui_driver_init(dev)
        print("init device pocoInstance", poco)
        gr.set_value(f"pocoInstance{param}", poco)


def set_cur_device(context, param):
    g_Context.device.set_cur_device(param)
    poco = gr.get_value(f"pocoInstance{param}")
    print("set cur pocoInstance", poco)
    gr.set_value("pocoInstance", poco)
    context.poco_instance = poco
    g_Context.ui_driver_instance = poco


def install_app(context, param):
    package_path = param
    if file_helper.is_web_url(package_path):
        package_path = download_app(package_path)

    g_Context.app.install_app(package_path)


def download_app(param):
    base_path = os.path.join(os.getcwd(), "download")
    file_helper.create_dirs(base_path)
    d_apk_path = os.path.join(os.getcwd(), "download", "tmp_install.apk")
    download_helper.downlaod(param, d_apk_path)
    return d_apk_path


def uninstall_app(context, param):
    g_Context.app.uninstall_app(param)


def start_app(context, param):
    g_Context.app.wake_app(param, 10)
    gr.set_value("packageName", param)
    # Modal box error detection
    # poco_ele.detect_error()


def clear_app(context, param):
    g_Context.app.clear_app(param)


def restart_app(context, package_name):
    if not package_name:
        package_name = gr.get_app_package_name()
    g_Context.app.shut_app(package_name)
    wait_time = gr.get_frame_config_value("app_start_time", 6)
    g_Context.app.wake_app(package_name, wait_time)


def stop_app(context, package_name):
    if not package_name:
        package_name = gr.get_app_package_name()
    g_Context.app.shut_app(package_name)


def return_pre_page(context):
    g_Context.element.key_event("4")


def to_device_home(context):
    g_Context.element.key_event("HOME")


def to_app_home(context):
    schema_goto_module = gr.get_value("projectScript").custom_operation
    to_home = getattr(schema_goto_module, "to_home")
    to_home()


def app_login(context, param1, param2):
    schema_goto_module = gr.get_value("projectScript").custom_operation
    login = getattr(schema_goto_module, "login")
    login(param1, param2)


def app_logout(context):
    schema_goto_module = gr.get_value("projectScript").custom_operation
    logout = getattr(schema_goto_module, "logout")
    logout()


def current_app():
    g_Context.app.current_app()
