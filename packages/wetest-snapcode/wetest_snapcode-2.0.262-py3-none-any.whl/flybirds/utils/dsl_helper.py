# -*- coding: utf-8 -*-
"""
dsl helper
"""
import base64
import sys
import re
from functools import wraps
import ctypes
from threading import Thread

import flybirds.core.global_resource as gr
import flybirds.utils.flybirds_log as log
from flybirds.core.exceptions import FlybirdsTimeoutException


# generate result_dic
def add_res_dic(dsl_params, functin_pattern, def_key):
    result_dic = {}
    match_obj = re.match(functin_pattern, dsl_params)
    if match_obj is not None:
        """
        senario：

        Flight, verifyEle=center_content_layout, verifyAction=position
        textMatches=shanghai.?
        .?economic.?, fuzzyMatch=true
        text=freshmode, timeout=15, swipeCount=40


        multi properities，example：text=freshmode, timeout=15, swipeCount=40
        Match from back to front, match back first,swipeCount=40
        match_obj_group_1（text=freshmode, timeout=15）
        f the conditions are still met, split again, Until the split to the
        last item: text=
        """
        group_1 = match_obj.group(1).strip().replace("\u200b", "")
        result_dic[match_obj.group(2)] = match_obj.group(3)
        match_obj_group_1 = re.match(functin_pattern, group_1)

        while match_obj_group_1 is not None:
            match_obj_group_1 = re.match(functin_pattern, group_1)
            if match_obj_group_1 is not None:
                group_1 = match_obj_group_1.group(1).strip().replace("\u200b", "")
                result_dic[match_obj_group_1.group(2)] = match_obj_group_1.group(3)
            else:
                result_dic[def_key] = group_1
                break
        else:
            result_dic[def_key] = group_1

    else:
        result_dic[def_key] = dsl_params.strip().replace("\u200b", "")
    # print('result_dic44444', result_dic)
    return result_dic


# generate result_dic
def params_to_dic(dsl_params, def_key="selector"):
    """
    Convert the parameters in the dsl statement into dict format for use in
    subsequent processes
    """
    result_dic = {}
    functin_pattern = re.compile(r"([\S\s]+),\s*([a-zA-Z0-9_]+)\s*=\s*(\S+)")
    if isinstance(dsl_params, str):
        result_dic = add_res_dic(dsl_params, functin_pattern, def_key)
    log.info("result_dic: {}".format(result_dic))
    return result_dic


def split_must_param(dsl_params):
    """
    Get must and optional parameters
    """
    result = dsl_params.split(",", 1)
    result[0] = result[0].strip().replace("\u200b", "")
    result[1] = result[1].strip().replace("\u200b", "")
    return result


def get_params(context, *args):
    """
    Get param from context
    :param context: step context
    :param args: A tuple containing value and parameter name
    :return:
    """
    items = []
    for val, param_name in args:
        if val is not None:
            items.append(replace_str(val))
        elif hasattr(context, param_name):
            items.append(replace_str(getattr(context, param_name)))
    return items


def return_value(value, def_value=None):
    """
    get global attribute value
    """
    if value is not None:
        return value
    return def_value


def is_number(s):
    """
    Determine if the parameter is a number
    """
    try:
        float(s)
        return True
    except ValueError:
        log.error(f"param {s} is not a number!")
    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        log.error(f"param {s} cannot turn to a number!")
    return False


def replace_str(u_text):
    return u_text.strip().replace(u"\u200b", "")


def handle_str(un_handle_str):
    res = re.match(r"([\S\s]+),\s*[0-9_]+\s*", un_handle_str)
    if res is not None:
        return res.group(1)
    else:
        return un_handle_str


def str2bool(v):
    return v.lower() in [
        "true",
        "1",
        "t",
        "y",
        "yes",
        "yeah",
        "yup",
        "certainly",
        "uh-huh",
    ]


def get_use_define_param(context, param_name):
    use_define = context.get("use_define")
    log.info(f"use_define: {use_define}")
    params = [i for i in use_define if param_name + "=" in i]
    user_data = {}
    if len(params) > 0:
        if len(params) > 1:
            log.error(
                f"Cannot customize multiple parameters with the same " f"name:{params}"
            )
        value = params[0].split("=", 1)[1]
        user_data[param_name] = str(base64.b64decode(value), "utf-8")
    return user_data


