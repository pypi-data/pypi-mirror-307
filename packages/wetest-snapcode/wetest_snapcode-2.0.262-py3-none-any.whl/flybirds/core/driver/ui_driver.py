# -*- coding: utf-8 -*-
"""
ui driver proxy
"""
from flybirds.core.global_context import GlobalContext
import flybirds.core.global_resource as gr


def air_bdd_screen_size(dr_instance):
    return GlobalContext.ui_driver.air_bdd_screen_size(dr_instance)


def init_driver():
    if gr.get_value(f"pocoInstance{gr.get_device_id()}") is not None:
        return gr.get_value(f"pocoInstance{gr.get_device_id()}")
    return GlobalContext.ui_driver.init_driver()


def init_ocr(lang=None):
    if gr.get_value(f"ocrInstance{gr.get_device_id()}") is not None:
        return gr.get_value(f"ocrInstance{gr.get_device_id()}")
    return GlobalContext.ui_driver.init_ocr(lang)


def close_driver():
    return GlobalContext.ui_driver.close_driver()
