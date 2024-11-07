# -*- coding: utf-8 -*-
"""
Step implement of element click.
"""
import re
import time
from random import random

import flybirds.core.global_resource as gr
import flybirds.core.plugin.plugins.default.ui_driver.poco.findsnap as find_snap
import flybirds.utils.dsl_helper as dsl_helper
from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.core.plugin.plugins.default.step.verify import (
    paddle_fix_txt,
    ocr_txt_exist,
    ocr_regional_txt_exist,
)
from flybirds.core.plugin.plugins.default.step.common import img_verify, screenshot
import flybirds.utils.flybirds_log as log
from flybirds.core.exceptions import FlybirdNotFoundException, FlybirdsException
from flybirds.utils import language_helper as lan
import flybirds.core.plugin.plugins.default.ui_driver.poco.poco_ele as poco_ele
import flybirds.core.plugin.plugins.default.ui_driver.poco.poco_manage as pm
from flybirds.core.plugin.plugins.default.step.verify import wait_ocr_text_appear
from flybirds.utils.http_helper import HttpUdt


def click_ele(context, param):
    print("click_ele====click_ele", param)
    """
    Click  element
    """
    param_dict = dsl_helper.params_to_dic(param)
    poco_instance = gr.get_value("pocoInstance")

    selector_str = param_dict["selector"]
    optional = {}
    optional["context"] = context
    if "path" in param_dict.keys():
        optional["path"] = param_dict["path"]
    elif "multiSelector" in param_dict.keys():
        optional["multiSelector"] = param_dict["multiSelector"]
    if "timeout" in param_dict.keys():
        optional["timeout"] = float(param_dict["timeout"])
    else:
        optional["timeout"] = gr.get_frame_config_value("wait_ele_timeout", 10)
    if "index" in param_dict.keys():
        optional["index"] = int(param_dict["index"])
    else:
        optional["index"] = 1
    if "double_click" in param_dict.keys():
        optional["double_click"] = int(param_dict["double_click"])
    if "freq" in param_dict.keys():
        optional["freq"] = int(param_dict["freq"])

    optional["duration"] = get_click_duration(param)

    verify_dsl_str = None
    verify_optional = {}
    verify_optional["context"] = context
    verify_action = None
    if "verifyEle" in param_dict.keys():
        verify_dsl_str = param_dict["verifyEle"]
        verify_action = param_dict["verifyAction"]
    if "verifyIsPath" in param_dict.keys():
        verify_optional["path"] = param_dict["verifyIsPath"]
    elif "verifyIsMultiSelector" in param_dict.keys():
        verify_optional["multiSelector"] = param_dict["verifyIsMultiSelector"]
    if "verifyTimeout" in param_dict.keys():
        verify_optional["timeout"] = float(param_dict["verifyTimeout"])
    else:
        verify_optional["timeout"] = gr.get_frame_config_value(
            "click_verify_timeout", 10
        )

    g_Context.element.air_bdd_click(
        poco_instance,
        selector_str,
        optional,
        verify_dsl_str,
        verify_optional,
        verify_action,
    )


def ai_icon_exist(context, name):
    img_path = screenshot(context)
    result = HttpUdt.icon_detect(img_path, name)
    if not result["data"]:
        if t := result.get("ms"):
            raise FlybirdsException(f"{name} not found, it spends [{t}]ms.")
        if msg := result["msg"]:
            raise FlybirdsException(msg)
    return result


def ai_icon_click(context, name, index=0):
    result = ai_icon_exist(context, name)

    t = result["ms"]
    log.info(f"{name} found, it spends [{t}]ms")
    icon = result["data"][index]
    screen_size = gr.get_device_size()
    coord = icon["coordinates"]
    x, y = coord[:2]
    x *= screen_size[0]
    y *= screen_size[1]
    click_coordinates(context, x, y, {})


