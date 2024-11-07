# -*- coding: utf-8 -*-
"""
android Element core api implement
"""

from flybirds.core.plugin.plugins.default.base_element import BaseElement

__open__ = ["Element"]


class Element(BaseElement):
    """Android Element Class"""

    name = "android_element"

    def ui_driver_init(self, device=None):
        """
        Initialize the poco object
         :return:
        """
        from flybirds_poco.drivers.android.uiautomation import AndroidUiautomationPoco
        from flybirds_poco.drivers.android.uiautomation import PocoServicePackage

        poco = AndroidUiautomationPoco(
            device=device,
            force_restart=True,
            use_airtest_input=True, screenshot_each_action=False
        )
        poco.device.adb.raw_shell(f"dumpsys deviceidle  whitelist +{PocoServicePackage}")
        if poco.device.sdk_version >= 24:
            poco.device.adb.raw_shell(f"cmd appops set {PocoServicePackage} RUN_IN_BACKGROUND allow")
        return poco
