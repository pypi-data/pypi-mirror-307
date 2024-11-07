# -*- coding: utf-8 -*-
"""
This module defines the common steps.
"""

from behave import step

from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.utils.dsl_helper import get_params
from flybirds.utils.dsl_helper import ele_wrap, timeout
import flybirds.core.global_resource as gr


@step("wait[{param}]seconds")
@timeout
def sleep(context, param=None):
    (param_1,) = get_params(context, (param, "param"))
    g_Context.step.sleep(context, param_1)


@step("screenshot")
@timeout
def screenshot(context):
    g_Context.step.screenshot(context)


@step("change ocr lang [{param}]")
@timeout
def change_ocr_lang(context, param=None):
    g_Context.step.change_ocr_lang(context, param)


@step("ocr [{selector}]")
@timeout
def scan(context, selector=None):
    g_Context.step.ocr(context, selector)


@step("ocr")
@timeout
def scan(context):
    g_Context.step.ocr(context)


@step(
    "information association of failed operation," " run the {param1} time :[{param2}]"
)
@timeout
def prev_fail_scenario_relevance(context, param1=None, param2=None):
    param_1, param_2 = get_params(context, (param1, "param1"), (param2, "param2"))
    g_Context.step.prev_fail_scenario_relevance(context, param_1, param_2)


@step("set env {key} {param}")
@ele_wrap
@timeout
def set_env(context, key, param):
    t_env = gr.get_test_envs()
    t_env[key] = param
    gr.set_test_env(t_env)


@step("check env {key} {param}")
@ele_wrap
@timeout
def check_env(context, key, param):
    t_env = gr.get_test_envs()
    if t_env.get(key) is not None:
        cached = t_env[key]
        if t_env[key] != param:
            raise Exception(f"check env{key} failed, cached {cached} != {param} ")
    else:
        raise Exception(f"not found {key}")


@step("can set [{key}]")
@ele_wrap
@timeout
def can_set(context, key):
    g_Context.step.can_set(context, key)


@step("can get [{key}]")
@ele_wrap
@timeout
def can_get(context, key):
    g_Context.step.can_get(context, key)


@step("can stop [{key}]")
@ele_wrap
@timeout
def can_stop(context, key):
    g_Context.step.can_stop(context, key)


@step("DAQ check[{key}]")
@ele_wrap
@timeout
def daq_check(context, key):
    g_Context.step.daq_check(context, key)


@step("PW read[{key}]")
@ele_wrap
@timeout
def pw_read(context, key):
    g_Context.step.pw_read(context, key)


@step("PW write[{key}]")
@ele_wrap
@timeout
def pw_write(context, key):
    g_Context.step.pw_write(context, key)


@step("")
@ele_wrap
@timeout
def placeholder(context):
    pass


@step("index[{key}]")
@ele_wrap
@timeout
def placeholder(context, key):
    set_env(context, "global_step_index", key)


@step("[{key}]次")
@ele_wrap
@timeout
def loop_times(context, key):
    g_Context.step.loop_times(context, key)


@step("attribute assert [{xpath}] text [{operator}] [{key}]")
@ele_wrap
@timeout
def attribute_assert(context, xpath, operator, key):
    g_Context.step.attribute_assert(context, xpath, operator, key)


@step("get [{xpath}] text and save as [{param}]")
@ele_wrap
@timeout
def set_variable(context, xpath, param):
    g_Context.step.set_variable(context, xpath, param)


@step("expression assert [{param}]")
@ele_wrap
@timeout
def expression_assert(context, param):
    g_Context.step.expression_assert(context, param)


@step("save page as [{param}]")
@ele_wrap
@timeout
def set_img_path(context, param):
    g_Context.step.set_img_path(context, param)


@step("image assert [{param}]")
@ele_wrap
@timeout
def img_assert(context, param):
    g_Context.step.img_assert(context, param)


@step("image assert not [{param}]")
@ele_wrap
@timeout
def img_assert_not(context, param):
    g_Context.step.img_assert_not(context, param)


@step("ai icon assert[{name}]")
@ele_wrap
@timeout
def ai_icon_assert(context, name):
    g_Context.step.ai_icon_assert(context, name)


@step("continue monitor")
@ele_wrap
@timeout
def continue_monitor(context):
    gr.set_value("use_detect_error", True)


@step("resume monitor")
@ele_wrap
@timeout
def resume_monitor(context):
    gr.set_value("use_detect_error", False)


@step("var assign[{name}={content}]")
@ele_wrap
@timeout
def var_init(context, name, content):
    g_Context.step.var_init(context, name, content)


@step("var func assign[{name}={func}]")
@ele_wrap
@timeout
def var_random_init(context, name, func):
    g_Context.step.var_func_init(context, name, func)


@step("var operate[{name}.{func}]")
@ele_wrap
@timeout
def var_operate(context, name, func):
    g_Context.step.var_operate(context, name, func)


@step("var fundamental rules")
@ele_wrap
@timeout
def fund_rule(context, name, expression):
    g_Context.step.fund_rule(context, name, expression)