def ele_wrap(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        context = args[0]
        for k, v in kwargs.items():
            if v is None:
                if hasattr(context, k):
                    v = getattr(context, k)
                else:
                    log.warn(f"[ele_wrap] step param:[{k}] is none.")
                    continue
            v = replace_str(v)
            if "selector" in k:
                selector_str = v
                ele_key = v.split(",")[0]
                ele_value = gr.get_ele_locator(ele_key)
                v = selector_str.replace(ele_key, ele_value, 1)
            new_v = get_global_value(v)
            if new_v is not None:
                v = new_v
            kwargs[k] = v
        func(*args, **kwargs)
        # Do something after the function.

    return wrapper_func


# https://zhuanlan.zhihu.com/p/390143037
class ThreadKiller(Thread):
    """separate thread to kill TerminableThread"""

    def __init__(self, target_thread, exception_cls, repeat_sec=2.0):
        Thread.__init__(self)
        self.target_thread = target_thread
        self.exception_cls = exception_cls
        self.repeat_sec = repeat_sec
        self.daemon = True

    def run(self):
        """loop raising exception incase thread doesn't be killed"""
        while self.target_thread.is_alive():
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(self.target_thread.ident),
                ctypes.py_object(self.exception_cls),
            )
            self.target_thread.join(self.repeat_sec)


class TerminableThread(Thread):
    """a thread that can be stopped by forcing an exception in the execution context"""

    def terminate(self, exception_cls, repeat_sec=2.0):
        if not self.is_alive():
            return True
        killer = ThreadKiller(self, exception_cls, repeat_sec=repeat_sec)
        killer.start()


def timeout(func):
    """
    timeout decorator
    :param sec: function raise TimeoutError after ? seconds
    :param raise_sec: retry kill thread per ? seconds
        default: 1 second
    """

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        raise_sec = 1
        for k in kwargs.values():
            if tmp := re.search("timeout=[0-9]+\.?[0-9]*", k):
                tmp = tmp.group().split("timeout=")[-1]
                sec = float(tmp)
                break
        else:
            sec = 35  # default
        err_msg = f"Function {func.__name__} timed out after {sec} seconds"

        """
        signal only works in main thread
        """
        # if sys.platform != "win32":
        #     import signal

        #     def _handle_timeout(signum, frame):
        #         raise FlybirdsTimeoutException(err_msg)

        #     signal.signal(signal.SIGALRM, _handle_timeout)
        #     signal.alarm(sec)
        #     try:
        #         result = func(*args, **kwargs)
        #     finally:
        #         signal.alarm(0)
        #     return result

        # else:

        result, exception = [], []

        def run_func():
            try:
                res = func(*args, **kwargs)
            except FlybirdsTimeoutException:
                pass
            except Exception as e:
                exception.append(e)
            else:
                result.append(res)

        # typically, a python thread cannot be terminated, use TerminableThread instead
        thread = TerminableThread(target=run_func, daemon=True)
        thread.start()
        thread.join(timeout=sec)

        if thread.is_alive():
            # a timeout thread keeps alive after join method, terminate and raise TimeoutError
            # exc = type('TimeoutError', FuncTimeoutError.__bases__, dict(FuncTimeoutError.__dict__))
            thread.terminate(
                exception_cls=FlybirdsTimeoutException, repeat_sec=raise_sec
            )
            raise FlybirdsTimeoutException(err_msg)
        elif exception:
            # if exception occurs during the thread running, raise it
            raise exception[0]
        else:
            # if the thread successfully finished, return its results
            return result[0]

    return wrapped_func


def get_global_value(v):
    projectScript = gr.get_value("projectScript")
    if projectScript is not None:
        if hasattr(projectScript, "custom_operation"):
            custom_operation = projectScript.custom_operation
            if custom_operation is not None and hasattr(
                custom_operation, "get_global_value"
            ):
                rp = custom_operation.get_global_value(v)
                if rp is not None:
                    return rp
        elif hasattr(projectScript, "app_operation"):
            app_operation = projectScript.app_operation
            if app_operation is not None and hasattr(app_operation, "get_global_value"):
                rp = app_operation.get_global_value(v)
                if rp is not None:
                    return rp
    return None
