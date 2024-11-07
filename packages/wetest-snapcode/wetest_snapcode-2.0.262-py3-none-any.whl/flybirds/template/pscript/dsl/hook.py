# -*- coding: utf-8 -*-
"""
The expansion of each hook function during the execution of flybirds
"""
import os
import time
import json
import tracemalloc

import flybirds
from behave.model_core import Status

from flybirds.core.server import config
from flybirds.core.server.dump import ScenarioState as ss
from flybirds.core.server.dump import StepState as step_state

import flybirds.core.global_resource as gr
import flybirds.utils.flybirds_log as log
from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.core.server.utils import ignore_env_step
from flybirds.utils import file_helper
from flybirds.utils.cos_helper import cos_client
from flybirds.core.plugin.plugins.default.step.common import screenshot
from flybirds.utils.http_helper import HttpUdt


def before_all_extend(context):
    current_scenario = ss()
    current_scenario.start_ts = int(round(time.time() * 1000))
    gr.set_value("current_scenario", current_scenario)
    gr.set_value("local_var", {})
    gr.set_value("global_var", {})


def after_all_extend(context):
    current_scenario = gr.get_value("current_scenario")
    current_scenario.end_ts = int(round(time.time() * 1000))
    gr.set_value("current_scenario", current_scenario)


def before_feature_extend(context, feature):
    pass


def after_feature_extend(context, feature):
    pass


def before_scenario_extend(context, scenario):
    state = gr.get_value("current_scenario")
    state.current_scenario = scenario.name
    gr.set_value("current_scenario", state)
    gr.set_value("image_paths", {})
    gr.set_value("use_detect_error", False)


def on_scenario_fail(context, scenario):
    state = gr.get_value("current_scenario")
    state.current_scenario = scenario.name
    for step in scenario.all_steps:
        if ignore_env_step(step.name):
            continue

        if step.status in (Status.failed, Status.undefined) and step.step_type not in (
            "IF",
            "ELIF",
        ):
            state.current_step = step.name
            state.step_status = step.status.name
            # if step.exception is not None:
            #     state.step_exception = step.exception.args[0]
    gr.set_value("current_scenario", state)


def on_scenario_success(context, scenario):
    ss = gr.get_value("current_scenario")
    ss.current_scenario = scenario.name
    gr.set_value("current_scenario", ss)


def after_scenario_extend(context, scenario):
    snapshot = tracemalloc.take_snapshot()
    # snapshot = snapshot.filter_traces(
    #     (
    #         tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
    #         tracemalloc.Filter(False, "<frozen importlib._bootstrap_external>"),
    #         tracemalloc.Filter(False, "<unknown>"),
    #     )
    # )
    top_stats = snapshot.statistics("lineno")
    log.info("[ Top 10 ]")
    for stat in top_stats[:10]:
        log.info(stat)


def before_step_extend(context, step):
    if gr.get_value("aborted") == 1:
        raise flybirds.core.exceptions.FlybirdsException("ABORTED: By user")

    if ignore_env_step(step.name):
        print("udt: ignore set condition step " + step.name)
        return

    st = step_state()
    st.start_ts = int(round(time.time() * 1000))
    gr.set_value("current_step", st)
    gr.set_value("log_capture", None)

    ss = gr.get_value("current_scenario")
    ss.current_step = step.name
    ss.step_index = gr.get_test_env_value("global_step_index")
    gr.set_value("current_scenario", ss)


def after_step_extend(context, step):
    if gr.get_value("aborted") == 1:
        raise flybirds.core.exceptions.FlybirdsException("ABORTED: By user")

    if ignore_env_step(step.name):
        print("udt: ignore set condition step " + step.name)
        return

    packageName = gr.get_value("packageName")
    while gr.get_value("pause_step") == 1:
        print("udt: pause_step: ", step)
        time.sleep(1)

    print(
        "udt: after_step_extend: ",
        step,
        packageName,
        step,
        gr.get_test_env_value("global_step_index"),
    )

    st = gr.get_value("current_step")
    st.name = step.name
    st.end_ts = int(round(time.time() * 1000))
    st.step_index = gr.get_test_env_value("global_step_index")
    st.status = step.status.name
    if step.status in (Status.failed, Status.undefined):
        if log := gr.get_value("log_capture"):
            st.log = json.dumps(log)
        if step.exception is not None:
            if hasattr(step.exception, "message"):
                st.desc = step.exception.message
            elif hasattr(step.exception, "args"):
                st.desc = step.exception.args
            else:
                st.desc = str(step.exception)

    if step.status == Status.passed:
        log = gr.get_value("log_capture")
        st.log = json.dumps(log)

    try:
        local_screen_path = screenshot(context)
        screen_path = HttpUdt.upload_file(local_screen_path)
        st.screen_cut.append(screen_path)
        print(f"udt: upload success : {screen_path}")
    except Exception as e:
        print(f"udt: upload failed : {e}")

    ss = gr.get_value("current_scenario")
    ss.current_step = st.name
    ss.step_index = st.step_index
    ss.step_status = st.status
    ss.step_process[gr.get_test_env_value("global_step_index")] = st
    gr.set_value("current_scenario", ss)


def before_tag_extend(context, tag):
    pass


def after_tag_extend(context, tag):
    pass
