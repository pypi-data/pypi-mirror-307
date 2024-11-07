# -*- coding: utf-8 -*-
"""
android device core api implement.
"""
from flybirds_airtest.core.api import (connect_device, set_current, device, shell)

__open__ = ["Device"]

class Device:
    """Android Device Class"""

    name = "android_device"

    def device_connect(self, device_id):
        """
        Initialize device with uri, and set as current device.
        """
        dev = connect_device("Android:///" + device_id)
        return dev

    def set_cur_device(self, device_id):
        """
        Initialize device with uri, and set as current device.
        """
        dev = set_current(device_id)
        return dev


    def device_disconnect(self, device_id):
        """
        Initialize device with uri, and set as current device.
        """
        device().disconnect()

    def use_shell(self, cmd):
        """
        Start remote shell in the target device and execute the command
        :platforms: Android
        """
        return shell(cmd)
