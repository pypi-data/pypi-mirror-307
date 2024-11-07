# -*- coding: utf-8 -*-
"""
Poco element apis
"""
import time

import flybirds.core.global_resource as gr
import flybirds.core.plugin.plugins.default.ui_driver.poco.findsnap as find_snap
import flybirds.core.plugin.plugins.default.ui_driver.poco.poco_manage as pm
import flybirds.utils.flybirds_log as log
from flybirds.core.exceptions import FlybirdEleExistsException, FlybirdVerifyException
from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.utils import language_helper as lan
from flybirds.core.plugin.plugins.default.step.common import screenshot
from flybirds.utils.http_helper import HttpUdt


def wait_exists(poco, selector_str, optional):
    """
    determine whether the element exists within the specified time
    """
    timeout = optional["timeout"]
    context = None
    index = 1
    if "context" in optional:
        context = optional["context"]
    if "index" in optional:
        index = optional["index"]
    current_wait_second = 1
    find_success = False
    while timeout > 0:
        create_success = False
        try:
            poco_target = pm.create_poco_object_by_dsl(poco, selector_str, optional)
            if len(poco_target) > max(1, index - 1):
                poco_target = poco_target[index - 1]

            create_success = True
            search_time = current_wait_second
            if search_time > 3:
                search_time = 3
            ele_exists = poco_target.exists()
            log.info(
                "wait_exists: {}, ele_exists: {}, timeout: {}".format(
                    selector_str, ele_exists, timeout
                )
            )

            if ele_exists:
                find_success = True
                break

            poco_target.wait_for_appearance(timeout=search_time)
            find_success = True
            log.info(
                "wait_for_appearance: find_success: {}, timeout: {}".format(
                    find_success, timeout
                )
            )
            break
        except Exception as e:
            log.info(f"create_poco_object_by_dsl exception: {e}")
            if not create_success or not find_success:
                # modal error detection
                try:
                    result = detect_error(context)
                    log.info(f"detect_error result:{result}")
                    if not result:
                        break
                except Exception as e:
                    log.info(f"detect_error exception: {e}")
            time.sleep(1)
        if current_wait_second > 3:
            find_success = False
            break
        timeout -= current_wait_second
        current_wait_second += 1
    if not find_success:
        message = "during {}s time, not find {} in page".format(
            optional["timeout"], selector_str
        )
        raise FlybirdVerifyException(message)


def not_exist(poco, selector_str, optional):
    """
    determine whether the element does not exist
    """
    ele_exists = False
    try:
        poco_object = pm.create_poco_object_by_dsl(poco, selector_str, optional)
        ele_exists = poco_object.exists()
    except Exception:
        pass
    if ele_exists:
        message = "{} exists in page".format(selector_str)
        raise FlybirdEleExistsException(message)


def wait_disappear(poco, selector_str, optional):
    """
    determine whether the element disappears within the specified time
    """
    timeout = optional["timeout"]
    current_wait_second = 1
    disappear_success = False
    while timeout > 0:
        create_success = False
        try:
            poco_target = pm.create_poco_object_by_dsl(poco, selector_str, optional)
            create_success = True
            search_time = current_wait_second
            if search_time > 3:
                search_time = 3
            poco_target.wait_for_disappearance(timeout=search_time)
            disappear_success = True
            break
        except Exception:
            if not create_success:
                time.sleep(1)
        if current_wait_second > 4:
            break
        timeout -= current_wait_second
        current_wait_second += 1
    if not disappear_success:
        message = "during {}s time, {} not disappear in page".format(
            optional["timeout"], selector_str
        )
        raise FlybirdVerifyException(message)


def detect_error(context):
    # use_detect_error = gr.get_frame_config_value("use_detect_error", False)
    use_detect_error = gr.get_value("use_detect_error")
    if use_detect_error is False:
        log.info("detect error not start, return None")
        return False
    language = g_Context.get_current_language()
    modal_list = lan.parse_glb_str("modal_list", language)
    break_list = lan.parse_glb_str("break_list", language)
    poco = g_Context.ui_driver_instance

    img_path = screenshot(context)
    result = HttpUdt.ai_popup(img_path)
    close, buttons, popup = (
        result.get("close", None),
        result.get("txtbutton", None),
        result.get("popup", None),
    )
    if popup:
        log.info(f"in detect error method, pop-up detected: {popup}")
        screen_size = gr.get_device_size()
        if close:
            log.info(f"in detect error method, close detected: {close}")
            coord = close[0]["coordinates"]
            g_Context.step.click_coordinates(
                context, coord[0] * screen_size[0], coord[1] * screen_size[1]
            )
            return True

        elif buttons:
            modal_list = HttpUdt.popup_text()
            modal_list = [m.strip().lower() for m in modal_list]
            for button in buttons:
                if button["text"].strip().lower() in modal_list:
                    coord = button["coordinates"]
                    g_Context.step.click_coordinates(
                        context, coord[0] * screen_size[0], coord[1] * screen_size[1]
                    )
                    log.info(f"in detect error method, button detected: {button}")
                    return True

    for break_str in break_list:
        log.info(f"in detect error method, break_str detect: {break_str}")
        break_target = pm.create_poco_object_by_dsl(poco, break_str, None)
        is_existed = break_target.exists()
        if is_existed:
            break_target.click()
            if gr.get_frame_config_value("use_snap", False):
                find_snap.fix_refresh_status(True)
            log.info("detect_error: {}, layer_errors_exists: true".format(break_str))
            return False
