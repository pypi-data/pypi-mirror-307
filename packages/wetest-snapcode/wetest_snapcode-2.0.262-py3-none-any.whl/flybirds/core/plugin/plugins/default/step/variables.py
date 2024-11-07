# -*- coding: utf-8 -*-
"""
Step implement of local and global variables.
"""
import numbers
import re
import string
import random
import datetime

from flybirds_airtest.core.android.adb import ADB
import flybirds.core.global_resource as gr
import flybirds.utils.flybirds_log as log
from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.core.exceptions import FlybirdsException
from flybirds.core.plugin.plugins.default.step.action import variable_substitution
from flybirds.core.plugin.plugins.default.step.common import ocr
from flybirds.core.plugin.plugins.default.step.verify import paddle_fix_txt


def var_init(name, content):
    local_var = gr.get_value("local_var")
    global_var = gr.get_value("global_var")

    if name[0].isupper():
        global_var.update({name: content})
    else:
        local_var.update({name: content})
    gr.set_value(
        "log_capture", {"local variables": local_var, "global varibales": global_var}
    )
    log.info(f"local variables: {local_var}, global varibales: {global_var}")


def func_var(context, name, raw_func):
    func, *args = filter(None, re.split(r"[(,=)]", raw_func))

    if func == "randint":
        args = list(map(int, args))
        content = random.randint(args[0], args[1])
    elif func == "randletter":
        args = list(map(int, args))
        content = random.sample(string.ascii_letters, args[0])
        content = "".join(content)
    elif func == "randchar":
        args = list(map(int, args))
        content = ""
        for _ in range(args[0]):
            # GBK2313
            head = random.randint(0xB0, 0xF7)
            body = random.randint(0xA1, 0xFE)
            val = f"{head:x} {body:x}"
            content += bytes.fromhex(val).decode("gb2312")
    elif func == "len":
        temp = var_content(args[0])
        content = len(temp)
    elif func == "cropText":
        region = list(map(float, args))
        content = ocr_regional_txt_by_coord(context, region)
    elif func == "time":
        content = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    elif func == "adb":
        device_id = gr.get_device_id()
        dev = ADB(device_id)
        cmd = args[0]
        assert cmd.startswith("adb"), "only support adb statement"
        cmd = cmd.strip("adb")
        content = dev.cmd(cmd)
    else:
        raise FlybirdsException(f"{func} method is undefined.")
    var_init(name, content)


def var_content(name):
    local_var = gr.get_value("local_var")
    global_var = gr.get_value("global_var")

    try:
        old_content = global_var[name] if name[0].isupper() else local_var[name]
    except Exception as e:
        raise FlybirdsException(f"{name} referenced before assignments, {e}")
    else:
        return old_content


def var_operate(name, raw_func):
    old_content = var_content(name)

    func, *args = filter(None, re.split(r"[(, )]", raw_func))

    if isinstance(old_content, numbers.Number):
        if func == "digit2str":
            new_content = str(old_content)
        else:
            raise FlybirdsException(f"[{name}: {old_content}] type is number.")
    elif isinstance(old_content, str):
        if func == "substr":
            start, end = map(int, args)
            try:
                new_content = old_content[start:end]
            except Exception as e:
                raise FlybirdsException(f"{raw_func} error: {e}")
        elif func == "index_replace":
            index, s = map(lambda x: x.strip(), args)
            old_content = list(old_content)
            try:
                old_content[int(index)] = s
            except Exception as e:
                raise FlybirdsException(f"{raw_func} error: {e}")
            new_content = "".join(old_content)
        elif func == "re_replace":
            # when re contain "()"
            pattern = re.search("\(.+,", raw_func)
            pattern = pattern.group()[1:-1].split()[0]
            s = re.search(",.+\)", raw_func)
            s = s.group()[1:-1].split()[0]
            try:
                new_content = re.sub(pattern, s, old_content)
            except Exception as e:
                raise FlybirdsException(f"{raw_func} error: {e}")
        elif func == "str2digit":
            old_content = old_content.strip()
            if not re.match("-?\d+(\.\d+)?", old_content):
                raise FlybirdsException(f"{name}: {old_content} is not digits.")
            old_content = old_content.lstrip("0")
            new_content = eval(old_content)
        elif func == "concat":
            s = var_content(args[0])
            if len(args) == 1:
                hyphen = ""
            elif args[1].isdigit():
                hyphen = " " * int(args[1])
            else:
                hyphen = args[1]
            new_content = hyphen.join((old_content, s))
        else:
            raise FlybirdsException(f"[{name}: {old_content}] type is string.")
    else:
        raise FlybirdsException(f"[{name}: {old_content}] type must be str or number.")

    var_init(name, new_content)


def fundamental_rule(name, expression):
    content = variable_substitution(expression)
    vs = {**gr.get_value("global_var"), **gr.get_value("local_var")}
    content = eval(content, vs)
    var_init(name, content)


def ocr_regional_txt_by_coord(context, region):
    ocr(context, region=region)

    for line in g_Context.ocr_result:
        txt = line[1][0]
        fixed_txt = paddle_fix_txt(txt)
        log.info(f"ocr txt got: {fixed_txt}")
        return fixed_txt
    else:
        raise FlybirdsException(f"there is no txt in {region}.")
