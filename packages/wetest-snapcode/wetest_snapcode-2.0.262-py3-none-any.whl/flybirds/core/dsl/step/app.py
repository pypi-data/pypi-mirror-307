# -*- coding: utf-8 -*-
"""
This module defines the steps related to the app.
"""
from behave import step

from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.utils.dsl_helper import ele_wrap, timeout


@step("install app[{selector}]")
@ele_wrap
@timeout
def install_app(context, selector=None):
    g_Context.step.install_app(context, selector)


@step("delete app[{selector}]")
@ele_wrap
@timeout
def uninstall_app(context, selector=None):
    """
    uninstall app
    """
    g_Context.step.uninstall_app(context, selector)


@step("start app[{selector}]")
@ele_wrap
@timeout
def start_app(context, selector=None):
    g_Context.step.start_app(context, selector)


@step("restart app")
@timeout
def restart_app(context):
    g_Context.step.restart_app(context)


@step("restart app[{selector}]")
@timeout
def restart_app(context, selector):
    g_Context.step.restart_app(context, selector)


@step("close app")
@timeout
def stop_app(context):
    g_Context.step.stop_app(context)


@step("close app[{selector}]")
@timeout
def stop_app(context, selector):
    g_Context.step.stop_app(context, selector)


@step("clear app[{selector}]")
@timeout
def clear_app(context, selector=None):
    g_Context.step.clear_app(context, selector)
