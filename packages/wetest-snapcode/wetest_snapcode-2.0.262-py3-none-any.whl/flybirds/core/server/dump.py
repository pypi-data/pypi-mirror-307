# -*- coding: utf-8 -*-
"""
dump scenario state
"""
import json


class ScenarioState:
    """
    state of scenario
    """

    def __init__(self):
        self.current_scenario = "None"
        self.current_step = None
        self.step_index = None
        self.step_status = None
        self.step_process = {}
        self.end_ts = None
        self.start_ts = None

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__ if hasattr(o, "__dict__") else repr(o),
            indent=4,
        )


class StepState:
    """
    state of scenario
    """

    def __init__(self):
        self.name = None
        self.step_index = None
        self.status = None
        self.screen_cut = []
        self.end_ts = None
        self.start_ts = None
        self.desc = None
        self.log = None
        self.variables = None

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
