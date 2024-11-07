# -*- coding: utf-8 -*-
"""
Element swipe
"""
import re

import flybirds.core.global_resource as gr
import flybirds.core.plugin.plugins.default.ui_driver.poco.poco_swipe as ps
import flybirds.utils.dsl_helper as dsl_helper
import flybirds.utils.point_helper as point_helper
import flybirds.utils.flybirds_log as log
from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.core.exceptions import FlybirdsException
from flybirds.core.plugin.plugins.default.step.common import img_verify
from flybirds.core.plugin.plugins.default.step.click import get_sorted_coordinates


def ele_swipe(context, param1, param2, param3):
    poco_instance = gr.get_value("pocoInstance")

    param1_dict = dsl_helper.params_to_dic(param1)
    selector_str = param1_dict["selector"]
    optional = {}
    optional["context"] = context
    if "path" in param1_dict.keys():
        optional["path"] = param1_dict["path"]
    elif "multiSelector" in param1_dict.keys():
        optional["multiSelector"] = param1_dict["multiSelector"]
    if "timeout" in param1_dict.keys():
        optional["timeout"] = float(param1_dict["timeout"])
    else:
        optional["timeout"] = gr.get_frame_config_value("wait_ele_timeout", 10)

    param3_dict = dsl_helper.params_to_dic(param3, "swipeNumber")

    start_point = [0.5, 0.5]
    if "startX" in param3_dict.keys():
        start_point[0] = float(param3_dict["startX"])
    if "startY" in param3_dict.keys():
        start_point[1] = float(param3_dict["startY"])

    screen_size = gr.get_device_size()

    direction = point_helper.search_direction_switch(param2.strip())

    distance = float(param3_dict["swipeNumber"])

    duration = None
    if gr.get_frame_config_value("use_swipe_duration", False):
        duration = gr.get_frame_config_value("swipe_duration", 1)
    if "duration" in param3_dict.keys():
        duration = float(param3_dict["duration"])

    ready_time = gr.get_frame_config_value("swipe_ready_time", 1)
    if "readyTime" in param3_dict.keys():
        ready_time = float(param3_dict["readyTime"])

    ps.air_bdd_ele_swipe(
        poco_instance,
        selector_str,
        optional,
        start_point,
        screen_size,
        direction,
        distance,
        duration,
        ready_time,
    )


def full_screen_swipe(context, param1, param2):
    poco_instance = gr.get_value("pocoInstance")

    param2_dict = dsl_helper.params_to_dic(param2, "swipeNumber")

    start_point = [0.5, 0.5]
    if "startX" in param2_dict.keys():
        start_point[0] = float(param2_dict["startX"])
    if "startY" in param2_dict.keys():
        start_point[1] = float(param2_dict["startY"])

    screen_size = gr.get_device_size()

    direction = point_helper.search_direction_switch(param1.strip())

    distance = float(param2_dict["swipeNumber"])

    duration = None
    if gr.get_frame_config_value("use_swipe_duration", False):
        duration = gr.get_frame_config_value("swipe_duration", 1)
    if "duration" in param2_dict.keys():
        duration = float(param2_dict["duration"])

    ready_time = gr.get_frame_config_value("swipe_ready_time", 1)
    if "readyTime" in param2_dict.keys():
        ready_time = float(param2_dict["readyTime"])

    ps.air_bdd_full_screen_swipe(
        poco_instance,
        start_point,
        screen_size,
        direction,
        distance,
        duration,
        ready_time,
    )


def coord_swipe(context, param1, param2):
    poco_instance = gr.get_value("pocoInstance")
    fmt = lambda s: list(map(float, (filter(None, re.split("[, ]", s)))))
    start, end = fmt(param1), fmt(param2)
    ps.air_bdd_percent_point_swipe(poco_instance, start, end)


def img_swipe(context, param1, param2, param3):
    poco_instance = gr.get_value("pocoInstance")

    pos, size = get_img_pos(context, param1)

    param3_dict = dsl_helper.params_to_dic(param3, "swipeNumber")
    start_point = [0.5, 0.5]
    if "startX" in param3_dict.keys():
        start_point[0] = float(param3_dict["startX"])
    if "startY" in param3_dict.keys():
        start_point[1] = float(param3_dict["startY"])
    distance = float(param3_dict["swipeNumber"])

    screen_size = gr.get_device_size()
    direction = point_helper.search_direction_switch(param2.strip())

    duration = None
    if gr.get_frame_config_value("use_swipe_duration", False):
        duration = gr.get_frame_config_value("swipe_duration", 1)
    if "duration" in param3_dict.keys():
        duration = float(param3_dict["duration"])

    ready_time = gr.get_frame_config_value("swipe_ready_time", 1)
    if "readyTime" in param3_dict.keys():
        ready_time = float(param3_dict["readyTime"])

    ps.air_bdd_img_swipe(
        poco_instance,
        start_point,
        screen_size,
        pos,
        size,
        direction,
        distance,
        duration,
        ready_time,
    )


def get_img_pos(context, param):
    param_dict = dsl_helper.params_to_dic(param)
    result = img_verify(context, param_dict["selector"])
    index = 1
    if "index" in param_dict:
        index = int(param_dict["index"])
    matchRes = []
    for res in result:
        x = res.get("rect").x + res.get("rect").width / 2
        y = res.get("rect").y + res.get("rect").height / 2
        matchRes.append((x, y))

    sortedRes = get_sorted_coordinates(matchRes)
    pos, size = [0, 0], [g_Context.image_size[1], g_Context.image_size[0]]
    if len(sortedRes) >= index:
        coord = sortedRes[index - 1]
        log.info(f"image found: {coord}")
        x_coordinate = float(coord[0]) / g_Context.image_size[1]
        y_coordinate = float(coord[1]) / g_Context.image_size[0]
        pos = [x_coordinate, y_coordinate]
    else:
        raise FlybirdsException(f"image error, {param} not found.")
    return pos, size


def ele_drag(context, param1, param2):
    poco_instance = gr.get_value("pocoInstance")

    param1_dict = dsl_helper.params_to_dic(param1)
    selector_str = param1_dict["selector"]
    optional = {}
    optional["context"] = context
    if "path" in param1_dict.keys():
        optional["path"] = param1_dict["path"]
    elif "multiSelector" in param1_dict.keys():
        optional["multiSelector"] = param1_dict["multiSelector"]
    if "timeout" in param1_dict.keys():
        optional["timeout"] = float(param1_dict["timeout"])
    else:
        optional["timeout"] = gr.get_frame_config_value("wait_ele_timeout", 10)

    f = lambda x: list(map(float, filter(None, re.split("[, ]", x))))
    coord = f(param2)

    ps.air_bdd_ele_drag(poco_instance, selector_str, optional, coord)