def click_text(context, param):
    print("click_text====click_text")
    param_dict = dsl_helper.params_to_dic(param)
    poco_instance = gr.get_value("pocoInstance")

    selector_str = param_dict["selector"]
    if "fuzzyMatch" in param_dict.keys():
        selector_str = "textMatches=" + selector_str
    else:
        selector_str = "text=" + selector_str
    optional = {}
    optional["context"] = context
    if "timeout" in param_dict.keys():
        optional["timeout"] = float(param_dict["timeout"])
    else:
        optional["timeout"] = gr.get_frame_config_value("wait_ele_timeout", 10)
    if "double_click" in param_dict.keys():
        optional["double_click"] = int(param_dict["double_click"])

    optional["duration"] = get_click_duration(param)

    verify_dsl_str = None
    verify_optional = {}
    verify_action = None
    if "verifyEle" in param_dict.keys():
        verify_dsl_str = param_dict["verifyEle"]
        verify_action = param_dict["verifyAction"]
    if "verifyIsPath" in param_dict.keys():
        verify_optional["path"] = param_dict["verifyIsPath"]
    elif "verifyIsMultiSelector" in param_dict.keys():
        verify_optional["multiSelector"] = param_dict["verifyIsMultiSelector"]
    if "verifyTimeout" in param_dict.keys():
        verify_optional["timeout"] = float(param_dict["verifyTimeout"])
    else:
        verify_optional["timeout"] = gr.get_frame_config_value(
            "click_verify_timeout", 10
        )

    g_Context.element.air_bdd_click(
        poco_instance,
        selector_str,
        optional,
        verify_dsl_str,
        verify_optional,
        verify_action,
    )


def click_coordinates(context, x, y, param):
    print("click_coordinates====click_coordinates")
    poco_instance = gr.get_value("pocoInstance")
    screen_size = gr.get_device_size()
    x_coordinate, y_coordinate = map(float, (x, y))
    if x_coordinate > 1 and y_coordinate > 1:
        x_coordinate /= screen_size[0]
        y_coordinate /= screen_size[1]
    param_dict = dsl_helper.params_to_dic(param)
    do_poco_click(poco_instance, x_coordinate, y_coordinate, param_dict)
    if gr.get_frame_config_value("use_snap", False):
        find_snap.fix_refresh_status(True)


def click_coordinates_pos(context, pos):
    print("click_coordinates====click_coordinates")
    poco_instance = gr.get_value("pocoInstance")
    screen_size = gr.get_device_size()
    f = lambda x: filter(None, re.split("[, ]", x))
    x, y, *_ = f(pos)
    x_coordinate, y_coordinate = map(float, (x, y))
    if x_coordinate > 1 and y_coordinate > 1:
        x_coordinate /= screen_size[0]
        y_coordinate /= screen_size[1]
    param_dict = dsl_helper.params_to_dic(pos)
    do_poco_click(poco_instance, x_coordinate, y_coordinate, param_dict)
    if gr.get_frame_config_value("use_snap", False):
        find_snap.fix_refresh_status(True)


def click_ocr_text(context, param):
    print("click_ocr_text====click_ocr_text")
    param_dict = dsl_helper.params_to_dic(param)
    selector_str = param_dict["selector"]
    index = 1
    if "index" in param_dict:
        index = int(param_dict["index"])
    matchRes = wait_ocr_text_appear(context, selector_str)

    if len(matchRes) >= index:
        coord = matchRes[index - 1]
        log.info(f"[click ocr txt] click txt found: {matchRes} {coord}")
        poco_instance = gr.get_value("pocoInstance")
        x_coordinate = float(coord[0]) / g_Context.image_size[1]
        y_coordinate = float(coord[1]) / g_Context.image_size[0]
        do_poco_click(poco_instance, x_coordinate, y_coordinate, param_dict)
    else:
        raise Exception("[click ocr text] click ocr text is not found !")


def click_image(context, param):
    print("click_image====click_image")
    timeout = 3
    param_dict = dsl_helper.params_to_dic(param)
    while timeout:
        result = img_verify(context, param)
        if result:
            log.info(f"detect img result: {result}")
            break
        res = poco_ele.detect_error(context)
        log.info(f"detect_error result: {res}")
        if not res:
            break
        time.sleep(1)
        timeout -= 1

    index = 1
    if "index" in param_dict:
        index = int(param_dict["index"])
    matchRes = []
    for res in result:
        x = res.get("rect").x + res.get("rect").width / 2
        y = res.get("rect").y + res.get("rect").height / 2
        matchRes.append((x, y))

    sortedRes = get_sorted_coordinates(matchRes)
    try:
        if len(sortedRes) >= index:
            coord = sortedRes[index - 1]
            log.info(f"[click_image]image found: {coord}")
            poco_instance = gr.get_value("pocoInstance")
            x_coordinate = float(coord[0]) / g_Context.image_size[1]
            y_coordinate = float(coord[1]) / g_Context.image_size[0]
            do_poco_click(poco_instance, x_coordinate, y_coordinate, param_dict)
        else:
            raise Exception("[click image] click image error !")
    except Exception:
        raise Exception("[click image] click image error !")


