# -*- coding: utf-8 -*-
"""
Poco element click
"""
import flybirds.core.global_resource as gr
from flybirds.core.global_context import GlobalContext as g_Context
import flybirds.core.plugin.plugins.default.ui_driver.poco.findsnap as findsnap
import flybirds.core.plugin.plugins.default.ui_driver.poco.poco_ele as poco_ele
import flybirds.core.plugin.plugins.default.ui_driver.poco.poco_manage as pm
import flybirds.core.plugin.plugins.default.ui_driver.poco.poco_position as pi
from flybirds.core.plugin.plugins.default.ui_driver.poco import poco_text
from flybirds.core.exceptions import (
    PositionNotChangeException,
    FlybirdNotFoundException,
)
from flybirds.utils import language_helper as lan
import flybirds.utils.flybirds_log as log


def air_bdd_click(
    poco,
    select_dsl_str,
    optional,
    verify_dsl_str=None,
    verify_optional=None,
    verify_action=None,
):
    """
    click on the element,
    optional parameters to determine whether the clicked page is rendered
    :param poco:
    :param select_dsl_str:
    :param optional: Optional parameters
    :param verify_dsl_str:
    :param verify_optional:
    :param verify_action:
    :return:
    """

    poco_ele.wait_exists(poco, select_dsl_str, optional)
    poco_object = pm.create_poco_object_by_dsl(poco, select_dsl_str, optional)
    index = 1
    if "index" in optional:
        index = optional["index"]
    if len(poco_object) > max(1, index - 1):
        poco_object = poco_object[index - 1]
    freq = int(optional.get("freq", "1"))
    o_position = None
    o_text = None
    if (not (verify_action is None)) and verify_action == "position":
        verify_poco_object = pm.create_poco_object_by_dsl(
            poco, verify_dsl_str, verify_optional
        )
        o_position = verify_poco_object.get_position()
    elif (not (verify_action is None)) and verify_action == "text":
        verify_poco_object = pm.create_poco_object_by_dsl(
            poco, verify_dsl_str, verify_optional
        )
        o_text = verify_poco_object.get_text()

    if "duration" in optional and optional["duration"] > 0:
        poco_object.long_click(optional["duration"])
    elif "double_click" in optional:
        poco_object.click()
        poco_object.click()
    else:
        for _ in range(freq):
            poco_object.click()

    if gr.get_frame_config_value("use_snap", False):
        # findsnap.refresh_snap()
        findsnap.fix_refresh_status(True)
    if not (verify_dsl_str is None):
        verify_click_end(
            poco,
            verify_dsl_str,
            verify_optional,
            verify_action,
            o_position,
            o_text,
        )


def verify_click_end(
    poco, verify_dsl_str, verify_optional, verify_action, o_position, o_text
):
    """
    determine whether the rendering of the click effect is completed according
    to the movement of the element,the disappearance of the element or the text
    :param poco:
    :param verify_dsl_str:
    :param verify_optional:
    :param o_position:
    :param verify_action:
    :return:
    """
    if verify_action == "position":
        pos_change = pi.position_change(
            poco, verify_dsl_str, verify_optional, o_position
        )
        if not pos_change:
            raise PositionNotChangeException(
                "during time={} the position of selector={}"
                " not changed".format(verify_optional["timeout"], verify_dsl_str)
            )
    elif verify_action == "text":
        pos_change = poco_text.text_change(
            poco, verify_dsl_str, verify_optional, o_text
        )
        if not pos_change:
            raise PositionNotChangeException(
                "during time={} the text of selector={} not changed".format(
                    verify_optional["timeout"], verify_dsl_str
                )
            )
    elif verify_action == "appear":
        poco_ele.wait_exists(poco, verify_dsl_str, verify_optional)
    elif verify_action == "disappear":
        poco_ele.wait_disappear(poco, verify_dsl_str, verify_optional)


def air_bdd_click_with_direction(
    poco,
    select_dsl_str,
    target_dsl_str,
    direction,
    screen_size,
    optional=None,
):
    """
    Slides a specified distance up, down, left, or right from a specified
    starting point within a sliding element.
    """
    poco_ele.wait_exists(poco, select_dsl_str, optional)
    poco_object = pm.create_poco_object_by_dsl(poco, select_dsl_str, optional)
    poco_position = poco_object.get_position()

    poco_ele.wait_exists(poco, target_dsl_str, optional)
    target_poco_object = pm.create_poco_object_by_dsl(poco, target_dsl_str, optional)

    flag = False

    target_poco_o = None

    for target_poco_o in target_poco_object:
        target_position = target_poco_o.get_position()

        log.info(
            "click_with_direction: found poco_object: {}, target_poco_object: {}".format(
                poco_position, target_position
            )
        )

        language = g_Context.get_current_language()
        direct_left = lan.parse_glb_str("left", language)
        direct_right = lan.parse_glb_str("right", language)
        direct_up = lan.parse_glb_str("up", language)
        direct_down = lan.parse_glb_str("down", language)

        o_size = poco_object.get_size()

        if direction == direct_left:
            flag = (
                poco_position[0] > target_position[0]
                and abs(poco_position[1] - target_position[1])
                < o_size[1] / 2 / screen_size[1]
            )
        elif direction == direct_right:
            flag = (
                poco_position[0] < target_position[0]
                and abs(poco_position[1] - target_position[1])
                < o_size[1] / 2 / screen_size[1]
            )
        elif direction == direct_up:
            flag = (
                poco_position[1] > target_position[1]
                and abs(poco_position[0] - target_position[0])
                < o_size[0] / 2 / screen_size[0]
            )
        elif direction == direct_down:
            flag = (
                poco_position[1] < target_position[1]
                and abs(poco_position[0] - target_position[0])
                < o_size[0] / 2 / screen_size[0]
            )

        if flag:
            break

    if flag:
        target_poco_o.click()
    else:
        message = "click {} {} {}，not find".format(
            select_dsl_str,
            direction,
            target_dsl_str,
        )
        raise FlybirdNotFoundException(message, {})
