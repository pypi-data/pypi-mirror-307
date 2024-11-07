# -*- coding: utf-8 -*-
"""
This module defines the steps related to the page.
"""

from behave import step

from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.utils.dsl_helper import ele_wrap, timeout
from flybirds.utils.dsl_helper import get_params


@step("go to url[{param}]")
@ele_wrap
@timeout
def jump_to_page(context, param=None):
    g_Context.step.jump_to_page(context, param)


@step("set cookie name[{name}] value[{value}] url[{url}]")
@ele_wrap
@timeout
def add_cookie(context, name, value, url):
    g_Context.step.add_cookies(context, name, value, url)


@step("get cookie")
@ele_wrap
@timeout
def get_cookie(context):
    g_Context.step.get_cookie(context)


@step("get local storage")
@ele_wrap
@timeout
def get_local_storage(context):
    g_Context.step.get_local_storage(context)


@step("get session storage")
@ele_wrap
@timeout
def get_session_storage(context):
    g_Context.step.get_session_storage(context)


@step("return to previous page")
@timeout
def return_pre_page(context):
    g_Context.step.return_pre_page(context)


@step("go to home page")
@timeout
def to_app_home(context):
    g_Context.step.to_app_home(context)


@step("logon account[{selector1}]password[{selector2}]")
@ele_wrap
@timeout
def app_login(context, selector1=None, selector2=None):
    g_Context.step.app_login(context, selector1, selector2)


@step("logout")
@timeout
def app_logout(context):
    g_Context.step.app_logout(context)


@step("unblock the current page")
@timeout
def unblock_page(context):
    g_Context.step.unblock_page(context)


@step("current page is [{param}]")
@ele_wrap
@timeout
def cur_page_is(context, param=None):
    g_Context.step.cur_page_is(context, param)


@step("current page is not last page")
@timeout
def has_page_changed(context):
    g_Context.step.has_page_changed(context)
