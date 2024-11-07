# -*- coding: utf-8 -*-
"""
project cli
"""
import os
import tracemalloc
from typing import List, Optional

import typer
from flask import Flask

import flybirds.utils.flybirds_log as log
from flybirds.cli.create_project import create_demo, create_mini, create_car_demo
from flybirds.cli.parse_args import parse_args, default_report_path
from flybirds.cli.server import run_server, run_test
from flybirds.core.launch_cycle.run_manage import run_script
from flybirds.core.server import config

app = typer.Typer(
    help='Welcome to flybirds. Type "--help" for more information.',
    no_args_is_help=True,
)


@app.command("run")
def runner(
    feature_path: str = typer.Option(
        "features",
        "--path",
        "-P",
        help="Feature path that needs " "to be executed",
    ),
    tag: str = typer.Option(
        None,
        "-T",
        "--tag",
        help="Run scenarios with a specific tag. "
        "Multiple scenarios are separated by "
        "commas(,). "
        "e.g. flybirds run --tag tag1,-tag2,tag4",
    ),
    report_format: str = typer.Option(
        "--format=json", "--format", "-F", help="Result format."
    ),
    report_path: str = typer.Option(
        default_report_path,
        "-R",
        "--report",
        help="The path to generate the report.",
    ),
    define: Optional[List[str]] = typer.Option(
        None,
        "-D",
        "--define",
        help="User-defined parameters. e.g. --define headless=false.",
    ),
    rerun: bool = typer.Option(
        None,
        "--rerun/--no-rerun",
        help="Whether the failed scenario needs to be rerun",
    ),
    es: str = typer.Option(None, "--es", help="APP boot environment parameters"),
    to_html: bool = typer.Option(
        True, "--html/--no-html", help="Whether to generate HTML report"
    ),
    run_at: str = typer.Option(
        "local", "--run-at", help="Run environment, extended parameters"
    ),
    server_port: int = typer.Option(
        0, "--port", help="Run as server and listen on port"
    ),
    udt_test_mode: str = typer.Option(
        "udt_test_mode",
        "--udt_test_mode",
        "-M",
        help="udt mode of test",
    ),
    udt_args: str = typer.Option(
        None,
        "--udt_args",
        help="udt args for test",
    ),
    processes: int = typer.Option(
        4,
        "--processes",
        "-p",
        help="Maximum number of processes. Default = 4. Effective when  "
        "test on web.",
    ),
):
    """
    Run the project.
    """
    tracemalloc.start()

    if server_port > 0:
        run_server(
            server_port,
            feature_path,
            tag,
            report_format,
            report_path,
            define,
            rerun,
            es,
            to_html,
            run_at,
            processes,
        )
    else:
        if udt_test_mode == "docker":
            run_test(
                udt_args,
                tag,
                report_format,
                report_path,
                define,
                rerun,
                es,
                to_html,
                run_at,
                processes,
            )
        else:
            run_args = parse_args(
                feature_path,
                tag,
                report_format,
                report_path,
                define,
                rerun,
                es,
                to_html,
                run_at,
                processes,
            )
            log.info("============last run_args: {}".format(str(run_args)))
            run_script(run_args)


@app.command("create")
def create_project(
    mini: bool = typer.Option(
        None,
        "--mini",
        "-M",
        help="create mini project",
    ),
    car: bool = typer.Option(
        None,
        "--car",
        "-C",
        help="create car project",
    ),
):
    """
    Generate project example
    """
    if mini is not None:
        create_mini()
    if car is not None:
        create_car_demo()
    else:
        create_demo()


@app.command("init")
def init_device(
    device_id: str = typer.Option(
        None,
        "--device_id",
        "-d",
        help="create mini project",
    ),
):
    """
    Init device
    """
    update_device_state(device_id, "init")


@app.command("uninit")
def uninit_device(
    device_id: str = typer.Option(
        None,
        "--device_id",
        "-d",
        help="create mini project",
    ),
):
    """
    Uninit device
    """
    update_device_state(device_id, "uninit")


def update_device_state(device_id, state):
    from flybirds.core.server.client import TestClient

    ip, port = get_server_port(device_id)
    udtBirds = TestClient(ip, port)
    print("connecting to udt birds server: http://" + ip + ":" + str(port))
    if udtBirds.wait_ready():
        print("connected to udt birds server")
        print("prepare to connecting {}".format(device_id))
        ret = None
        if state == "init":
            ret = udtBirds.init_device(device_id)
        elif state == "uninit":
            ret = udtBirds.uninit_device(device_id)
        print(f"result to {state} device {ret}")
    else:
        print("udt birds server not ready")


def get_server_port(device_id):
    from flybirds.core.server.client import AssistdClient

    ip = os.environ.get("UDT_CAR_LOCAL_SERVER_IP", "127.0.0.1")
    port = os.environ.get("UDT_CAR_LOCAL_SERVER_PORT")

    if config.is_desktop_mode():
        host = config.get_assistd_host()
        if host is not None:
            assist_client = AssistdClient(host)
            assist_client.wait_ready()
            assistd_port = assist_client.get_port(device_id)
            print("get port from assistd", assistd_port)
            if assistd_port > 0:
                port = assistd_port

    return ip, port


if __name__ == "__main__":
    app()
