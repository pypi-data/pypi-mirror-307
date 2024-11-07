# -*- coding: utf-8 -*-
"""
Global config
"""
import os


def get_local_server_ip():
    return os.environ.get("UDT_CAR_LOCAL_SERVER_IP")


def get_local_server_port():
    return os.environ.get("UDT_CAR_LOCAL_SERVER_PORT")


def get_result_dir():
    return os.environ.get("RESULT_DIR")


def set_test_id(test_id):
    if os.environ.get("TEST_ID"):
        os.environ["TEST_ID"] = test_id
    else:
        os.environ.setdefault("TEST_ID", test_id)


def get_test_id():
    return os.environ.get("TEST_ID", "")


def set_device_id(device_id):
    if os.environ.get("DEVICE_ID"):
        os.environ["DEVICE_ID"] = device_id
    else:
        os.environ.setdefault("DEVICE_ID", device_id)


def get_device_id():
    return os.environ.get("DEVICE_ID")


def get_raw_serial():
    return os.environ.get("UDT_DEVICE_SERIAL")


def set_script_id(script_id):
    if os.environ.get("SCRIPT_ID"):
        os.environ["SCRIPT_ID"] = script_id
    else:
        os.environ.setdefault("SCRIPT_ID", script_id)


def get_script_id():
    return os.environ.get("SCRIPT_ID")


def get_script_dir():
    return os.environ.get("UDT_SCRIPT_DIR")


def is_desktop_mode():
    return os.environ.get("COMMON_MODE", "") == "desktop"


def get_assistd_host():
    return os.environ.get("ASSISTD_HOST")


def get_report_host():
    return os.environ.get("REPORT_URL")


def dump_config():
    if get_local_server_ip() is not None:
        print("env: get_local_server_ip " + get_local_server_ip())

    if get_local_server_port() is not None:
        print("env: get_local_server_port " + get_local_server_port())

    if get_result_dir() is not None:
        print("env: get_result_dir " + get_result_dir())

    if get_test_id() is not None:
        print("env: get_test_id " + get_test_id())

    if get_device_id() is not None:
        print("env: get_device_id " + get_device_id())

    if is_desktop_mode() is not None:
        print("env: is_desktop_mode ", is_desktop_mode())

    if get_assistd_host() is not None:
        print("env: get_assistd_host " + get_assistd_host())

    if get_report_host() is not None:
        print("env: get_report_host " + get_report_host())