def click_regional_ocr_text(context, param1, param2):
    print("click_regional_ocr_text====click_regional_ocr_text")
    param1_dict = dsl_helper.params_to_dic(param1)
    selector_str = param1_dict["selector"]
    str_list = selector_str.split("=")
    regional_id = int(str_list[1])
    regional_ocr_result = list(
        filter(
            lambda item: item["regional_id"] == regional_id, g_Context.struct_ocr_result
        )
    )
    flag = False
    param2_dict = dsl_helper.params_to_dic(param2)
    selector_str = param2_dict["selector"]
    for line in regional_ocr_result:
        try:
            if (
                "fuzzyMatch" in param2_dict.keys()
                and re.search(selector_str, line["txt"], flags=0) is not None
            ):
                log.info(
                    f"[click regional ocr txt] click txt fuzzyMatch found: {line['txt']}"
                )
                flag = True
            else:
                trim_param = selector_str.replace(" ", "")
                fixed_txt = paddle_fix_txt([line["txt"]], True)
                line_param = trim_param.replace("-", "")
                line_txt = fixed_txt[0].replace("-", "")
                if trim_param == fixed_txt[0] or line_param == line_txt:
                    log.info(f"[click regional ocr txt] click txt found: {line['txt']}")
                    flag = True
            if flag is True:
                box = line["box"]
                x = (box[0][0] + box[1][0]) / 2
                y = (box[0][1] + box[2][1]) / 2
                poco_instance = gr.get_value("pocoInstance")
                x_coordinate = float(x) / g_Context.image_size[1]
                y_coordinate = float(y) / g_Context.image_size[0]
                do_poco_click(poco_instance, x_coordinate, y_coordinate, param1_dict)
                break
        except Exception:
            raise Exception("[click regional ocr text] click ocr text error !")
    if flag is False:
        raise Exception("[click regional ocr text] click ocr text is not found !")


def click_regional_ocr(context, param):
    print("click_regional_ocr====click_regional_ocr")
    try:
        param_dict = dsl_helper.params_to_dic(param)
        selector_str = param_dict["selector"]
        str_list = selector_str.split("=")
        regional_id = int(str_list[1])
        regional_ocr_result = list(
            filter(
                lambda item: item["regional_id"] == regional_id,
                g_Context.struct_ocr_result,
            )
        )
        box = regional_ocr_result[0]["regional_box"]
        log.info(f"[click regional ocr] regional box found: {box}")
        x = (box[0][0] + box[1][0]) / 2
        y = (box[0][1] + box[2][1]) / 2
        poco_instance = gr.get_value("pocoInstance")
        x_coordinate = float(x) / g_Context.image_size[1]
        y_coordinate = float(y) / g_Context.image_size[0]
        do_poco_click(poco_instance, x_coordinate, y_coordinate, param_dict)
    except Exception:
        raise Exception("[click regional ocr] click regional box error !")


def init_click_action_selector(selector, click_action=None):
    if click_action:
        param_dict = dsl_helper.params_to_dic(click_action, "click_action")
        if "duration" in param_dict.keys() and "duration" not in selector:
            selector = selector + ", duration=" + param_dict["duration"]
        if "click_count" in param_dict.keys() and param_dict["click_count"] == "2":
            selector = selector + ", double_click=1"
        if "random_count" in param_dict.keys() and "random_count" not in selector:
            selector = selector + ", random_click=1"
        if "freq" in click_action:
            selector = selector + "," + click_action
    return selector


def do_poco_click(poco_instance, x_coordinate, y_coordinate, param_dict):
    if "random_click" in param_dict.keys():
        x_coordinate = random()
        y_coordinate = random()
        log.info(f"[click anywhere]: {x_coordinate} {y_coordinate}")
        poco_instance.click([x_coordinate, y_coordinate])
        return

    duration = 0
    if "duration" in param_dict.keys():
        duration = int(param_dict["duration"])
    freq = int(param_dict.get("freq", "1"))

    if "double_click" in param_dict.keys():
        poco_instance.click([x_coordinate, y_coordinate])
        poco_instance.click([x_coordinate, y_coordinate])
    elif duration > 0:
        poco_instance.long_click([x_coordinate, y_coordinate], duration)
    else:
        for _ in range(freq):
            poco_instance.click([x_coordinate, y_coordinate])


def get_click_duration(param):
    param_dict = dsl_helper.params_to_dic(param)
    if "duration" in param_dict.keys():
        duration = int(param_dict["duration"])
    else:
        duration = 0

    return duration


