# -*- coding: utf-8 -*-
"""
Command methods.
"""
import json
import os
import re
import time
import datetime
import traceback

from PIL import Image as Img
import numpy as np

import flybirds.core.global_resource as gr
import flybirds.utils.flybirds_log as log
import flybirds.utils.dsl_helper as dsl_helper
from flybirds.core.plugin.plugins.default.screen import BaseScreen
from flybirds.core.driver import ui_driver
from flybirds.core.global_context import GlobalContext
from baseImage import Image
from flybirds.core.exceptions import FlybirdsException
from flybirds.utils import file_helper
from flybirds.utils.cos_helper import COS_FILE_PREFIX, cos_client
from flybirds.utils.http_helper import HttpUdt


def sleep(context, param):
    time.sleep(float(param))


def screenshot(context):
    step_index = context.cur_step_index - 1
    return BaseScreen.screen_link_to_behave(context.scenario, step_index, "screen_")


def ocr(context, param=None, region=None):
    step_index = context.cur_step_index - 1
    image_path = BaseScreen.screen_link_to_behave(
        context.scenario, step_index, "screen_", True
    )

    if region:
        image = Img.open(image_path).convert("RGB")
        width, height = image.size
        lx, rx = map(lambda x: x * width, region[::2])
        ly, ry = map(lambda y: y * height, region[1::2])
        cropped_image = image.crop((lx, ly, rx, ry))
        cropped_image.save(image_path)

    right_gap_max = None
    left_gap_max = None
    height_gap_max = None
    skip_height_max = None
    if param is not None:
        param_dict = dsl_helper.params_to_dic(param)
        selector_str = param_dict["selector"]
        if (
            "right_gap_max=" in selector_str
            or "left_gap_max=" in selector_str
            or "height_gap_max=" in selector_str
            or "skip_height_max=" in selector_str
        ):
            str_list = selector_str.split("=")
            param_dict[str_list[0]] = str_list[1]
        if (
            "right_gap_max" in param_dict.keys()
            and 0 < float(param_dict["right_gap_max"]) < 1
        ):
            right_gap_max = float(param_dict["right_gap_max"])
            log.info(f"right_gap_max is {right_gap_max}")
        if (
            "left_gap_max" in param_dict.keys()
            and 0 < float(param_dict["left_gap_max"]) < 1
        ):
            left_gap_max = float(param_dict["left_gap_max"])
            log.info(f"left_gap_max is {left_gap_max}")
        if (
            "height_gap_max" in param_dict.keys()
            and 0 < float(param_dict["height_gap_max"]) < 1
        ):
            height_gap_max = float(param_dict["height_gap_max"])
            log.info(f"height_gap_max is {height_gap_max}")
        if (
            "skip_height_max" in param_dict.keys()
            and 0 < float(param_dict["skip_height_max"]) < 1
        ):
            skip_height_max = float(param_dict["skip_height_max"])
            log.info(f"skip_height_max is {skip_height_max}")

    BaseScreen.image_ocr(
        image_path, right_gap_max, left_gap_max, height_gap_max, skip_height_max
    )


def change_ocr_lang(context, lang=None):
    """
    change ocr language
    """
    ocr_instance = ui_driver.init_ocr(lang)
    gr.set_value("ocrInstance", ocr_instance)
    context.ocr_instance = ocr_instance
    GlobalContext.ocr_driver_instance = ocr_instance
    log.info("ocr change lang complete with {}".format(lang))


