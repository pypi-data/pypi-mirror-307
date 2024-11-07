# -*- coding: utf-8 -*-
"""
Step implement of element attribute.
"""
import re
import numbers

import flybirds.core.global_resource as gr
from flybirds.core.global_context import GlobalContext
import flybirds.utils.dsl_helper as dsl_helper
import flybirds.core.plugin.plugins.default.ui_driver.poco.poco_attr as pa
from flybirds.core.exceptions import FlybirdsException
from flybirds.core.plugin.plugins.default.step.common import screenshot
from flybirds.core.plugin.plugins.default.step.common import img_verify

import flybirds.utils.flybirds_log as log


def pause_step(context, param=None):
    gr.set_value("pause_step", 1)


def resume_step(context, param=None):
    gr.set_value("pause_step", 0)


def set_variable(context, xpath, param):
    poco_instance = gr.get_value("pocoInstance")

    param_dict = dsl_helper.params_to_dic(xpath)
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

    platform = GlobalContext.platform
    if platform == "android":
        ele_attr = pa.get_ele_attr(
            poco_instance, selector_str, optional, "text", None, None
        )
    elif platform == "ios":
        ele_attr = pa.get_ele_attr(
            poco_instance, selector_str, optional, "label", None, None
        )
    else:
        raise FlybirdsException(
            f"current platform is {platform}, we only support Android and iOS"
        )

    variables = (
        gr.get_value("global_var") if param[0].isupper() else gr.get_value("local_var")
    )
    symbols = "￥， ¥, $, $, €, ￡"
    ele_attr = ele_attr.strip(symbols)
    ele_attr = ele_attr.strip()
    try:
        if isinstance(eval(ele_attr), int) or isinstance(eval(ele_attr), float):
            variables[param] = ele_attr
    except:
        variables[param] = repr(ele_attr)


def var_exist(param):
    variables = (
        gr.get_value("global_var") if param[0].isupper() else gr.get_value("local_var")
    )
    log.info(variables)
    return variables.get(param)


def variable_substitution(param):
    pattern = "[+ \- * / // ( ) > < >= <= == != %]+ | (abs)+"
    vs = filter(None, re.split(pattern, param, flags=re.X))
    for v in vs:
        v = v.strip()
        if not v.isdigit() and not var_exist(v):
            value = "'" + v + "'"
            pattern = "\\b" + v + "\\b"
            param = re.sub(pattern, value, param)
    return param


def expression_assert(param):
    param = variable_substitution(param)
    vs = {**gr.get_value("global_var"), **gr.get_value("local_var")}
    vs_list = vs.copy()
    try:
        if not eval(param, vs):
            raise FlybirdsException(f"{vs_list}, the expression {param} is not true.")
    except Exception as e:
        raise FlybirdsException(f"{param} is invalid expression.\n {e}")


def set_img_path(context, param):
    img_path = screenshot(context)
    image_paths = gr.get_value("image_paths")
    image_paths[param] = img_path


def get_img_path(context, param):
    image_paths = gr.get_value("image_paths")
    if param not in image_paths:
        raise FlybirdsException(f"variable '{param}' referenced before assignment.")
    return image_paths[param]


def img_assert(context, param):
    pre_path = get_img_path(context, param)
    if img_verify(context, pre_path):
        raise FlybirdsException(f"There are no noticeable changes to the page.")


def img_assert_not(context, param):
    pre_path = get_img_path(context, param)
    if not img_verify(context, pre_path):
        raise FlybirdsException(f"There are noticeable changes to the page.")
