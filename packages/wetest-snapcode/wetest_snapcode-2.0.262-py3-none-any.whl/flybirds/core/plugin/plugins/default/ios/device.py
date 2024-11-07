# -*- coding: utf-8 -*-
"""
ios device core api implement.
"""
import time
import re
from tidevice import Device as t_device
from tidevice._wdaproxy import WDAService
from flybirds_airtest.core.api import connect_device, device, set_current
from flybirds.utils.flybirds_log import logger
from flybirds.core.global_context import GlobalContext

__open__ = ["Device"]


class Device:
    """IOS App Class"""

    name = "ios_device"

    def device_connect(self, device_id):
        """
        Initialize device with uri, and set as current device.
        """

        if GlobalContext.connector is not None:
            return GlobalContext.connector.connect(device_id, 60)
        else:
            return PC.static_connect(device_id)

    def device_disconnect(self, device_id):
        """
        Initialize device with uri, and set as current device.
        """
        if GlobalContext.connector:
            GlobalContext.connector.close()
        else:
            device().disconnect()

    def set_cur_device(self, device_id):
        """
        Initialize device with uri, and set as current device.
        """
        if GlobalContext.connector is not None:
            return GlobalContext.connector.set_current(device_id, 60)
        else:
            return PC.static_set_current(device_id, 60)

    def pc_init(self, device_id, test_driver, timeout=50):
        """
        please not call multi times
        """

        if GlobalContext.connector is None:
            return PC(device_id, test_driver, timeout)
        else:
            logger.info("already init connector")
            return GlobalContext.connector


class PC:
    """
    pc connector mac windows
    """

    def __init__(self, device_id, test_driver, timeout):
        self.process = None
        self.replay = None
        try:
            d = t_device(device_id)
            self.process = WDAService(d, test_driver)
            if d.major_version() < 15:
                # cmds = [
                #     sys.executable, '-m', 'tidevice', '-u', d.udid, 'relay',
                #     '8200', '8100'
                # ]
                # self.replay = subprocess.Popen(cmds, stdout=None, stderr=None,
                #                                shell=True)
                self.process.start()
            else:
                d.app_start(test_driver)

            time.sleep(1)
            self.wait_ready(timeout)
        except Exception as wda_error:
            self.close()
            logger.info(f"start wda proxy fail:{str(wda_error)}")

    def connect(self, device_id, timeout):
        try:
            dev = None
            if PC.check_ip(device_id):
                dev = connect_device(f"ios:///{device_id}")
            else:
                dev = connect_device(f"ios:///http+usbmux://{device_id}")
            return dev
        except Exception as c_e:
            logger.info(f"connect device fail: {str(c_e)}")
            self.close()

    def set_current(self, device_id, timeout):
        try:
            dev = None
            if PC.check_ip(device_id):
                dev = set_current(f"{device_id}")
            else:
                dev = set_current(f"http+usbmux://{device_id}")
            return dev
        except Exception as c_e:
            logger.info(f"set_current device fail: {str(c_e)}")
            self.close()

    @staticmethod
    def static_set_current(device_id, timeout):
        try:
            dev = None
            if PC.check_ip(device_id):
                dev = set_current(f"{device_id}")
            else:
                dev = set_current(f"http+usbmux://{device_id}")
            return dev
        except Exception as c_e:
            logger.info(f"set_current device fail: {str(c_e)}")

    @staticmethod
    def static_connect(device_id):
        try:
            dev = None
            if PC.check_ip(device_id):
                dev = connect_device(f"ios:///{device_id}")
            else:
                dev = connect_device(f"ios:///http+usbmux://{device_id}")
            return dev
        except Exception as c_e:
            logger.info(f"connect device fail: {str(c_e)}")

    @staticmethod
    def check_ip(ip_addr):
        result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", ip_addr)
        if result:
            return True
        else:
            return False

    def close(self):
        if hasattr(self, "process") and self.process is not None:
            self.process.stop()

        if hasattr(self, "replay") and self.replay is not None:
            self.replay.terminate()

    def wait_ready(self, timeout):
        deadline = time.time() + timeout

        while time.time() <= deadline:
            if hasattr(self, "process") and self.process is not None:
                if self.process._is_alive() is True:
                    break
            time.sleep(1)
            logger.info("device not ready")