def prev_fail_scenario_relevance(context, param1, param2):
    """
    Related operations for the previous failure scenario
    """
    try:
        print("failed info about param", param2)
        fail_info = gr.get_rerun_info(param2.strip())
        if not (fail_info is None):
            if isinstance(fail_info, str):
                fail_info = json.loads(fail_info)
            if isinstance(fail_info, dict):
                scenario = context.scenario
                step_index = context.cur_step_index - 1

                scenario_uri = "failed function: {}。 senario: {}".format(
                    fail_info["feature_name"], fail_info["scenario_name"]
                )
                scenario_uri = scenario_uri.replace(",", "#")
                data = "embeddingsTags, stepIndex={}, <p>{}</p>".format(
                    step_index, scenario_uri
                )
                scenario.description.append(data)

                if isinstance(fail_info["description"], list):
                    # fail_description = fail_info["description"]
                    for des_item in fail_info["description"]:
                        print("des_item", des_item)
                        if des_item.strip().startswith("embeddingsTags"):
                            if "<image" in des_item and "/screen_" in des_item:
                                continue
                            else:
                                scenario.description.append(
                                    re.sub(
                                        r"stepIndex=\d+",
                                        "stepIndex={}".format(step_index),
                                        des_item,
                                        1,
                                    )
                                )
        else:
            log.warn("not find failed senario info: ", param2)
    except Exception:
        log.warn("rerun failed senario error")
        log.warn(traceback.format_exc())


def img_verify(context, search_image_paths):
    """
    verify image exist or not
    """
    search_image_paths = search_image_paths.split(",")
    for search_image_path in search_image_paths:
        search_image_path = search_image_path.strip()
        search_image_path = f"{search_image_path}"
        if search_image_path.startswith(COS_FILE_PREFIX):
            # base_path = os.path.join(os.getcwd(), "download")
            # remote_img_url = search_image_path.split(COS_FILE_PREFIX)[1]
            # tmp_search_image_path = os.path.join(base_path, remote_img_url)
            # log.warn(
            #     f"convert search_image_path from {search_image_path} to {tmp_search_image_path}"
            # )
            # if os.path.exists(tmp_search_image_path):
            #     search_image_path = tmp_search_image_path
            # else:
            #     file_helper.create_dirs(os.path.dirname(tmp_search_image_path))
            #     cos_client.downloadFromCos(remote_img_url, tmp_search_image_path)
            #     if os.path.exists(tmp_search_image_path):
            #         search_image_path = tmp_search_image_path
            search_image_path = search_image_path.split(COS_FILE_PREFIX + "car")[1]
        if not os.path.exists(search_image_path):
            file_path = HttpUdt.download_file(search_image_path)
            log.info(f"download file to {file_path}")
            search_image_path = file_path
        step_index = context.cur_step_index - 1
        source_image_path = BaseScreen.screen_link_to_behave(
            context.scenario, step_index, "screen_", False
        )
        GlobalContext.image_size = Image(source_image_path).size
        if result := BaseScreen.image_verify(source_image_path, search_image_path):
            return result
    return []


def audio_verify(search_audio_paths):
    """
    verify audio exist or not
    """
    search_audio_paths = search_audio_paths.split(",")
    for search_audio_path in search_audio_paths:
        search_audio_path = search_audio_path.strip()
        search_audio_path = f"{search_audio_path}"
        if search_audio_path.startswith(COS_FILE_PREFIX):
            base_path = os.path.join(os.getcwd(), "download")
            remote_audio_url = search_audio_path.split(COS_FILE_PREFIX)[1]
            tmp_search_audio_path = os.path.join(base_path, remote_audio_url)
            log.warn(
                f"convert search_audio_path from {search_audio_path} to {tmp_search_audio_path}"
            )
            if os.path.exists(tmp_search_audio_path):
                search_audio_path = tmp_search_audio_path
            else:
                file_helper.create_dirs(os.path.dirname(tmp_search_audio_path))
                cos_client.downloadFromCos(remote_audio_url, tmp_search_audio_path)
                if os.path.exists(tmp_search_audio_path):
                    search_audio_path = tmp_search_audio_path
        elif not os.path.exists(search_audio_path):
            file_path = HttpUdt.download_file(search_audio_path)
            log.info(f"download file to {file_path}")
            search_audio_path = file_path
    return search_audio_path


def loop_times(context, param):
    """loop times"""
    assert param.isdigit(), f"Please check the type, param must be int."
    param = int(param)

    cur_times = gr.get_value("loop_times", 0) + 1
    gr.set_value("loop_times", cur_times)
    if param == cur_times:
        gr.set_value("loop_times", 0)
        raise FlybirdsException(f"Loop times reached, stop the loop")