def get_sorted_coordinates(coordinates, minDis=50):
    if len(coordinates) == 1:
        return coordinates

    coordinates = sorted(coordinates, key=lambda coord: coord[1])

    grouped_coordinates = []
    current_group = []
    for coord in coordinates:
        if len(current_group) == 0:
            current_group.append(coord)
        else:
            if abs(coord[1] - current_group[0][1]) <= minDis:
                current_group.append(coord)
            else:
                grouped_coordinates.append(current_group)
                current_group = [coord]
    grouped_coordinates.append(current_group)

    # 对每个组的坐标按照横坐标进行排序
    sorted_coordinates = []
    for group in grouped_coordinates:
        sorted_group = sorted(group, key=lambda coord: coord[0])
        sorted_coordinates.extend(sorted_group)

    return sorted_coordinates


def click_to_ele_with_direction(context, param1, param2, direction):
    param1_dict = dsl_helper.params_to_dic(param1)
    selector_str = param1_dict["selector"]

    param2_dict = dsl_helper.params_to_dic(param2)
    target_selector_str = param2_dict["selector"]

    poco_instance = gr.get_value("pocoInstance")
    direction = direction.strip()
    optional = {}
    optional["context"] = context
    if "path" in param2_dict.keys():
        optional["path"] = param2_dict["path"]
    elif "multiSelector" in param2_dict.keys():
        optional["multiSelector"] = param2_dict["multiSelector"]
    if "timeout" in param2_dict.keys():
        optional["timeout"] = float(param2_dict["timeout"])
    else:
        optional["timeout"] = gr.get_frame_config_value("wait_ele_timeout", 10)
    if "index" in param2_dict.keys():
        optional["index"] = int(param2_dict["index"])
    else:
        optional["index"] = 1

    screen_size = gr.get_device_size()

    g_Context.element.air_bdd_click_with_direction(
        poco_instance,
        selector_str,
        target_selector_str,
        direction,
        screen_size,
        optional,
    )


def init_params(context, param):
    param_dict = dsl_helper.params_to_dic(param)
    selector_str = param_dict["selector"]
    index = 1
    if "index" in param_dict:
        index = int(param_dict["index"])
    return (param_dict, selector_str, index)


def get_image_coordinates(context, param):
    result = img_verify(context, param)
    matchRes = []
    for res in result:
        x = res.get("rect").x + res.get("rect").width / 2
        y = res.get("rect").y + res.get("rect").height / 2
        width = res.get("rect").width
        height = res.get("rect").height
        matchRes.append((x, y, width, height))
    return matchRes


def get_ocr_coordinates(context, param_dict, selector_str):
    matchRes = []
    flag = False
    screen_size = gr.get_device_size()

    for line in g_Context.ocr_result:
        try:
            if (
                "fuzzyMatch" in param_dict.keys()
                and re.search(selector_str, line[1][0], flags=0) is not None
            ):
                log.info(f"[click ocr txt] click txt fuzzyMatch found: {line[1][0]}")
                flag = True
            else:
                trim_param = selector_str.replace(" ", "")
                fixed_txt = paddle_fix_txt([line[1][0]], True)
                line_param = trim_param.replace("-", "")
                line_txt = fixed_txt[0].replace("-", "")
                if trim_param == fixed_txt[0] or line_param == line_txt:
                    log.info(f"[click ocr txt] click txt found: {line[1][0]}")
                    flag = True
            if flag is True:
                box = line[0]
                x_factor = screen_size[0] / g_Context.image_size[1]
                y_factor = screen_size[1] / g_Context.image_size[0]
                x = (box[0][0] + box[1][0]) / 2
                y = (box[0][1] + box[2][1]) / 2
                x = float(x) * x_factor
                y = (g_Context.image_size[0] - float(y)) * y_factor
                width = (box[1][0] - box[0][0]) * x_factor
                height = (box[2][1] - box[0][1]) * y_factor
                matchRes.append((x, y, width, height))
                flag = False
        except Exception:
            raise Exception("[click ocr text] click ocr text error !")
    return matchRes


