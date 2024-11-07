# -*- coding: utf-8 -*-
"""
app base step class
"""
import flybirds.core.plugin.plugins.default.step.action as step_action
import flybirds.core.plugin.plugins.default.step.app as step_app
import flybirds.core.plugin.plugins.default.step.attr as step_attr
import flybirds.core.plugin.plugins.default.step.click as step_click
import flybirds.core.plugin.plugins.default.step.common as step_common
import flybirds.core.plugin.plugins.default.step.page_show_adjust as step_adjust
import flybirds.core.plugin.plugins.default.step.record as step_record
import flybirds.core.plugin.plugins.default.step.swipe as step_swipe
import flybirds.core.plugin.plugins.default.step.verify as step_verify
import flybirds.core.plugin.plugins.default.step.variables as step_variables
from flybirds.core.plugin.plugins.default.step.app import (
    to_app_home,
    app_login,
    app_logout,
)
from flybirds.core.plugin.plugins.default.step.input import (
    only_input,
    ele_input,
    ocr_text_input,
)
from flybirds.core.plugin.plugins.default.step.position import position_not_change
from flybirds.core.plugin.plugins.default.car_driver.car_interface import CarProtocol


class AppBaseStep:
    """APP Base Step Class"""

    name = "app_base_step"

    def init_device(self, context, param=None):
        step_app.init_device(context, param)

    def change_ocr_lang(self, context, param=None):
        step_common.change_ocr_lang(context, lang=param)

    def img_exist(self, context, param):
        step_verify.img_exist(context, param)

    def img_not_exist(self, context, param):
        step_verify.img_not_exist(context, param)

    def connect_device(self, context, param):
        step_app.connect_device(context, param)

    def set_cur_device(self, context, param):
        step_app.set_cur_device(context, param)

    def start_app(self, context, param):
        step_app.start_app(context, param)

    def restart_app(self, context, param=None):
        step_app.restart_app(context, param)

    def clear_app(self, context, param):
        step_app.clear_app(context, param)

    def stop_app(self, context, param=None):
        step_app.stop_app(context, param)

    def text_attr_equal(self, context, selector, param2, param3):
        step_attr.text_attr_equal(context, selector, param2, param3)

    def ele_attr_equal(self, context, selector, param2, param3):
        step_attr.ele_attr_equal(context, selector, param2, param3)

    def click_ele(self, context, selector, click_action=None):
        selector = step_click.init_click_action_selector(selector, click_action)
        step_click.click_ele(context, selector)

    def ai_icon_click(self, context, name):
        step_click.ai_icon_click(context, name)

    def click_text(self, context, selector, click_action=None):
        selector = step_click.init_click_action_selector(selector, click_action)
        step_click.click_text(context, selector)

    def click_coordinates(self, context, x, y, click_action=None):
        selector = step_click.init_click_action_selector(
            "click_coordinates", click_action
        )
        step_click.click_coordinates(context, x, y, selector)

    def click_coordinates_pos(self, context, pos):
        step_click.click_coordinates_pos(context, pos)

    def click_ocr_text(self, context, selector, click_action=None):
        selector = step_click.init_click_action_selector(selector, click_action)
        step_click.click_ocr_text(context, selector)

    def click_regional_ocr_text(self, context, selector, param2, click_action=None):
        selector = step_click.init_click_action_selector(selector, click_action)
        step_click.click_regional_ocr_text(context, selector, param2)

    def click_regional_ocr(self, context, selector, click_action=None):
        selector = step_click.init_click_action_selector(selector, click_action)
        step_click.click_regional_ocr(context, selector)

    def click_image(self, context, selector, click_action=None):
        selector = step_click.init_click_action_selector(selector, click_action)
        step_click.click_image(context, selector)

    def sleep(self, context, param):
        step_common.sleep(context, param)

    def screenshot(self, context):
        step_common.screenshot(context)

    def ocr(self, context, param=None):
        step_common.ocr(context, param)

    def prev_fail_scenario_relevance(self, context, param1, param2):
        step_common.prev_fail_scenario_relevance(context, param1, param2)

    def only_input(self, context, param1):
        only_input(context, param1)

    def ele_input(self, context, selector, param2):
        ele_input(context, selector, param2)

    def ocr_text_input(self, context, selector, param2):
        ocr_text_input(context, selector, param2)

    def swipe_to_ele(self, context, p_selector, param2, c_selector):
        step_adjust.swipe_to_ele(context, p_selector, param2, c_selector)

    def full_screen_swipe_to_ele_aaa(self, context, param1, selector):
        step_adjust.full_screen_swipe_to_ele_aaa(context, param1, selector)

    def full_screen_swipe_to_ocr_txt(self, context, param1, selector):
        step_adjust.full_screen_swipe_to_ocr_txt(context, param1, selector)

    def full_screen_swipe_to_img(self, context, param1, selector):
        step_adjust.full_screen_swipe_to_img(context, param1, selector)

    def position_not_change(self, context, selector, param2):
        position_not_change(context, selector, param2)

    def start_screen_record_timeout(self, context, param):
        step_record.start_screen_record_timeout(context, param)

    def start_screen_record(self, context):
        step_record.start_screen_record(context)

    def stop_screen_record(self, context):
        step_record.stop_screen_record(context)

    def ele_swipe(self, context, selector, param2, param3):
        step_swipe.ele_swipe(context, selector, param2, param3)

    def img_swipe(self, context, selector, param2, param3):
        step_swipe.img_swipe(context, selector, param2, param3)

    def full_screen_swipe(self, context, param1, param2):
        step_swipe.full_screen_swipe(context, param1, param2)

    def ele_drag(self, context, param1, param2):
        step_swipe.ele_drag(context, param1, param2)

    def coord_swipe(self, context, param1, param2):
        step_swipe.coord_swipe(context, param1, param2)

    def wait_text_exist(self, context, selector):
        step_verify.wait_text_exist(context, selector)

    def ocr_text_exist(self, context, selector):
        step_verify.ocr_txt_exist(context, selector)

    def ocr_regional_text_exist(self, context, selector, param2):
        step_verify.ocr_regional_txt_exist(context, selector, param2)

    def ocr_text_contain(self, context, selector):
        step_verify.ocr_txt_contain(context, selector)

    def ocr_regional_text_contain(self, context, selector, param2):
        step_verify.ocr_regional_txt_contain(context, selector, param2)

    def ocr_text_not_exist(self, context, selector):
        step_verify.ocr_txt_not_exist(context, selector)

    def text_not_exist(self, context, selector):
        step_verify.text_not_exist(context, selector)

    def wait_text_disappear(self, context, selector):
        step_verify.wait_text_disappear(context, selector)

    def wait_ele_exit(self, context, selector):
        step_verify.wait_ele_exit(context, selector)

    def ele_not_exit(self, context, selector):
        step_verify.ele_not_exit(context, selector)

    def wait_ele_disappear(self, context, selector):
        step_verify.wait_ele_disappear(context, selector)

    def wait_ocr_text_appear(self, context, param):
        step_verify.wait_ocr_text_appear(context, param)

    def ele_text_equal(self, context, selector, param2):
        step_verify.ele_text_equal(context, selector, param2)

    def ele_text_container(self, context, selector, param2):
        step_verify.ele_text_container(context, selector, param2)

    def wait_ele_appear(self, context, selector):
        step_verify.wait_ele_appear(context, selector)

    def exist_ele(self, context, selector):
        step_verify.exist_ele(context, selector)

    def to_app_home(self, context):
        to_app_home(context)

    def app_login(self, context, param1, param2):
        app_login(context, param1, param2)

    def app_logout(self, context):
        app_logout(context)

    def current_app(self):
        step_app.current_app()

    def to_device_home(self, context):
        step_app.to_device_home(context)

    def click_to_ele_with_direction(self, context, param1, param2, direction):
        # step_click.click_to_ele_with_direction(context, param1, param2, direction)
        step_click.click_with_direction(
            context, param1, param2, direction, "poco", "poco"
        )

    def click_to_image_with_direction(self, context, param1, param2, direction):
        step_click.click_with_direction(
            context, param1, param2, direction, "image", "image"
        )

    def click_to_ocr_with_direction(self, context, param1, param2, direction):
        step_click.click_with_direction(
            context, param1, param2, direction, "ocr", "ocr"
        )

    def click_to_img_ocr_with_direction(self, context, param1, param2, direction):
        step_click.click_with_direction(
            context, param1, param2, direction, "image", "ocr"
        )

    def click_to_ocr_img_with_direction(self, context, param1, param2, direction):
        step_click.click_with_direction(
            context, param1, param2, direction, "ocr", "image"
        )

    def click_to_img_ele_with_direction(self, context, param1, param2, direction):
        step_click.click_with_direction(
            context, param1, param2, direction, "image", "poco"
        )

    def click_to_ele_img_with_direction(self, context, param1, param2, direction):
        step_click.click_with_direction(
            context, param1, param2, direction, "poco", "image"
        )

    def click_to_ocr_ele_with_direction(self, context, param1, param2, direction):
        step_click.click_with_direction(
            context, param1, param2, direction, "ocr", "poco"
        )

    def click_to_ele_ocr_with_direction(self, context, param1, param2, direction):
        step_click.click_with_direction(
            context, param1, param2, direction, "poco", "ocr"
        )

    def can_set(self, context, key):
        CarProtocol.control_can(key, "set")

    def can_get(self, context, key):
        CarProtocol.control_can(key, "get")

    def can_stop(self, context, key):
        CarProtocol.control_can(key, "stop")

    def daq_check(self, context, key):
        CarProtocol.control_daq(key)

    def pw_read(self, context, key):
        CarProtocol.control_pw(key, "read")

    def pw_write(self, context, key):
        CarProtocol.control_pw(key, "write")

    def loop_times(self, context, param):
        step_common.loop_times(context, param)

    def attribute_assert(self, context, xpath, operator, key):
        step_attr.attribute_assert(context, xpath, operator, key)

    def set_variable(self, context, xpath, param):
        step_action.set_variable(context, xpath, param)

    def expression_assert(self, context, param):
        step_action.expression_assert(param)

    def set_img_path(self, context, param):
        step_action.set_img_path(context, param)

    def img_assert(self, context, param):
        step_action.img_assert(context, param)

    def img_assert_not(self, context, param):
        step_action.img_assert_not(context, param)

    def ai_icon_assert(self, context, name):
        step_click.ai_icon_exist(context, name)

    def var_init(self, context, name, content):
        step_variables.var_init(name, content)

    def var_func_init(self, context, name, func):
        step_variables.func_var(context, name, func)

    def var_operate(self, context, name, func):
        step_variables.var_operate(name, func)

    def fund_rule(self, context, name, expression):
        step_variables.fundamental_rule(name, expression)
