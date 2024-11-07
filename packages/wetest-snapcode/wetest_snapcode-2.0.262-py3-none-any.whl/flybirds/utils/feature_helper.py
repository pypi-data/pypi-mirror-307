# -*- coding: utf-8 -*-
"""
feature helper
"""
import os
import sys

from flybirds.utils import flybirds_log as log, download_helper
from flybirds.utils.file_helper import create_dirs


SCRIPT_TYPE_OF_FILE = "file"
SCRIPT_TYPE_OF_CODE = "code"
SCRIPT_TYPE_OF_HTTP = "http"


def store_feature_to_file_path(script, script_type, d_id=None, d_dir=None):
    """
    json feature to file
    """
    script_path = ""
    if script_type == SCRIPT_TYPE_OF_CODE:
        base_path = os.path.join(os.getcwd(), d_dir)
        create_dirs(base_path)
        s_script_path = os.path.join(d_dir, f"{d_id}.feature")
        if sys.platform.startswith('win'):
            s_script_path = s_script_path.replace('\\', '/')
        with open(s_script_path, "w", encoding='utf-8', newline='') as file:
            file.write(script + "\n")
        script_path = s_script_path
    elif script_type == SCRIPT_TYPE_OF_HTTP:
        base_path = os.path.join(os.getcwd(), d_dir)
        create_dirs(base_path)
        d_script_path = os.path.join(base_path, f"{d_id}.feature")
        log.info("download start")
        download_helper.downlaod(script, d_script_path)
        log.info("download end")
        script_path = d_script_path
    return script_path