def get_poco_coordinates(context, param_dict, selector_str):
    matchRes = []

    poco_instance = gr.get_value("pocoInstance")
    optional = {}
    optional["context"] = context
    if "path" in param_dict.keys():
        optional["path"] = param_dict["path"]
    elif "multiSelector" in param_dict.keys():
        optional["multiSelector"] = param_dict["multiSelector"]
    if "timeout" in param_dict.keys():
        optional["timeout"] = float(param_dict["timeout"])
    else:
        optional["timeout"] = gr.get_frame_config_value("wait_ele_timeout", 10)
    if "index" in param_dict.keys():
        optional["index"] = int(param_dict["index"])
    else:
        optional["index"] = 1

    poco_ele.wait_exists(poco_instance, selector_str, optional)
    poco_object = pm.create_poco_object_by_dsl(poco_instance, selector_str, optional)
    screen_size = gr.get_device_size()
    for poco in poco_object:
        x, y = poco.get_position()
        width, height = poco.get_size()
        x = (x + width / 2) * screen_size[0]
        y = (1 - y - height / 2) * screen_size[1]
        matchRes.append((x, y, width * screen_size[0], height * screen_size[1], poco))
    return matchRes


def click_with_direction(context, param1, param2, direction, tag1, tag2):
    param1_dict, selector1_str, index1 = init_params(context, param1)
    param2_dict, selector2_str, index2 = init_params(context, param2)

    direction = direction.strip()
    language = g_Context.get_current_language()
    direct_left = lan.parse_glb_str("left", language)
    direct_right = lan.parse_glb_str("right", language)
    direct_up = lan.parse_glb_str("up", language)
    direct_down = lan.parse_glb_str("down", language)

    if tag1 == "image":
        matchRes1 = get_image_coordinates(context, param1)
        matchRes1 = get_sorted_coordinates(matchRes1)
    elif tag1 == "ocr":
        matchRes1 = get_ocr_coordinates(context, param1_dict, selector1_str)
    elif tag1 == "poco":
        matchRes1 = get_poco_coordinates(context, param1_dict, selector1_str)

    if tag2 == "image":
        matchRes2 = get_image_coordinates(context, param2)
    elif tag2 == "ocr":
        matchRes2 = get_ocr_coordinates(context, param2_dict, selector2_str)
    elif tag2 == "poco":
        matchRes2 = get_poco_coordinates(context, param2_dict, selector2_str)

    try:
        if len(matchRes1) >= index1 and len(matchRes2) >= index2:
            coord1 = matchRes1[index1 - 1]
            log.info(f"[raw {tag1}] {tag1} found: {coord1}")
            flag = False
            for coord2 in matchRes2:
                log.info(f"[click {tag2}] {tag2} found: {coord2}")
                if direction == direct_left:
                    flag = (
                        coord1[0] > coord2[0]
                        and abs(coord1[1] - coord2[1])
                        < 2 * max(coord1[3], coord2[3]) / 3
                    )
                elif direction == direct_right:
                    flag = (
                        coord1[0] < coord2[0]
                        and abs(coord1[1] - coord2[1])
                        < 2 * max(coord1[3], coord2[3]) / 3
                    )
                elif direction == direct_up:
                    flag = (
                        coord1[1] < coord2[1]
                        and abs(coord1[0] - coord2[0])
                        < 2 * max(coord1[2], coord2[2]) / 3
                    )
                elif direction == direct_down:
                    flag = (
                        coord1[1] > coord2[1]
                        and abs(coord1[0] - coord2[0])
                        < 2 * max(coord1[2], coord2[2]) / 3
                    )
                if flag and tag2 == "poco":
                    coord2[-1].click()
                    break
                elif flag:
                    poco_instance = gr.get_value("pocoInstance")
                    x_coordinate = float(coord2[0]) / g_Context.image_size[1]
                    y_coordinate = float(coord2[1]) / g_Context.image_size[0]
                    if tag2 == "image":
                        do_poco_click(
                            poco_instance, x_coordinate, y_coordinate, param2_dict
                        )
                    elif tag2 == "ocr":
                        screen_size = gr.get_device_size()
                        x_factor = screen_size[0] / g_Context.image_size[1]
                        y_factor = screen_size[1] / g_Context.image_size[0]
                        do_poco_click(
                            poco_instance,
                            x_coordinate / x_factor,
                            1 - y_coordinate / y_factor,
                            param2_dict,
                        )
                    break

            if not flag:
                message = f"{param2} not find"
                raise FlybirdNotFoundException(message, {})

        elif len(matchRes1) < index1:
            message = f"{param1} not find"
            raise FlybirdNotFoundException(message, {})
        else:
            message = f"{param2} not find, {matchRes2} {index2}"
            raise FlybirdNotFoundException(message, {})

    except Exception:
        raise Exception(f"[click {tag2}] click {tag2} error !")
