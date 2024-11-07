# -*- coding: utf-8 -*-
"""
Utils
"""
from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.utils import language_helper as lan


def ignore_env_step(name):
    language = g_Context.get_current_language()
    if lan.parse_glb_str("set_env", language) in name:
        return True

    return False
