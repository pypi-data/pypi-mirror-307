# -*- coding: utf-8 -*-
"""
Poco Element verification
"""
from flybirds.core.global_context import GlobalContext
import flybirds.core.plugin.plugins.default.ui_driver.poco.poco_attr as pa
import flybirds.core.plugin.plugins.default.ui_driver.poco.poco_text as pt
import flybirds.utils.verify_helper as verify_helper
from flybirds.core.exceptions import FlybirdsException


def ele_text_is(
    poco,
    selector_str,
    target_str,
    optional,
    deal_method=None,
    params_deal_module=None,
):
    """
    determine whether the element is the expected value
    """
    ele_str = pt.get_ele_text_replace_space(
        poco, selector_str, optional, deal_method, params_deal_module
    )
    verify_helper.text_equal(target_str, ele_str)


def ele_text_contains(
    poco,
    selector_str,
    target_str,
    optional,
    deal_method=None,
    params_deal_module=None,
):
    """
    determine whether the element contains
    """
    ele_str = pt.get_ele_text_replace_space(
        poco, selector_str, optional, deal_method, params_deal_module
    )
    verify_helper.text_container(target_str, ele_str)


def ele_attr_is(
    poco,
    selector_str,
    optional,
    target_attr,
    target_attr_value,
    deal_method,
    params_deal_module,
):
    """
    determine whether the specified attribute of the element is the expected
    value.
    """
    ele_attr = pa.get_ele_attr(
        poco,
        selector_str,
        optional,
        target_attr,
        deal_method,
        params_deal_module,
    )
    verify_helper.attr_equal(target_attr_value, ele_attr)


def assert_ele(poco, selector_str, optional, operator, target_value):
    """
    determine whether the text attribute of the element is the expected value.
    """
    platform = GlobalContext.platform
    if platform == "android":
        ele_attr = pa.get_ele_attr(poco, selector_str, optional, "text", None, None)
    elif platform == "ios":
        ele_attr = pa.get_ele_attr(poco, selector_str, optional, "label", None, None)
    else:
        raise FlybirdsException(
            f"current platform is {platform}, we only support Android and iOS"
        )
    verify_helper.text_operator(target_value, ele_attr, operator)
